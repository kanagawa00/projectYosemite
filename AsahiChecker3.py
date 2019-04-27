from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
waseda_username="######"
keypass="######"
keywordlist=["(ワーキングママ+ワーキング母+ワーママ+ワーキングマザー+働くママ+働く母)&(子ども+子育て+保育+育児+ＰＴＡ+児童+保育園+出産+育休+子供+主婦+家事+職場+改革+キャリア+妊娠+共働き+結婚+産む+赤ちゃん)"]
#keywordlist=["尖閣諸島&国有"]
articles=[]
fa=open("D_AsahiChecker1.txt","w",encoding="utf-8")
fa.write("<H1>第一期</H1>\n<H2>朝日新聞</H2>\n")
fb=open("D_AsahiChecker2.txt","w",encoding="utf-8")
fb.write("<H1>第二期</H1>\n<H2>朝日新聞</H2>\n")
fc=open("D_AsahiChecker3.txt","w",encoding="utf-8")
fc.write("<H1>第三期</H1>\n<H2>朝日新聞</H2>\n")
timenode_a=20121010
timenode_b=20131010
def khcoderwrite(f,fd,ft,fn):
    f.write("<H3>"+fd+"</H3>"+"\n")
    f.write("<H4>"+ft.text+"</H4>"+"\n")
    f.write("\n"+fn.text+"\n\n\n")


#一覧表示&テキストスクレイピングのプログラム
def newsdownload(browser,nl):
    browser.find_element_by_xpath('//input[@name="btnCheckOn"]').click()
    browser.find_element_by_xpath('//input[@name="btnDetail"]').click()
    numlist=browser.find_elements_by_xpath('//td[@class="topic-list"]//nobr') #掲載日
    arealist=browser.find_elements_by_xpath('//td[@class="topic-list"and@align="center"]') #掲載日
    time.sleep(1)
    ttllist=browser.find_elements_by_class_name("font002")
    
    #newslist=browser.find_elements_by_class_name("detail001")
    allnewslist=browser.find_elements_by_xpath('//table[@class="topic-detail"]/tbody/tr/td')
    newslist=[]
    for c in range(int(len(allnewslist)/3)):
        newslist.append(allnewslist[c*3+2])
    
    time.sleep(1)

    datelist=[]
    for i in range(int(len(numlist)/2)):
        datelist.append(str(numlist[i*2].text+numlist[i*2+1].text))

    nolist,daylist,menlist,pagelist,lenlist=[],[],[],[],[]
    for k in range(int(len(arealist)/6)):
        nolist.append(arealist[k*6].text)
        daylist.append(arealist[k*6+2].text)
        menlist.append(arealist[k*6+3].text)
        pagelist.append(arealist[k*6+4].text)
        lenlist.append(arealist[k*6+5].text)
    
    print("ttlist size:",len(ttllist))
    print("menlist size:",len(menlist))
    print("nolist size:",len(nolist))
    print("datelist size:",len(datelist))
    print("newslist size:",len(newslist))
    print("daylist size:",len(daylist))
    print("pagelist size:",len(pagelist))
    print("lenlist size:",len(lenlist))
    
    for no,date,ttl,news,day,men,page,size in zip(nolist,datelist,ttllist,newslist,daylist,menlist,pagelist,lenlist):
        if news.text.startswith("※著作権などの関係で本文を表示できません。"):
            pass
        else:
            timenode=int(date.replace("年","").replace("月","").replace("日",""))
            if timenode > timenode_b:
                khcoderwrite(fa,date,ttl,news)
                node="第三期"
            elif timenode >= timenode_a and timenode < timenode_b:
                khcoderwrite(fb,date,ttl,news)
                node="第二期"
            else:
                khcoderwrite(fc,date,ttl,news)
                node="第一期"
            nl.append([node,no,date,ttl.text,day,men,page,size])
            #print("■■■■■■■■■■■■■■■■■■")
    time.sleep(2)
    browser.find_element_by_xpath('//img[@alt="検索一覧画面へ戻る"]').click()
    time.sleep(1)
    try:
        browser.find_element_by_name("next").click()
    except:
        pass


def getpage(browser,search_keyword,newsdata):
#早稲田検索ページを開ける
    browser.get("http://waseda.summon.serialssolutions.com/jp/search?q=%E6%9C%9D%E6%97%A5%E6%96%B0%E8%81%9E&l=jp#!/search?ho=t&l=jp&q=%E6%9C%9D%E6%97%A5%E6%96%B0%E8%81%9E")
    time.sleep(3)
    targetlink=browser.find_element_by_xpath('//*[@ng-bind="::item.bet.title"]')
    targetlink.click()
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
    time.sleep(2)
    browser.find_element_by_xpath('//*[@alt="ログイン（Login）へ"]').click()
    time.sleep(3)
    browser.switch_to_frame("Introduce")
    browser.find_element_by_xpath('//input[@id="chkShishi2"]').click()
    browser.find_element_by_xpath('//input[@id="chkShishi3"]').click()
    browser.find_element_by_xpath('//input[@id="chkShishi4"]').click()
    #検索キーワードを入力する
    elem_inkw = browser.find_element_by_name("txtWord")
    elem_inkw.send_keys(search_keyword)
    
    browser.find_element_by_xpath('//input[@id="rdoSrchMode2"]').click() #詳細検索
    #browser.find_element_by_xpath('//input[@id="rdoSrchItem3"]').click() #見出しだけ検索
    browser.find_element_by_xpath('//input[@id="chkHochi2"]').click() #地方紙
    browser.find_element_by_xpath('//input[@id="chkIssueS2"]').click()
    browser.find_element_by_xpath('//input[@id="chkIssueS3"]').click()
    browser.find_element_by_xpath('//input[@id="chkIssueS4"]').click()
    browser.find_element_by_xpath('//input[@id="chkIssueS5"]').click()
    Select(browser.find_element_by_name("cmbDspNum")).select_by_value("100") 

    Select(browser.find_element_by_name("cmbIDFy")).select_by_value("2015") 
    Select(browser.find_element_by_name("cmbIDFm")).select_by_value("04") 
    Select(browser.find_element_by_name("cmbIDFd")).select_by_value("01")
    Select(browser.find_element_by_name("cmbIDTy")).select_by_value("2017") 
    Select(browser.find_element_by_name("cmbIDTm")).select_by_value("12") 
    Select(browser.find_element_by_name("cmbIDTd")).select_by_value("31")

    time.sleep(1)
    browser.find_element_by_xpath('//input[@value="検索実行"]').click()

    #ページの切り替え
    w_start=1
    w_news=browser.find_element_by_xpath('//*[@class="fontcolor001"]')
    w_page=int(w_news.text)//100+1
    while w_start<=w_page:
        newsdownload(browser,newsdata)
        w_start+=1

    #browser.close()

browser = webdriver.Chrome()
for keyword in keywordlist:
    getpage(browser,keyword,articles)

browser.quit()
fa.close()
fb.close()
fc.close()
       
#データフレーム構築
df = pd.DataFrame(articles,columns=["時期","No","時間","タイトル","朝夕刊","面","ページ","文字数"])
df.to_csv("D_AsahiCheck2.csv",encoding="utf-8",sep="\t", index=False)
df
