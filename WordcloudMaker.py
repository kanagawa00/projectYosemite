import pandas as pd
df=pd.read_csv("最終課題.csv",encoding="utf-8", sep="\t",engine="python",usecols=[2])
sentence=""
for i in range(0, len(df)):
    sentence+=df.iloc[i][0]
    sentence+="\n\n"
########################################################
import jieba
import jieba.analyse
from collections import Counter
#seg_list = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造",cut_all=True)
#print("Full Mode:", "/ ".join(seg_list)) #全模式
#seg_list = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造",cut_all=False)
#print("Default Mode:", "/ ".join(seg_list)) #精确模式
#seg_list = jieba.cut("小明硕士毕业于中国科学院计算所，后在日本京都大学深造") #默认是精确模式
#print(", ".join(seg_list))
#seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造") #搜索引擎模式
#print(", ".join(seg_list))
#jieba.load_userdict(file_name)
jieba.add_word("机器学习",100,"n")
jieba.add_word("深度学习",100,"n")
jieba.add_word("大数据",100,"n")
seg_list=jieba.cut(sentence)
c=Counter()
#print("/".join(seg_list))
for x in seg_list:
    if len(x)>1 and x != '\r\n':
        c[x] += 1
print("1.頻出語上位トップ20")
for (k,v) in c.most_common(20):
    print(k,"|",v)
    #print("%s%s %s  %d" % ("  "*(5-len(k)), k, "*"*int(v/3), v))
######################################################
tags=jieba.analyse.extract_tags(sentence,100,False)
keywords=jieba.analyse.extract_tags(sentence,50,True)
print("2.TF-DF上位語トップ100")
print(",".join(tags))
print("3.TF-DF上位語トップ10とその値")
ruiji1=dict(keywords)
import matplotlib.pyplot as plt
import wordcloud
cloud = wordcloud.WordCloud(font_path="C:\Windows\Fonts\STXIHEI.TTF",width=500, height=200,background_color="white")
cloudlist=dict(keywords)
cloud.fit_words(cloudlist)
plt.figure(figsize=(10,10))
plt.imshow(cloud) # 在坐标轴上显示图像
plt.axis("off") # 去除图像坐标轴
plt.show() # 显示词云图

#以 jieba 與 gensim 探索文本主題 https://medium.com/pyladies-taiwan/-i-cd2147b89083

import pandas as pd
import jieba,codecs
import jieba.analyse
df=pd.read_csv("最終課題.csv",encoding="utf-8", sep="\t",engine="python",usecols=[2])
wtags = codecs.open("jieba_tags.txt", "w","utf-8")

for i in range(0, len(df)):
    sentence=df.iloc[i][0]
    #print(sentence)
    #tags = jieba.analyse.extract_tags(sentence,topK=10, withWeight=True)
    #for tag, weight in tags:
    #    print(tag + "," + str(weight))
    # 將每篇新闻的前10個tags存檔
    words = jieba.analyse.extract_tags(sentence,200)
    wtags.write(" ".join(words))

# 把所有新闻的前10個tags變為萃取資料的input
print("4.TF-IDF上位ワードクラウド")
with open("jieba_tags.txt", "rb") as jieba_tags:
    for line in jieba_tags:
        tags = jieba.analyse.extract_tags(line,50,True)
        ruiji2=dict(tags)
        keywords = jieba.analyse.extract_tags(line,15)
        print(",".join(keywords))
jieba_tags.close()

import matplotlib.pyplot as plt
import wordcloud
cloud = wordcloud.WordCloud(font_path="C:\Windows\Fonts\STXIHEI.TTF",width=500, height=200,background_color="white")
cloudlist=dict(tags)
cloud.fit_words(cloudlist)
plt.figure(figsize=(10,10))
plt.imshow(cloud) # 在坐标轴上显示图像
plt.axis("off") # 去除图像坐标轴
plt.show() # 显示词云图

import math
def sim_pearson(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    n = len(si)
    if n == 0: return 0
    mean1 = sum([prefs[person1][item] for item in si]) / n
    mean2 = sum([prefs[person2][item] for item in si]) / n
    variance1 = math.sqrt(sum([((prefs[person1][item] - mean1) ** 2) for item in si]))
    variance2 = math.sqrt(sum([((prefs[person2][item] - mean2) ** 2) for item in si]))
    covariance = sum([(prefs[person1][item] - mean1)*(prefs[person2][item] - mean2) for item in si])
    if variance1 * variance2 == 0: return 0
    return covariance / (variance1 * variance2)
print("5.TF-DF上位語とTF-IDF上位語のピアソンの積率相関係数")
data = {"TF-DF上位語": ruiji1,"TF-IDF上位語": ruiji2}
print(sim_pearson(data, "TF-DF上位語", "TF-IDF上位語"))

#KHCoderで解析した頻出語トップ50を読み込む
khdata=pd.read_csv("ruiji3.txt",encoding="utf-8", sep=";",engine="python",header=None)
khkeys=[]
khvalues=[]
for k in range(0, len(khdata)):
    khkeys.append(khdata.iloc[k][0])
    khvalues.append(khdata.iloc[k][1])
ruiji3=dict(list(zip(khkeys,khvalues)))

print("6.JiebaとKHCoderのTF-DF上位語のピアソンの積率相関係数")
data = {"TF-DF上位語": ruiji1,"TF-DF上位語(KHCoder)": ruiji3}
print(sim_pearson(data, "TF-DF上位語", "TF-DF上位語(KHCoder)"))

del ruiji1["人工智能"]
del ruiji2["人工智能"]
del ruiji3["人工智能"]

print("7.TF-DF上位語とTF-IDF上位語のピアソンの積率相関係数（「人工知能抜き」）")
data = {"TF-DF上位語": ruiji1,"TF-IDF上位語": ruiji2}
print(sim_pearson(data, "TF-DF上位語", "TF-IDF上位語"))
print("8.JiebaとKHCoderのTF-DF上位語のピアソンの積率相関係数（「人工知能抜き」）")
data = {"TF-DF上位語": ruiji1,"TF-DF上位語(KHCoder)": ruiji3}
print(sim_pearson(data, "TF-DF上位語", "TF-DF上位語(KHCoder)"))