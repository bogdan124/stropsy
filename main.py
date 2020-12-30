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
        text=request.form["text"]
        get=KeyExtractor(text)
        return jsonify(get.extractorKEYS())
    else:
        return "error"


@app.route("/api/scraper",methods=["POST"])
def apiScraper():
    if request.method=="POST":
        getURL=request.form['word']
        getType=int(request.form['type'])
        data=googleAPIinteract(getURL,getType)
        extract=data.getJsonData()  
        getdata=data.findPage(extract['items'][0]['link'])
        return jsonify(getdata)
    else:
        return "error"


@app.route("/summary/create/<ratio>",methods=["POST"])
def summaryCreate(ratio):
    if request.method=="POST":
        text=request.form["text"]
        text=summarize(text,ratio=ratio)
        return text
    else:
        return "error"


if __name__ == "__main__":
    app.run(host='0.0.0.0')
