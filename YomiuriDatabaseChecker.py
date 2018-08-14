from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
waseda_username="######"
keypass="#######"
search_keyword="GMO"
#早稲田検索ページを開ける
browser = webdriver.Chrome()
browser.get("http://waseda.summon.serialssolutions.com/jp/search?q=%E8%AA%AD%E5%A3%B2%E6%96%B0%E8%81%9E&l=jp#!/search?ho=t&l=jp&q=%E8%AA%AD%E5%A3%B2%E6%96%B0%E8%81%9E")
time.sleep(3)
targetlink=browser.find_element_by_xpath('//*[@ng-bind="::item.bet.title"]')
targetlink.click()
print("1.検索完了")
#新しいページでログインする
allHandles = browser.window_handles
for handle in allHandles:
    if browser.title.find("EZproxy") == -1:
        browser.switch_to_window(handle)
elem_user = browser.find_element_by_name("user")
elem_user.send_keys(waseda_username)
elem_pwd = browser.find_element_by_name("pass")
elem_pwd.send_keys(keypass)
browser.find_element_by_xpath('//*[@type="submit"]').click()
time.sleep(2)
print("2.ログイン完了")
#読売歴史館に入った後、検索モードを平成モードに切り替える
browser.get("https://database-yomiuri-co-jp.ez.wul.waseda.ac.jp/rekishikan/yomiuriNewsSearch.action")
time.sleep(1)
#検索キーワードを入力する
elem_inkw = browser.find_element_by_name("yomiuriNewsSearchDto.txtWordSearch")
elem_inkw.send_keys(search_keyword)
browser.find_element_by_id("yomiuriNewsSubmitButton").click()
print("3.検索完了")
print("■■■■■■■■■■■■■■■■■■")
#一覧表示&テキストスクレイピングのプログラム
def newsdownload():
    browser.find_element_by_xpath('//*[@onclick="toggleCheck(document.forms[\'search\'], \'yomiuriNewsArticleDto.chkboxCollectiveIndication\', true);return false;"]').click()
    browser.find_element_by_xpath('//*[@onclick="validateAllDisplayCheckBox(\'yomiuriNewsArticleDto.chkboxCollectiveIndication\', \'search\', new Array(\'表示チェックが選択されていません。\', \'一括表示できる件数は20件までです。続行しますか？\'), \'yomiuriNewsArticle.action?allDisplayFlg=true\');return false;"]').click()
    ttllist=browser.find_elements_by_class_name("wp50")
    newslist=browser.find_elements_by_class_name("mb10")
    for ttl,newslist in zip(ttllist,newslist):
        print(ttl.text)
        print(newslist.text)
        print("■■■■■■■■■■■■■■■■■■")
    time.sleep(3)
    browser.find_element_by_xpath('//*[@onclick="execute(document.forms[\'article\'], \'yomiuriNewsPageSearchList.action\');return false;"]').click()
    time.sleep(1)
    browser.find_element_by_class_name("nextPage").click()
#ページの切り替え
w_start=0
w_news=browser.find_element_by_xpath('//*[@class="heiseiOperationLeft"]//*[@class="flL"]')
w_news=w_news.text.replace(" 件中","")
w_page=int(w_news)//50+1
while w_start<w_page:
    newsdownload()
    w_start+=1
print("4.done")
browser.close()