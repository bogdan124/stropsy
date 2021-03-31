 
import string
from nltk.corpus import stopwords
import nltk
##nltk.download('stopwords')
import spacy
##!pip install git+https://github.com/boudinfl/pke.git
##python3 -m spacy download en_core_web_sm
nlp = spacy.load("en_core_web_sm")
import pke
from goose3 import Goose
import requests
import json
import requests
import json
import nltk
# import spacy
import spacy
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint


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

"""
class RequestSearchCertainPartOfText:

    def __init__(self,word):
        self.words=word;
    
    def getDataForWord(self):
        stringRequest="https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch="+self.words+"&format=json"
        r=requests.get(url=stringRequest)
        print(r)
"""


class RequestSearchCertainPartOfText:

    def __init__(self,word):
        self.words=word;
    
    def getDataForWord(self):    
        stringRequest="https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch="+self.words+"&format=json"
        r=requests.get(url=str(stringRequest))
        r=json.loads(r.text)
        print(r['query']['search'][0]['snippet'])
    
    def getWikipediaPage(self):
        pass

    def getWikipediaFirstProp(self): 
        pass

    def extractSmallParagrphData(self):
        text=self.words
        # load english language model
        nlp = spacy.load('en_core_web_sm',disable=['ner','textcat'])
        ##text = "Biochemistry or biological chemistry, is the study of chemical processes within and relating to living organisms.[1] A sub-discipline of both chemistry and biology, biochemistry may be divided into three fields: structural biology, enzymology and metabolism. "
        listToPermit=['PROPN','NOUN','ADJ']##adj trebuie sa aibe o prop si un PROPN sau NOUN pe langa el 
        # create spacy 
        def preprocess(sent):
            sent = nltk.word_tokenize(sent)
            sent = nltk.pos_tag(sent)
            return sent

        doc = preprocess(text)
        ##NN,NNS,NNP,NN
        ##as putea sublinia automat alea de sus sau partile mari din test si daca nu le gasesc pe alea subliniez alte parti


        pattern2=r"""
                ##   Chink: }<VB.?|IN|DT|VBN>{ 
                    Chunk: {<JJ>*<NN.>*<NN.>}    
                    Chink: }<VB.?|IN|DT|VBN|TO>{ 
                    Chunk: {<JJ>*<NN>*<NN>} 
                    Chink: }<VB.?|IN|DT|VBN|TO>{ 
                    Chunk: {<NN>*<NN>} 
                    Chink: }<VB.?|IN|DT|VBN|TO>{ 
                    Chunk: {<NNP>*<NN>*<NN>}
                    Chink: }<VB.?|IN|DT|VBN|TO>{ 
                    Chunk: {<JJ>*<NNP>*<NN>}   
                """
        cp = nltk.RegexpParser(pattern2)
        tree = cp.parse(doc)

        def extract_chunk(tree, chunk='NP'):
            """
            Extract chunk as text from a parsed tree.
            """
            result = []
            for subtree in tree.subtrees():
                if subtree.label() == chunk:
                    words = subtree.leaves()
                    result.append(' '.join([w for w,t in words]))
                    
            return result

        returnData=[]
        spitout=["[","]","%","-","+"]
        for i in extract_chunk(tree,"Chunk"):
            if i not in spitout:
                returnData.append(i)
        return returnData




class RequestServicesFromMultipleAPIcalls():

    def __init__(self,search,api_Id):
        self.search=search
        self.api_Id=api_Id

    def callApiListYotube(self):
        response = requests.get("https://www.googleapis.com/youtube/v3/search?q="+self.search+"&key=AIzaSyC9ZVMsS7RX4Temw5ORKoaaHQqw5BGb9RE")
        getData=response.json()
        return getData

    def callApiVideoYoutube(self):
        response = requests.get("https://www.googleapis.com/youtube/v3/videos?id=" + text + "&key=AIzaSyC9ZVMsS7RX4Temw5ORKoaaHQqw5BGb9RE&part=snippet,contentDetails,statistics")
        getData=response.json()
        return getData



    def getDataAPIcall(self):
        if self.api_Id==1:
            return self.callApiListYotube()
        elif self.api_Id==2:
            return self.callApiVideoYoutube()
        else:
            return None