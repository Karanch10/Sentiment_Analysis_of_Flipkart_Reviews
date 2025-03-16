from src.exception import CustomException
from src.logger import logging
from src.components.data_ingestion import DataIngestion
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import numpy as np
import nltk
import os
import sys

class SentimentPredictions:
    def __init__(self,filename,product_name):
       self.__filename=filename
       self.__product_name=product_name

    def predictions(self):
        try:
            sentiments = SentimentIntensityAnalyzer()
            dataset=pd.DataFrame()
            dataset=pd.read_csv(self.__filename)
            dataset["Positive"] = [sentiments.polarity_scores(i)["pos"] for i in dataset    ["Reviews"]]
            dataset["Negative"] = [sentiments.polarity_scores(i)["neg"] for i in dataset    ["Reviews"]]
            dataset["Neutral"] = [sentiments.polarity_scores(i)["neu"] for i in dataset ["Reviews"]]

            def get_sentiment(text):
              sentiment = sentiments.polarity_scores(text)
              if sentiment['compound'] > 0:
                return 'positive'
              elif sentiment['compound'] < 0:
                return 'negative'
              else:
                return 'neutral'

            List_sentiments = []
            for summary in dataset['Reviews']:
                if isinstance(summary, str):
                    sentiment = get_sentiment(summary)
                else:
                    sentiment = 'missing'
                List_sentiments.append(sentiment)

            sentiment_df = pd.DataFrame({'Summary': dataset['Reviews'], 'NewSentiment':         List_sentiments})


            dataset['New sentiments'] = sentiment_df['NewSentiment']
            dataset = dataset[["Reviews", "Positive", "Negative","Neutral",'New sentiments']]
            os.makedirs('static',exist_ok=True)
            file_path = os.path.join('static',"{}Sentiment.csv".format(self.__product_name))
            dataset.to_csv(file_path,index=False)

            x = sum(dataset["Positive"])
            y = sum(dataset["Negative"])
            z = sum(dataset["Neutral"])
            def sentiment_score(a, b, c):
                if (a>b) and (a>c):
                    print("Positive 😊😊😊 ")
                elif (b>a) and (b>c):
                    print("Negative 😠😠😠 ")
                else:
                    print("Neutral 🙂 ")
            sentiment_score(x, y, z)
            # X = dataset[[dataset['New sentiments']=="positive" ]].shape[0]
            # Y = dataset[[dataset['New sentiments']=="neutral" ]].shape[0]
            # Z = dataset[[dataset['New sentiments']=="negative" ]].shape[0]
            
            X = dataset[dataset['New sentiments']=="positive" ].shape[0]
            Y = dataset[dataset['New sentiments']=="neutral" ].shape[0]
            Z = dataset[dataset['New sentiments']=="negative" ].shape[0]
            total = X+Y+Z
            per_X = round(X/total,2)
            per_Y = round(Y/total,2)
            per_Z =round(Z/total,2)
               
               
            print("Positive score:",x)
            print("Negative score:",y)
            print("Neutral score:",z)
            return (per_X*100,per_Y*100,per_Z*100)

        except Exception as e:
            raise CustomException(e,sys)


# if __name__=="__main__":
#    obj=SentimentPredictions('static\processed_1.csv')
#    obj.predictions()
   
   