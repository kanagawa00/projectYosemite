from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd
waseda_username="######"
keypass="#######"
search_keyword="GMO"
#早稲田検索ページを開ける
browser = webdriver.Chrome()
browser.get("http://waseda.summon.serialssolutions.com/jp/search?q=%E6%9C%9D%E6%97%A5%E6%96%B0%E8%81%9E&l=jp#!/search?ho=t&l=jp&q=%E6%9C%9D%E6%97%A5%E6%96%B0%E8%81%9E")
time.sleep(3)
targetlink=browser.find_element_by_xpath('//*[@ng-bind="::item.bet.title"]')
targetlink.click()
print("1.検索完了")
#新しいページでログインする
allHandles = browser.window_handles
for handle in allHandles:
    if browser.title.find("EZproxy") == -1:
        browser.switch_to_window(handle)
#elem_user = browser.find_element_by_name("user")
#elem_user.send_keys(waseda_username)
#elem_pwd = browser.find_element_by_name("pass")
#elem_pwd.send_keys(keypass)
#browser.find_element_by_xpath('//*[@type="submit"]').click()
#time.sleep(2)
browser.find_element_by_xpath('//*[@alt="ログイン（Login）へ"]').click()
time.sleep(3)
print("2.ログイン完了")
browser.switch_to_frame("Introduce")
browser.find_element_by_xpath('//input[@id="chkShishi2"]').click()
browser.find_element_by_xpath('//input[@id="chkShishi3"]').click()
browser.find_element_by_xpath('//input[@id="chkShishi4"]').click()
#検索キーワードを入力する
elem_inkw = browser.find_element_by_name("txtWord")
elem_inkw.send_keys(search_keyword)
time.sleep(1)
browser.find_element_by_xpath('//input[@value="検索実行"]').click()

#一覧表示&テキストスクレイピングのプログラム
def newsdownload(nl):
    browser.find_element_by_xpath('//input[@name="btnCheckOn"]').click()
    browser.find_element_by_xpath('//input[@name="btnDetail"]').click()
    numlist=browser.find_elements_by_xpath('//td[@class="topic-list"]//nobr')
    ttllist=browser.find_elements_by_class_name("font002")
    newslist=browser.find_elements_by_class_name("detail001")
    
    datelist=[]
    for i in range(int(len(numlist)/2)):
        datelist.append(str(numlist[i*2].text+numlist[i*2+1].text))
    for date,ttl,news in zip(datelist,ttllist,newslist):
        nl.append([date,ttl.text,news.text])
        print("<h1>",date,"</h1>")
        print("<h2>",ttl.text,"</h2")
        print(news.text)
        print("■■■■■■■■■■■■■■■■■■")
    time.sleep(2)
    browser.find_element_by_xpath('//img[@alt="検索一覧画面へ戻る"]').click()
    time.sleep(1)
    try:
        browser.find_element_by_name("next").click()
    except:
        pass

#ページの切り替え
articles=[]

w_start=1
w_news=browser.find_element_by_xpath('//*[@class="fontcolor001"]')
w_page=int(w_news.text)//20+1
while w_start<=w_page:
    newsdownload(articles)
    w_start+=1

#browser.close()
browser.quit()
#データフレーム構築
df = pd.DataFrame(articles,columns=["時間","タイトル","記事"])
print(df)


import pandas as pd
import matplotlib.pyplot as plt
#data=pd.read_csv("最終課題.csv",encoding="utf-8", sep="\t",engine="python",usecols=[0])
#content=pd.read_csv("最終課題.csv",encoding="utf-8", sep="\t",engine="python",usecols=[2])
#content.to_csv("最終課題（コンテンツ）.txt",encoding="utf-8",index=False)
#data=pd.read_csv("最終課題.csv",encoding="utf-8", sep="\t",engine="python")
#print(data["1.Date"])
x=[]
y=[]
for n in range(1988,2019):
    year=df["時間"].str.startswith(str(n)).sum()
    x.append(n)
    y.append(year)
    #print(n,"年：",year,"件")
###########################################################
plt.figure(figsize=(10,4))
plt.plot(x,y,color="red", linewidth=3.0, linestyle="--")
plt.xticks(fontsize=15)
plt.yticks(fontsize=15) 
font ={"family":"SimHei","weight":"normal","size":15}
plt.title("図1",font)
plt.xlabel("年",font)
plt.ylabel("件数",font)
plt.show()
##########################################################
