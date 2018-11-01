from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd

#search_keyword="GMO"

articles=[]
fa=open("D_YomiuriChecker1.txt","w",encoding="utf-8")
fa.write("<H1>第一期</H1>\n<H2>読売新聞</H2>\n")
fb=open("D_YomiuriChecker2.txt","w",encoding="utf-8")
fb.write("<H1>第二期</H1>\n<H2>読売新聞</H2>\n")
fc=open("D_YomiuriChecker3.txt","w",encoding="utf-8")
fc.write("<H1>第三期</H1>\n<H2>読売新聞</H2>\n")
timenode_a=20121010
timenode_b=20131010
def khcoderwrite(f,fd,ft,fn):
    f.write("<H3>"+fd.text+"</H3>"+"\n")
    f.write("<H4>"+ft.text+"</H4>"+"\n")
    f.write("\n"+fn.text+"\n\n\n")

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
        if daynight.startswith("東京朝刊") or daynight.startswith("東京夕刊"):
            #print(daynight.text)
            #print(date.text)
            #print(ttl.text)
            #print(news.text)
            timenode=int(date.text.replace(".",""))
            if timenode > timenode_b:
                khcoderwrite(fa,date,ttl,news)
                node="第三期"
            elif timenode >= timenode_a and timenode < timenode_b:
                khcoderwrite(fb,date,ttl,news)
                node="第二期"
            else:
                khcoderwrite(fc,date,ttl,news)
                node="第一期"
            #print("■■■■■■■■■■■■■■■■■■")
            nl.append([node,date.text,ttl.text,daynight,area,page,size])
        else:
            pass
    time.sleep(3)
    browser.find_element_by_xpath('//*[@onclick="execute(document.forms[\'article\'], \'yomiuriNewsPageSearchList.action\');return false;"]').click()
    time.sleep(1)
    browser.find_element_by_class_name("nextPage").click()

#早稲田検索ページを開ける
def getpage(browser,search_keyword,newsdata):
    browser.get("http://waseda.summon.serialssolutions.com/jp/search?q=%E8%AA%AD%E5%A3%B2%E6%96%B0%E8%81%9E&l=jp#!/search?ho=t&l=jp&q=%E8%AA%AD%E5%A3%B2%E6%96%B0%E8%81%9E")
    time.sleep(3)
    targetlink=browser.find_element_by_xpath('//*[@ng-bind="::item.bet.title"]')
    targetlink.click()
    #print("1.検索完了")
    #新しいページでログインする
    allHandles = browser.window_handles
    for handle in allHandles:
        if browser.title.find("EZproxy") == -1:
            browser.switch_to_window(handle)
    #elem_user = browser.find_element_by_name("user")
    #elem_user.send_keys("tsh")
    #elem_pwd = browser.find_element_by_name("pass")
    #elem_pwd.send_keys("Aragaki01!")
    #browser.find_element_by_xpath('//*[@type="submit"]').click()
    time.sleep(2)
    #print("2.ログイン完了")
    #読売歴史館に入った後、検索モードを平成モードに切り替える
    browser.get("https://database-yomiuri-co-jp.ez.wul.waseda.ac.jp/rekishikan/yomiuriNewsSearch.action")
    time.sleep(1)
    #検索キーワードを入力する
    elem_inkw = browser.find_element_by_name("yomiuriNewsSearchDto.txtWordSearch")
    elem_inkw.send_keys(search_keyword)

    browser.find_element_by_class_name("choiceArea1Open").click()
    browser.find_element_by_name("yomiuriNewsSearchDto.selSelectArea").click()
    browser.find_element_by_id("txtSYear").send_keys("2016")
    browser.find_element_by_id("txtSMonth").send_keys("4")
    browser.find_element_by_id("txtSDay").send_keys("1")
    browser.find_element_by_id("txtEYear").send_keys("2017")
    browser.find_element_by_id("txtEMonth").send_keys("12")
    browser.find_element_by_id("txtEDay").send_keys("31")
    time.sleep(5)
    browser.find_element_by_id("yomiuriNewsSubmitButton").click()
    #print("3.検索完了")
    #print("■■■■■■■■■■■■■■■■■■")

    #ページの切り替え
    w_start=1
    w_news=browser.find_element_by_xpath('//*[@class="heiseiOperationLeft"]//*[@class="flL"]')
    w_news=w_news.text.replace(" 件中","")
    w_page=int(w_news)//50+1
    while w_start<=w_page:
        newsdownload(browser,newsdata)
        w_start+=1
#print("4.done")

keywordlist=["(ワーキングママ OR ワーキング母 OR ワーママ OR ワーキングマザー OR 働くママ OR 働く母) AND (子ども OR 子育て OR 保育 OR 育児 OR ＰＴＡ OR 児童 OR 保育園 OR 出産 OR 育休 OR 子供 OR 主婦 OR 家事 OR 職場 OR 改革 OR キャリア OR 妊娠 OR 共働き OR 結婚 OR 産む OR 赤ちゃん)"]
#keywordlist=["尖閣諸島 AND 国有"]
browser = webdriver.Chrome()
for keyword in keywordlist:
    getpage(browser,keyword,articles)
browser.quit()
fa.close()
fb.close()
fc.close()
#データフレーム構築
df = pd.DataFrame(articles,columns=["時期","時間","タイトル","地域","面","ページ","文字数"])
df.to_csv("D_YomiuriChecker.csv",encoding="utf-8",sep="\t", index=False)
df
