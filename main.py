from flask import Flask,jsonify,request
from api import KeyExtractor, scraperWebsite, googleAPIinteract
import gensim
from gensim.summarization import keywords
from gensim.summarization.summarizer import summarize
import json
from nltk.stem.lancaster import LancasterStemmer
from bs4 import BeautifulSoup
import re
import nltk
from nltk.corpus import stopwords
import requests

##https://medium.com/thecyphy/generating-abstractive-summaries-using-googles-pegasus-model-18eef8ae985b
app = Flask(__name__)

@app.route("/api/keywords",methods=["POST"])
def apiKeywords():
        data1=request.get_json()
        text=data1["text"]
        get=KeyExtractor(text)
        return jsonify(get.extractorKEYS())


@app.route("/api/scraper",methods=["POST"])
def apiScraper():
        data1=request.get_json()
        getURL=data1['word']
        getType=int(data1['type'])
        data=googleAPIinteract(getURL,getType)
        extract=data.getJsonData()  
        ##print(extract)
        ##getdata=data.findPage(extract['items'][0]['snippet'])
        return jsonify(extract)

@app.route("/api/rewrite",methods=['POST'])
def rewrite():
        ##test
        ##https://en.wikipedia.org/wiki/Gene_delivery
        ##https://en.wikipedia.org/wiki/Biochemistry
        ##bad 
        ##https://en.wikipedia.org/wiki/Football_in_England

        data1=request.get_json()
        ##text1=data1["text"]
        addReturn=[]
        bodyText=data1["bodyText"]
        soup = BeautifulSoup(bodyText, "html.parser")
        bodyText = soup.get_text()
        get=KeyExtractor(bodyText)
        keys=get.extractorKEYS()
        f=open("static/data.txt","r")
        text=f.readlines()
        text=str(text)
        a=[]
        sum=""
        for i in text:
           if i!=',':
             sum=sum+i
           else:
             for j in sum[1:-1].split(" "):                   
                a.append(j)
                sum=""
        ##st = LancasterStemmer()
        ##b=[]
        ##for i in a:
        ##   b.append(st.stem(i))
        keySec=[]
        sa=0
        ##for i in a:
        ##   print(i)
        b=[]
        stpWords=stopwords.words('english')
        stpWords.append("ro")
        stpWords.append("la")
        stpWords.append("li")
        stpWords.append("de")
        stpWords.append("ea")
        for i in a:
           if i not in stpWords:
                b.append(i)
        a=b
        for j in keys:
           for il in a:     
                
              if il in j[0] :
                 ##print(il,j[0])
                 for z in keySec:
                    if j[0]==z[0] :
                      sa=1
                      break
                 if sa==0:
                      keySec.append([j[0],j[1]])
                 else:
                      sa=0
        ##print(keys,keySec)
        keys=keySec
        

        if len(keys)>2000:
                return jsonify(keys[:2000])
        else:
                return jsonify(keys)

@app.route("/api/summary",methods=["POST"])
def summaryCreate():
        data1=request.get_json()
        text=data1["text"]
        ratio=float(data1["ratio"]/100)
        text=summarize(str(text),ratio=ratio)
        return text

@app.route("/api/videos",methods=["POST","GET"])
def videos():
        data1=request.get_json()
        text=data1["search"]
        response = requests.get("https://www.googleapis.com/youtube/v3/search?q="+text+"&key=AIzaSyC9ZVMsS7RX4Temw5ORKoaaHQqw5BGb9RE")
        return response.json()

if __name__ == "__main__":
    app.run(host='0.0.0.0')

'''
        for text1 in data1["text"]:
                ##print(text1)
                add=0
                save=text1
                ##print(keys)
                saveKeys=[]
                for i in range(0,len(keys)):
                        if keys[i][0] in save.lower():
                                ##print(text1[int(text1.lower().find(i[0])):int(text1.lower().find(i[0])+len(i[0]))],i[0])
                                add+=1
                                save=save.replace(str(save[int(save.lower().find(keys[i][0])):int(save.lower().find(keys[i][0])+len(keys[i][0]))]),
                                "<span class='tooltip detect-text' data-id-get='#text-tooltip-"+str(add)+"' >"+
                                save[int(save.lower().find(keys[i][0])):int(save.lower().find(keys[i][0])+len(keys[i][0]))]+
                                " <span class='tooltiptext add-text-desc' id='text-tooltip-"+str(add)+"'>"
                                +save[int(save.lower().find(keys[i][0])):int(save.lower().find(keys[i][0])+len(keys[i][0]))]+"</span></span>",1)
                                saveKeys.append(i)
                ##print(saveKeys,keys)
                ##for i in saveKeys:
                ##        print(i+"sdfs")
                ##        keys.pop(i)
                        
                addReturn.append(save)
                save=""
                ##print(addReturn)
'''