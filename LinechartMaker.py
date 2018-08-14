import pandas as pd
import matplotlib.pyplot as plt
data=pd.read_csv("最終課題.csv",encoding="utf-8", sep="\t",engine="python",usecols=[0])
#content=pd.read_csv("最終課題.csv",encoding="utf-8", sep="\t",engine="python",usecols=[2])
#content.to_csv("最終課題（コンテンツ）.txt",encoding="utf-8",index=False)
#data=pd.read_csv("最終課題.csv",encoding="utf-8", sep="\t",engine="python")
#print(data["1.Date"])
x=[]
y=[]
for n in range(1980,2019):
    year=data["1.Date"].str.startswith(str(n)).sum()
    x.append(n)
    y.append(year)
    #print(n,"年：",year,"件")
###########################################################
plt.figure(figsize=(10,4))
plt.plot(x,y,color="red", linewidth=3.0, linestyle="--")
plt.xticks(fontsize=15)
plt.yticks(fontsize=15) 
font ={"family":"SimHei","weight":"normal","size":15}
plt.title("図1　人民日報におけるタイトルに人工知能が含まれる報道の経時的な推移",font)
plt.xlabel("年",font)
plt.ylabel("件数",font)
plt.show()