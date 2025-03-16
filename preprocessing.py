from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string
import os
import sys


class DataPreprocessing:
    def __init__(self,filepath,product_name):
        self.__filename=filepath
        self.__product_name=product_name
        

    def preprocessing(self):
        try:
            
           
            dataset = pd.read_csv(self.__filename)
            stemmer = nltk.SnowballStemmer("english")
            wordnet = WordNetLemmatizer()
            stopword = set(nltk.corpus.stopwords.words('english'))

            def clean(text):
                text = str(text).lower()
                text = re.sub('[.*?]', '', text)
                text = re.sub('https?://S+|www.S+', '', text)
                text = re.sub('\+', '', text)  # escape the + symbol
                text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    
    
                text = [word for word in text.split(' ') if word not in stopword]
                text = " ".join(text)
                text = [wordnet.lemmatize(word) for word in text.split(' ')]
                text = " ".join(text)
                return text

            dataset["Reviews"] = dataset["Reviews"].apply(clean)
            os.makedirs('static',exist_ok=True)
            file_path = os.path.join('static',"{}_processed_1.csv".format(self.__product_name))
            dataset.to_csv(file_path,index=False)




        except Exception as e:
            raise CustomException(e,sys)




# if __name__=="__main__":
#     obj=DataPreprocessing('static\iphone5g.csv')
#     obj.preprocessing()








