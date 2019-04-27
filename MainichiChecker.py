from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
#waseda_username="#######"
#keypass="#######"
search_keyword="千の証言： OR 戦後７０年： OR 戦後７０年これまで・これから： OR 戦後７０年・戦後７０年の夏： OR 特集ワイド： OR 会いたい・戦後７０年の夏に"
dffile=[]
#f=open("MainichiChecker.txt","w",encoding="utf-8")
#早稲田検索ページを開ける
browser = webdriver.Chrome()
#browser.get("http://waseda.summon.serialssolutions.com/jp/search?q=%E6%AF%8E%E6%97%A5%E6%96%B0%E8%81%9E&l=jp#!/search?ho=t&l=jp&q=%E6%AF%8E%E6%97%A5%E6%96%B0%E8%81%9E")
#time.sleep(3)
#browser.find_element_by_xpath('//*[@ng-bind="::item.bet.title"]').click()
#print("1.検索完了")
#新しいページでログインする
#allHandles = browser.window_handles
#for handle in allHandles:
#    if browser.title.find("EZproxy") == -1:
#        browser.switch_to_window(handle)

#学外アクセス
#elem_user = browser.find_element_by_name("user")
#elem_user.send_keys(waseda_username)
#elem_pwd = browser.find_element_by_name("pass")
#elem_pwd.send_keys(keypass)
#browser.find_element_by_xpath('//*[@type="submit"]').click()
#time.sleep(2)
#browser.find_element_by_xpath('//div[@class="item clr"]//a[@target="WMSK"]').click()

browser.get("https://dbs.g-search.or.jp/WMAI/WMAI_ipcu_login.html")

browser.get("https://dbs.g-search.or.jp/aps/WMSK/main.jsp?uji.verb=GSHWA0300&serviceid=WMSK")
time.sleep(3)
print("2.ログイン完了")

#キーワード入力
elem_inkw = browser.find_element_by_name("paraTi")
elem_inkw.send_keys(search_keyword)

#期間限定
Select(browser.find_element_by_name("paraYearFrom")).select_by_value("2015") 
Select(browser.find_element_by_name("paraMonthFrom")).select_by_value("1") 
Select(browser.find_element_by_name("paraDayFrom")).select_by_value("1")
Select(browser.find_element_by_name("paraFromTo")).select_by_value("1")
Select(browser.find_element_by_name("paraYearTo")).select_by_value("2015") 
Select(browser.find_element_by_name("paraMonthTo")).select_by_value("12") 
Select(browser.find_element_by_name("paraDayTo")).select_by_value("31")

#見出しだけ検索
browser.find_element_by_xpath('//*[@value="34"]').click()

#東京朝刊＆東京夕刊限定
browser.find_element_by_xpath('//*[@value="東京朝刊"]').click()
browser.find_element_by_xpath('//*[@value="東京夕刊"]').click()

time.sleep(1)
browser.find_element_by_name("btn1Top").click()


#検索結果一覧表示
browser.find_element_by_xpath('//*[@name="paraSort" and @value="4"]').click()
Select(browser.find_element_by_name("paraHyoujiKensuu")).select_by_value("200")
w_news=browser.find_element_by_xpath('//*[@class="num"]').text
browser.find_element_by_xpath('//*[@value="一覧表示"]').click()

#一括表示&テキストスクレイピングのプログラム
def newsdownload(browser,nl):
    #検索結果一括表示
    browser.find_element_by_xpath('//*[@alt="全て選択"]').click()
    browser.find_element_by_xpath('//*[@alt="一括表示"]').click()
    
    #コンテンツ収集
    ttllist=browser.find_elements_by_class_name("title")
    arclist=browser.find_elements_by_class_name("article")
    
    for content,article in zip(ttllist,arclist):
        content=content.text.split("\n")
        ttl=content[0]
        ctt=content[1]
        ctt=ctt.split("　")
        date,area,size=ctt[0],ctt[1],ctt[-1]
        if "頁" in ctt[2]:
            page=ctt[2]
        else:
            page=""
        #if "頁" or "地方版" in ctt[-2]:
        #    men=""
        #else:
        men=ctt[-2]
        nl.append([date.replace(".","/"),ttl,area,men,page,size,article.text])
        #print(ttl+"\n")
        #print(date+"\n")
        #print(article.text)
        #f.write("<H3>"+ttl+"</H3>"+"\n")
        #f.write("<H4>"+date+"</H4>"+"\n")
        #f.write("\n"+article.text+"\n\n\n")
        
    #一覧に戻る
    browser.find_element_by_xpath('//*[@onclick="execute(\'sys_form\',\'Back\',\'C\')"]').click()

#ページの切り替え
w_start=1
w_page=int(w_news)//200+1
while w_start<=w_page:
    newsdownload(browser,dffile)
    nextpage="//*[@onclick=\"javascript:execute(\'sys_form\', \'Page\', \'"+str(w_start+1)+"\');return false;\"]"
    try:
        browser.find_element_by_xpath(nextpage).click()
    except:
        pass
    w_start+=1

browser.quit()
#f.close()

#データフレーム構築
df = pd.DataFrame(dffile,columns=["時間","タイトル","朝夕刊","面","ページ","文字数","記事内容"])
#df.to_csv("C_MainichiCheck.csv",encoding="utf-8",sep="\t", index=False)
df.to_excel('Mainichi.xlsx', sheet_name='sheet1')
df
