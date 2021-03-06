'''
20190112 機能追加「各地域版を個別に選択する」
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd

#search_keyword="GMO"

articles=[]
#f=open("C_YomiuriChecker1.txt","w",encoding="utf-8")

#一覧表示&テキストスクレイピングのプログラム
def newsdownload(browser,nl):
    browser.find_element_by_xpath('//*[@onclick="toggleCheck(document.forms[\'search\'], \'yomiuriNewsArticleDto.chkboxCollectiveIndication\', true);return false;"]').click()
    browser.find_element_by_xpath('//*[@onclick="validateAllDisplayCheckBox(\'yomiuriNewsArticleDto.chkboxCollectiveIndication\', \'search\', new Array(\'表示チェックが選択されていません。\', \'一括表示できる件数は20件までです。続行しますか？\'), \'yomiuriNewsArticle.action?allDisplayFlg=true\');return false;"]').click()
    datelist=browser.find_elements_by_xpath('//*[@style="width:80px;vertical-align:middle;"]')
    alllist=browser.find_elements_by_xpath('//table[@class="contentsTable"]/tbody/tr')
    daynightlist,arealist,pagelist,sizelist=[],[],[],[]
    for tmps in alllist:
        tmps=str(tmps.text)
        tlist=tmps.split(" ")
        daynightlist.append(tlist[3])
        arealist.append(tlist[4])
        pagelist.append(tlist[5])
        sizelist.append(tlist[6])

    ttllist=browser.find_elements_by_class_name("wp50")
    newslist=browser.find_elements_by_class_name("mb10")
    for date,ttl,news,daynight,area,page,size in zip(datelist,ttllist,newslist,daynightlist,arealist,pagelist,sizelist):
        #if daynight.startswith("東京朝刊") or daynight.startswith("東京夕刊"):
            #print(daynight.text)
            #print(date.text)
            #print(ttl.text)
            #print(news.text)
            #f.write("<H1>"+date.text+"</H1>"+"\n")
            #f.write("<H2>"+ttl.text+"</H2>"+"\n")
            #f.write("\n"+news.text+"\n\n\n")
            #print("■■■■■■■■■■■■■■■■■■")
        nl.append([date.text,ttl.text,daynight,area,page,size,news.text])
        #else:
        #    pass
    time.sleep(3)
    browser.find_element_by_xpath('//*[@onclick="execute(document.forms[\'article\'], \'yomiuriNewsPageSearchList.action\');return false;"]').click()
    time.sleep(1)
    browser.find_element_by_class_name("nextPage").click()

#早稲田検索ページを開ける
def getpage(browser,search_keyword,newsdata):
    #browser.get("http://waseda.summon.serialssolutions.com/jp/search?q=%E8%AA%AD%E5%A3%B2%E6%96%B0%E8%81%9E&l=jp#!/search?ho=t&l=jp&q=%E8%AA%AD%E5%A3%B2%E6%96%B0%E8%81%9E")
    #time.sleep(3)
    #targetlink=browser.find_element_by_xpath('//*[@ng-bind="::item.bet.title"]')
    #targetlink.click()
    #print("1.検索完了")
    #新しいページでログインする
    #allHandles = browser.window_handles
    #for handle in allHandles:
    #    if browser.title.find("EZproxy") == -1:
    #        browser.switch_to_window(handle)
    #elem_user = browser.find_element_by_name("user")
    #elem_user.send_keys("tsh")
    #elem_pwd = browser.find_element_by_name("pass")
    #elem_pwd.send_keys("Aragaki01!")
    #browser.find_element_by_xpath('//*[@type="submit"]').click()
    browser.get("https://database.yomiuri.co.jp/rekishikan/")
    time.sleep(2)
    #print("2.ログイン完了")
    #読売歴史館に入った後、検索モードを平成モードに切り替える
    browser.get("https://database-yomiuri-co-jp.ez.wul.waseda.ac.jp/rekishikan/yomiuriNewsSearch.action")
    time.sleep(1)
    #検索キーワードを入力する
    elem_inkw = browser.find_element_by_name("yomiuriNewsSearchDto.txtWordSearch")
    elem_inkw.send_keys(search_keyword)
    
    browser.find_element_by_xpath('//*[@value="100"]').click() #100件表示

    browser.find_element_by_class_name("choiceArea1Open").click()  #個別に選択する
    browser.find_element_by_xpath(u'//*[@title="全国版"]').click() #全国版
    browser.find_element_by_xpath(u'//*[@title="地域版"]').click() #地域版
    
    #各地域版を個別に選択する
    browser.find_element_by_xpath(u'//*[@title="各地域版を個別に選択する"]').click()
    ##関東
    browser.find_element_by_xpath(u'//*[@title="茨城"]').click()
    browser.find_element_by_xpath(u'//*[@title="栃木"]').click()
    browser.find_element_by_xpath(u'//*[@title="群馬"]').click()
    browser.find_element_by_xpath(u'//*[@title="埼玉"]').click()
    browser.find_element_by_xpath(u'//*[@title="千葉"]').click()
    browser.find_element_by_xpath(u'//*[@title="東京"]').click()
    browser.find_element_by_xpath(u'//*[@title="神奈川"]').click()
    
    #期間
    browser.find_element_by_id("txtSYear").send_keys("2011")
    browser.find_element_by_id("txtSMonth").send_keys("3")
    browser.find_element_by_id("txtSDay").send_keys("11")
    browser.find_element_by_id("txtEYear").send_keys("2018")
    browser.find_element_by_id("txtEMonth").send_keys("3")
    browser.find_element_by_id("txtEDay").send_keys("10")
    time.sleep(5)
    browser.find_element_by_id("yomiuriNewsSubmitButton").click()
    #print("3.検索完了")
    #print("■■■■■■■■■■■■■■■■■■")

    #ページの切り替え
    w_start=1
    w_news=browser.find_element_by_xpath('//*[@class="heiseiOperationLeft"]//*[@class="flL"]')
    w_news=w_news.text.replace(" 件中","")
    w_page=int(w_news)//100+1
    while w_start<=w_page:
        newsdownload(browser,newsdata)
        w_start+=1
#print("4.done")

#keywordlist=["(ワーキングママ OR ワーキング母 OR ワーママ OR ワーキングマザー OR 働くママ OR 働く母) AND (子ども OR 子育て OR 保育 OR 育児 OR ＰＴＡ OR 児童 OR 保育園 OR 出産 OR 育休 OR 子供 OR 主婦 OR 家事 OR 職場 OR 改革 OR キャリア OR 妊娠 OR 共働き OR 結婚 OR 産む OR 赤ちゃん)"]
#keywordlist=["［戦後７０年",
#             "［社会保障　戦後７０年］",
#             "［証言　大連の抑留］",
#             "［７０年後の返信］",
#             "［ニッポンの貢献　戦後７０年］",
#             "［語る］戦後７０年",
#             "［日米関係　戦後７０年］"]
keywordlist=["福島 AND (農 OR 漁 OR 畜 OR 風評被害)"]

browser = webdriver.Chrome()
for keyword in keywordlist:
    getpage(browser,keyword,articles)
browser.quit()
#データフレーム構築
df = pd.DataFrame(articles,columns=["時間","タイトル","地域","面","ページ","文字数","記事内容"])
#df.to_csv("C_YomiuriChecker1.csv",encoding="utf-8",sep="\t", index=False)
df.to_excel('LLZ_YomiuriCheck_FUKUSHIMA.xlsx', sheet_name='sheet1')
df
