'''
Copy all data from SankeiDatabase to a local text file at first, 
then divide news by "■■■■■■■■■■■■■■■■■■\n" and run the code.
'''

import pandas as pd

f=open("C:\\Users\\kanag\\Desktop\\戦争責任.txt","r",encoding="utf-8").read()
articles=[]
kijis=f.split("■■■■■■■■■■■■■■■■■■\n")
print(len(kijis))
for kiji in kijis:
    kijipart=kiji.split("\n  閉じる\nテキスト切り抜き画像 印刷別ウインドウで開く\n")
    ctt=kijipart[1]
    part=kijipart[0].split("\n")
    ttl=part[0]
    tmp=part[1].split("・")
    date,area,men=tmp[0],tmp[1],tmp[2]
    articles.append([date,ttl,area,men,len(ctt),ctt])
    
df = pd.DataFrame(articles,columns=["時間","タイトル","朝夕刊","面","文字数","記事内容"])
df.to_excel('C:\\Users\\kanag\\Desktop\\Sankei.xlsx', sheet_name='sheet1')
df
