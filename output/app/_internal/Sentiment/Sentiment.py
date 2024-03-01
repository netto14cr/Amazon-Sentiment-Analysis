import pandas as pd
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk import pos_tag

class Sentiment:
    def __init__(self, csv_file):
        self.stop_words = set(stopwords.words('english'))
        self.cache = {}
        self.data = pd.read_csv(csv_file)

    def analyze(self, text):
        if text in self.cache:
            return self.cache[text]
        blob = TextBlob(text, analyzer=NaiveBayesAnalyzer())
        sentiment_score = blob.sentiment.p_pos - blob.sentiment.p_neg
        keywords = self.extract_keywords(text)
        result = {'sentiment_score': sentiment_score, 'keywords': keywords}
        self.cache[text] = result
        return result


    def extract_keywords(self, text):
        tokens = word_tokenize(text)
        tokens = [word.lower() for word in tokens if word.isalpha()]
        tokens = [word for word in tokens if word not in self.stop_words]
        tagged = pos_tag(tokens)
        keywords = [word for word, tag in tagged if tag.startswith('NN')]
        return list(set(keywords))

    
    def get_reviews(self,product_name):
        # Obtener los comentarios para el producto dado
        reviews = self.data[self.data['name'] == product_name]['review'].tolist()
        return reviews

    def get_rating(self, product_name):
        rating = self.data[self.data['name'] == product_name]['rating'].mean()
        return rating
