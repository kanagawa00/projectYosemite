'''
20190125 增加分批抓取注释
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time,re,requests
import pandas as pd

search_keyword="汶川地震"
browser = webdriver.Chrome()
################################################
#学外アクセス
def gakugai(browser,un,pw):
    browser.get("http://www.wul.waseda.ac.jp.ez.wul.waseda.ac.jp/DOMEST/db_about/pdo/pdo.html")
    elem_user = browser.find_element_by_name("user")
    elem_user.send_keys(un)
    elem_pwd = browser.find_element_by_name("pass")
    elem_pwd.send_keys(pw)
    browser.find_element_by_xpath('//*[@type="submit"]').click()
    time.sleep(1)
    browser.find_element_by_class_name("A_button").click()
    time.sleep(1)
    browser.switch_to_window(browser.window_handles[1])
    browser.get("http://data.people.com.cn.ez.wul.waseda.ac.jp/rmrb")
user="##########"
password="############"
#gakugai(browser,user,password)
################################################
#学内
browser.get("http://data.people.com.cn.ez.wul.waseda.ac.jp/rmrb")
################################################
#時期限定検索
def phase(browser,search_keyword,timeA,timeB):
    #browser.get("http://data.people.com.cn/rmrb/")
    browser.maximize_window()
    browser.find_element_by_xpath('//*[@value="2"and@name="dateTimeType"]').click()
    browser.find_element_by_name("dateTimeStart").send_keys(timeA)
    browser.find_element_by_name("dateTimeEnd").send_keys(timeB)
    browser.find_element_by_xpath('//*[@type="text"and@name="contentText"]').send_keys(search_keyword)
    browser.find_element_by_xpath('//*[@type="submit"and@class="input_s"]').click()
#ステップ①時期変更
starttime="2012-01-01"
endtime="2013-12-31"
phase(browser,search_keyword,starttime,endtime)

###############################################
#検索
#browser.get("http://data.people.com.cn/rmrb/")
#browser.find_element_by_name("queryStr").send_keys(search_keyword)
#browser.find_element_by_class_name("search_btn").click()
#browser.find_element_by_id("searchInAll").click()
browser.find_element_by_xpath('//*[@class="sortUl_li"and@value="1"]').click()
time.sleep(1)
################################################
#ステップ②記事番号更新
filenum="0856"
articles=[]

def onepage(browser,start,pdlist):
    linklist=[]
    for link in browser.find_elements_by_xpath('//*[@class="open_detail_link"]'):
        #htmldata=requests.get(link.get_attribute("href")).text
        getlink=link.get_attribute("href")
        linklist.append(getlink)
    for truelink in linklist:
        onettl,onedetail,oneset=getdetail(browser,truelink)        
        fn=start
        f=open("C:\\Users\\kanag\\Desktop\\Renminribao\\"+fn+".txt","w",encoding="utf-8")
        f.write("<title>"+onettl+"</title>")
        f.write("\n")
        f.write(onedetail)
        f.close()
        pdlist.append(oneset)
        start=str("%04d" % (int(start)+1))
        time.sleep(0.5)
    try:
        browser.find_element_by_xpath('//*[@title="下一页"]').click()
    except:
        pass
    return start

def getdetail(browser,url):
    #url.click()
    #browser.switch_to_window(browser.window_handles[1])
    browser.get(url)
    ttl=browser.find_element_by_class_name("title").text
    left=browser.find_element_by_class_name("sha_left").text
    date=re.search(r"(?<=人民日报)\d{4}年\d{1,2}月\d{1,2}日",left).group()
    area=re.search(r"第\d{1,2}版",left).group()
    try:
        category=re.search(r"(?<=版).+(?=】)",left).group()
    except:
        category=""
    detail=browser.find_element_by_class_name("detail_con").text
    #print(ttl)
    #print(detail)
    time.sleep(0.75)
    browser.back()
    time.sleep(0.25)
    return ttl,detail,[ttl,date,area,category]

#ページの切り替え
w_start=1
w_news=browser.find_element_by_xpath('//*[@id="allDataCount"]')
w_page=int(w_news.text)//20+1
while w_start<=w_page:
    filenum=onepage(browser,filenum,articles)
    w_start+=1
    
browser.quit()

#ステップ③CSVファイルネーム番号変更
df = pd.DataFrame(articles,columns=["タイトル","時間","版","カテゴリー"])
df.to_csv("Renminribao4.csv",encoding="utf-8",sep="\t", index=False)
df
