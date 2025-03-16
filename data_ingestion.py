import os
import sys 
from src.exception import CustomException
from src.logger import logging
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import concurrent.futures


class DataIngestion:
    def __init__(self,flipkart_product_name):
        self.__name=flipkart_product_name
        

    def initiate_data_ingestion(self):
        try:
            name=str(self.__name)

            BaseSearchURL = "https://www.flipkart.com/search?q="

            def SearchPageURL(product_name):
                W = product_name
                arrayinput = W.split()
                print(arrayinput)
                SearchpageURL = BaseSearchURL
                for i in arrayinput:
                    j = 0
                    if j == 0:
                        SearchpageURL = SearchpageURL + i
                    else:
                        SearchpageURL = SearchpageURL + i
                    j = j + 1
                return SearchpageURL

            def scrape_product_reviews(product_url, headers, visited_reviews):
                Reviews = []
                Rating = []

                pn = 1

                while pn <= 5:
                    get_finalUrl = product_url + str(pn)
                    product_req = requests.get(get_finalUrl, headers=headers)

                    if product_req.status_code != 200:
                        break

                    product_html = bs(product_req.text, 'html.parser')
                    product_ratings = product_html.find_all("div", {"class": "_3LWZlK _1BLPMq"})
                    product_reviews = product_html.find_all("div", {"class": "t-ZTKy"})

                    if len(product_ratings) == len(product_reviews) and len(product_ratings) > 0:
                        for k, z in zip(product_reviews, product_ratings):
                            review_text = k.text.strip().replace('READ MORE', '')
                
                            # Check if the review is unique
                            if review_text not in visited_reviews:
                                visited_reviews.add(review_text)
                                Reviews.append(review_text)
                                Rating.append(int((z.text)[:1]))

                    pn = pn + 1

                return Reviews, Rating

            Url = SearchPageURL(name)
            finalUrl = Url
            
            headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Accept-Language': 'en-GB,en;q=0.5',
    'Dnt': '1',
    'Referer': 'https://google.com'
            }

            req = requests.get(finalUrl, headers=headers)
            print(req.status_code)
            print(finalUrl)

            BaseUrl = 'https://www.flipkart.com'
            soup = bs(req.content, 'html.parser')
            Links = soup.findAll("a", {"class": "_1fQZEK"})

            Reviews = []
            Rating = []

            visited_product_reviews = set()  # Store visited product reviews to avoid duplicates

            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []
                for i in Links:
                    product_url = (BaseUrl + i.get('href').strip()).replace('/p/', '/product-reviews/')
                    product_url = product_url + '&page='
                    futures.append(executor.submit(scrape_product_reviews, product_url, headers, visited_product_reviews))

                for future in concurrent.futures.as_completed(futures):
                    result_reviews, result_ratings = future.result()
                    Reviews.extend(result_reviews)
                    Rating.extend(result_ratings)

            data = {"Reviews": Reviews, "Rating": Rating}
            df = pd.DataFrame(data)
            name=name.replace(' ','')
            os.makedirs('static',exist_ok=True)
            file_path = os.path.join('static',"{}.csv".format(name))
            df.to_csv(file_path,index=False)

            



            
        except Exception as e:
            raise CustomException(e,sys)
        


# if __name__=="__main__":
#     obj=DataIngestion("iphone 5g")
#     obj.initiate_data_ingestion()        