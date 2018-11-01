import pandas as pd
import matplotlib.pyplot as plt

frames=[]
for datanum in range(2,12):
    filename="Renminribao"+str(datanum)+".csv"
    locals()["df"+str(datanum)]=pd.read_csv(filename,encoding="utf-8", sep="\t",engine="python")
    frames.append(locals()["df"+str(datanum)])

result = pd.concat(frames)
result.to_csv("Renminribao.csv",encoding="utf-8",sep="\t", index=False)
result


import matplotlib.pyplot as plt

x,y=[],[]
for n in range(1949,2019):
    year=result["時間"].str.startswith(str(n)).sum()
    x.append(n)
    y.append(year)
    #print(n,"年：",year,"件")
###########################################################
%matplotlib
plt.figure(figsize=(10,4))
plt.bar(x,y,color="black", linewidth=3.0, linestyle="--")
#plt.plot(x,y,color="black", linewidth=3.0, linestyle="--")
plt.xticks(fontsize=15)
plt.yticks(fontsize=15) 
font ={"family":"SimHei","weight":"normal","size":15}
plt.title("図1",font)
plt.xlabel("年",font)
plt.ylabel("件数",font)
plt.show()
##########################################################



#第一面に出現される回数

import matplotlib.pyplot as plt

x,y=[],[]
first=result.loc[result["版"]=="第1版",["時間"]]

for n in range(1949,2019):
    num=first["時間"].str.startswith(str(n)).sum()
    x.append(n)
    y.append(num)
    #print(n,"年：",num,"件")
###########################################################
%matplotlib
plt.figure(figsize=(10,4))
plt.bar(x,y,color="black", linewidth=3.0, linestyle="--")
#plt.plot(x,y,color="black", linewidth=3.0, linestyle="--")
plt.xticks(fontsize=15)
plt.yticks(fontsize=15) 
font ={"family":"SimHei","weight":"normal","size":15}
plt.title("図2",font)
plt.xlabel("年",font)
plt.ylabel("件数",font)
plt.show()
##########################################################



#「重要なニュース」として報道される回数

import matplotlib.pyplot as plt

x,y=[],[]
top=result.loc[result["カテゴリー"]=="要闻",["時間"]]

for n in range(1949,2019):
    num=top["時間"].str.startswith(str(n)).sum()
    x.append(n)
    y.append(num)
    #print(n,"年：",num,"件")
###########################################################
%matplotlib
plt.figure(figsize=(10,4))
plt.bar(x,y,color="black", linewidth=3.0, linestyle="--")
#plt.plot(x,y,color="black", linewidth=3.0, linestyle="--")
plt.xticks(fontsize=15)
plt.yticks(fontsize=15) 
font ={"family":"SimHei","weight":"normal","size":15}
plt.title("図3 「重要なニュース」として報道される回数",font)
plt.xlabel("年",font)
plt.ylabel("件数",font)
plt.show()
##########################################################
