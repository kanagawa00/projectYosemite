import re,requests
import pandas as pd
from bs4 import BeautifulSoup
urllist=[]
titleList=[]
leadList=[]
dateList=[]
#########################################
for n in range(1,12):
    num=str(n)
    link="http://data.people.com.cn/rmrb/s?qs=%7B%22cds%22%3A%5B%7B%22cdr%22%3A%22AND%22%2C%22cds%22%3A%5B%7B%22fld%22%3A%22title%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22true%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%22%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%22%7D%2C%7B%22fld%22%3A%22subTitle%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%22%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%22%7D%2C%7B%22fld%22%3A%22introTitle%22%2C%22cdr%22%3A%22OR%22%2C%22hlt%22%3A%22false%22%2C%22vlr%22%3A%22AND%22%2C%22qtp%22%3A%22DEF%22%2C%22val%22%3A%22%E4%BA%BA%E5%B7%A5%E6%99%BA%E8%83%BD%22%7D%5D%7D%5D%2C%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D&tr=A&ss=1&pageNo="+num+"&pageSize=20"
    urllist.append(link)
for URL in urllist:
    req=requests.get(URL)
    htmldata=BeautifulSoup(req.text, "html.parser")
########################################
    classdata=htmldata.select("div.sreach_li a.open_detail_link")
    patternT=re.compile(r"(?<=target=\"_blank\">).+(?=</a>)")
    for obj in classdata:
        titles=patternT.findall(str(obj))
        title=titles[0].replace("<em>","").replace("</em>","")
        titleList.append(title)
########################################
    classdate=htmldata.select("div.listinfo")
    patternD=re.compile(r"[0-9]{4}年[0-9]{1,2}月[0-9]{1,2}日")
    for obk in classdate:
        dates=patternD.findall(str(obk))
        dateList.append(dates[0])
#######################################
    classlead=htmldata.select("div.incon_text.clearfix p")
    for obl in classlead:
        lead=obl.text.replace("\t","").replace("\r\n","")
        leadList.append(lead)
#######################################
my_dict = {"1.Date": dateList,"2.Title": titleList,"3.Lead":leadList}
data=pd.DataFrame.from_dict(my_dict)
data.to_csv("最終課題.csv",encoding="utf-8",sep="\t", index=False)
print("done")
