from flask import Flask,jsonify,request
from api import KeyExtractor, scraperWebsite, googleAPIinteract
import gensim
from gensim.summarization.summarizer import summarize
import json

##https://medium.com/thecyphy/generating-abstractive-summaries-using-googles-pegasus-model-18eef8ae985b
app = Flask(__name__)

@app.route("/api/keywords",methods=["POST"])
def apiKeywords():
    if request.method=="POST":
        data1=request.get_json()
        text=data1["text"]
        get=KeyExtractor(text)
        return jsonify(get.extractorKEYS())
    else:
        return "error"


@app.route("/api/scraper",methods=["POST"])
def apiScraper():
    if request.method=="POST":
        data1=request.get_json()
        getURL=data1['word']
        getType=int(data1['type'])
        data=googleAPIinteract(getURL,getType)
        extract=data.getJsonData()  
        getdata=data.findPage(extract['items'][0]['link'])
        return jsonify(getdata)
    else:
        return "error"


@app.route("/api/create/<ratio>",methods=["POST"])
def summaryCreate(ratio):
    if request.method=="POST":
        data1=request.get_json()
        text=data1["text"]
        text=summarize(text,ratio=ratio)
        return text
    else:
        return "error"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
