 
import string
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')
import spacy
##!pip install git+https://github.com/boudinfl/pke.git
##python3 -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")
import pke
from goose3 import Goose
import requests
import json



class KeyExtractor():

    def __init__(self,text):
        self.text=text
        self.num_words=int(len(text)/1000)*30

    def extractorKEYS(self):    
        pos = {'NOUN', 'PROPN', 'ADJ'}
        # 1. create a SingleRank extractor.
        extractor = pke.unsupervised.SingleRank()
        # 2. load the content of the document.
        extractor.load_document(input=self.text)
        # 3. select the longest sequences of nouns and adjectives as candidates.
        extractor.candidate_selection(pos=pos)
        # 4. weight the candidates using the sum of their word's scores that are
        #    computed using random walk. In the graph, nodes are words of
        #    certain part-of-speech (nouns and adjectives) that are connected if
        #    they occur in a window of 10 words.
        extractor.candidate_weighting(window=10,pos=pos)
        # 5. get the 30-highest scored candidates as keyphrases
        keyphrases = extractor.get_n_best(n=self.num_words)
        ##idx = 941
        return keyphrases
        ##1142

##here we scrape the searched url
class scraperWebsite():

    def __init__(self,url):
        self.url=url
        self.g = Goose()
        self.article = self.g.extract(url=url)
    
    def getTitle(self):
        return self.article.title

    def getMetaDesc(self):
        return self.article.meta_description

    def getAlltext(self):
        return self.article.cleaned_text

    def getLinks(self):
        return self.article.links


##here we interact with google search programmable api
class googleAPIinteract():

    def __init__(self,word,number):
        self.word=word
        self.number=number
        self.API_KEY="AIzaSyC9ZVMsS7RX4Temw5ORKoaaHQqw5BGb9RE"
        self.SEARCH_ENGINE_ID="1aeca8730692b98d6"
        self.url="https://www.googleapis.com/customsearch/v1?key="+self.API_KEY+"&cx="+self.SEARCH_ENGINE_ID+"&q="+self.word

    def findPage(self,getURL):
        getData=self.getJsonData()
        getscraper=scraperWebsite(getURL)
        if self.number==1:
            return getscraper.getTitle()
        elif self.number==2:
            return getscraper.getMetaDesc()          
        elif self.number==3:
            return getscraper.getAlltext()
        elif self.number==4:
            return getscraper.getLinks()
        else:
            return "error"
        


    def getJsonData(self):
        self.data = requests.get(self.url)
        dataDict=self.data.json()
        return dataDict

