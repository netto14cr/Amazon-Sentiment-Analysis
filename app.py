# -*- coding: utf-8 -*-
import os
from flask import Flask, jsonify, render_template
import Sentiment.Sentiment as sentiment
import pandas as pd

app = Flask(__name__)



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sentiment')
def sentiment_analysis():
    # Renderizar la plantilla sin los comentarios
    return render_template('review.html')

@app.route('/get_comments')
def get_comments():
    # Name of the file to read
    csv_name = 'amazon_reviews.csv'
    
    # Get the path to the CSV file
    csv_file = os.path.join(app.root_path, 'static', csv_name)

    # Create a Sentiment object
    s = sentiment.Sentiment(csv_file)

    # Get all the products in the dataset
    all_reviews = s.data['review'].tolist()

    # Analyze the reviews and store the results in a list
    analyzed_reviews = [(comment, analysis) for comment, analysis in [(str(comment), s.analyze(str(comment))) for comment in all_reviews]]
    
    # Devolver los comentarios como un objeto JSON
    return jsonify(analyzed_reviews)



if __name__ == '__main__':
    app.run(debug=True)
