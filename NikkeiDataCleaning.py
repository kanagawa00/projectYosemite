import pandas as pd
f=open("nikkei.txt", "r")
fr=f.read().split("印刷対象にする")
articles=[]
for data in fr:
    try:
        tmp=str(data).split("その他の書誌情報を表示")
        tmp2=tmp[0].split("\n")
        ttl=tmp2[1]
        ctt=tmp[1]
        tmp3=tmp2[2].split(" ")
        date,daynight,page,size=tmp3[0],tmp3[1],tmp3[2],tmp3[3]
        print(ttl,"\n",ctt) 
        articles.append([ttl,date,daynight,page,size])
    except:
        pass
    
df = pd.DataFrame(articles,columns=["タイトル","時間","版","ページ","文字数"])
#df.to_csv("Nikkei.csv",encoding="utf-8",sep="\t", index=False)
df
