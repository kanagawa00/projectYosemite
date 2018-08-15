import re
import pandas as pd

#读取文件
fp=open("Comments_for_news6286409.txt","r",encoding="utf-8") 
tmp_read=fp.read()

#定义正则表达
#AA(?=BB) 文字列AAを検索、ただし直後に文字列BBがあるもののみ
#(?<=AA)BB 文字列BBを検索、ただし直前に文字列AAがあるもののみ
#AA(?!BB) 文字列AAを検索、ただし直後に文字列BBが無いもののみ
#.+ 1文字以上の任意の文字列

#最短匹配模式
#你正在试着用正则表达式匹配某个文本模式，但是它找到的是模式的最长可能匹配。 而你想修改它变成查找最短的可能匹配。
#http://python3-cookbook-personal.readthedocs.io/zh_CN/latest/c02/p07_specify_regexp_for_shortest_match.html

#re.S 即为 . 并且包括换行符在内的任意字符（. 不包括换行符）
#http://www.runoob.com/python/python-reg-expressions.html

##############################################
#直接抓取所有评论
#pattern_all=re.compile(r"(?<=日前).+?(?=Y \d{1,4}  N \d{1,4})",re.S)
#comments=pattern_all.findall(tmp_read)
#for cmt in comments:
#    print(cmt)
#    print("▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲")
##############################################

#python 正则 替换 子表达式
#https://segmentfault.com/q/1010000000178361

#只抓母评论（带编号）
#pattern_mother=re.compile(r"(?<=comment).+?(?=Y \d{1,4}  N \d{1,4})",re.S)
#mothers=pattern_mother.findall(tmp_read)
#pattern_mother_clear=re.compile(r"--------------------------.+日前",re.S)
#for mcmt in mothers:
#    mcmt=pattern_mother_clear.sub("",mcmt)
#    print(mcmt)

#只抓母评论（不带编号）
#推荐不带编号：可以写入dataframe时再按写入顺序加编号
#pattern_mother=re.compile(r"(?<=--------------------------).+?(?=Y \d{1,4}  N \d{1,4})",re.S)
#mothers=pattern_mother.findall(tmp_read)
#pattern_mother_clear=re.compile(r".+日前",re.S)
#for mcmt in mothers:
#    mcmt=pattern_mother_clear.sub("",mcmt)
#    #print(mcmt)

#只抓子评论（带编号）
#print("■■■■■■■■■■■■以下子评论预览■■■■■■■■■■■■■")
#pattern_child=re.compile(r"(?<=<<< reply).+?(?=Y \d{1,4}  N \d{1,4})",re.S)
#children=pattern_child.findall(tmp_read)
#pattern_child_clear=re.compile(r">>>.+日前",re.S)
#for ccmt in children:
#    ccmt=pattern_child_clear.sub("",ccmt)
#    num=int(ccmt[1:3])
    #ccmt[1:3]是ccmt里的ID的所在位，int化
#    ccmt=ccmt[4:]
    #ccmt[4:]是ccmt里内容的所在位
    #print(num)
    #print(ccmt)
    #写入dataframe时，如果num不等于1，就代表这条子评论和上一条子评论同属一条母评论
    #用num判断，用ccmt写
    
    
##############################################
#直接抓取所有评论，用0,1表示子母评论
pattern_all=re.compile(r"(?:comment|reply).+?(?=Y \d{1,4}  N \d{1,4})",re.S)
comments=pattern_all.findall(tmp_read)
pattern_all_clear=re.compile(r".+日前",re.S)
num_m=0
num_c=1
cmtlist=[]
for cmt in comments:
    #用cmt[0]="c"或"r"来判断是母评论还是子评论
    if cmt[0]=="c":
        #print("母评论")
        cmt=pattern_all_clear.sub("",cmt)
        cmt=cmt.replace("\n","").replace("\u3000","")
        #print(cmt)
        #csv模块逐行写入时
        cmtlist.append([num_m,cmt])
    else:
        #print("子评论")
        cmt=pattern_all_clear.sub("",cmt)
        cmt=cmt.replace("\n","").replace("\u3000","")
        #print(cmt)
        #print([num_c,cmt])
        cmtlist.append([num_c,cmt])

#用两个list构建dataframe
df = pd.DataFrame(cmtlist,columns=["母(0)/子(1)","评论内容"])
print(df)