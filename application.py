from flask import Flask, render_template, request
import seaborn as sns
import matplotlib.pyplot as plt
import os
from src.components.data_ingestion import DataIngestion
from src.components.preprocessing import DataPreprocessing
from src.components.prediction import SentimentPredictions
from waitress import serve

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Review', methods=['GET', 'POST'])
def register():
    product_name = ''
    X = Y = Z = None
    image_path=''
    if request.method == 'POST' and 'product_name' in request.form:
        product_name = request.form['product_name']
        product_name=product_name.replace(' ','')
        obj=DataIngestion(product_name)
        obj.initiate_data_ingestion() 
        obj1=DataPreprocessing('static\{}.csv'.format(product_name),product_name)
        obj1.preprocessing()
        obj2=SentimentPredictions('static\{}_processed_1.csv'.format(product_name),product_name)
        X,Y,Z = obj2.predictions()
        labels = ['Positive', 'Neutral', 'Negative']
        sizes = [X, Y, Z]  # Example sizes for the pie chart

        # Create a pie plot using Seaborn
        plt.figure(figsize=(6, 6))
        sns.set_style("darkgrid", {"axes.facecolor": "#f0f0f0"})
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis('equal') 
        # plt.axis().set_facecolor('blue')
        os.makedirs('static',exist_ok=True)
        image_path = os.path.join('static','pie_chart{}.png'.format(product_name))
        print(image_path)
        plt.savefig(image_path, bbox_inches='tight')
        
       
    return render_template('Review.html', product_name=product_name)


if __name__ == '__main__':
    app.run(debug=True)
# serve(app, host='0.0.0.0', port=5000)

