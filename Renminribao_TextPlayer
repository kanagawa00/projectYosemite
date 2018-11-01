import os,re

class News():
    def __init__(self,read):
        try:
            self.ttl=re.search(r"(?<=<title>).+(?=</title>)",read).group()
            self.ctt=re.sub(r"<title>.+</title>\n","",read)
            self.khcoder="<h1>"+self.ttl+"</h1>\n"+self.ctt
        except:
            self.ttl,self.ctt,self.khcoder="","",""
        
    def __str__(self):
        output_for_python=self.ttl+"\n"+self.ctt
        return output_for_python

path ="Desktop/Renminribao"
files= os.listdir(path)

fopen=open("Desktop/MasterKhcoder/renminribao_text.txt","w",encoding="utf-8")

for file in files:
    if not os.path.isdir(file):
        fr=open(path+"/"+file,"r",encoding="utf-8")
        fn=News(fr.read())
        fr.close()
        fopen.write(fn.khcoder)

fopen.close()
print("Done")
        
        
    
