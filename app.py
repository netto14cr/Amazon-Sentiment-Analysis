import sys
import os
import webbrowser
from flask import Flask, jsonify, render_template
import pandas as pd
import chardet
import webview
import Sentiment.Sentiment as sentiment


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main/index.html')

@app.route('/sentiment')
def sentiment_analysis():
    # Render the template witout waiting for the comments
    return render_template('sentiment/review.html')

@app.route('/get_comments')
def get_comments():
    # Name of the file to read
    csv_name = 'Amazon Reviews.csv'
    
    # Get the path to the CSV file
    csv_file = os.path.join(app.root_path, 'static', "files/"+csv_name)

    # Create a Sentiment object
    s = sentiment.Sentiment(csv_file)

    # Get all the products in the dataset
    all_reviews = s.data['review'].tolist()

    # Analyze the reviews and store the results in a list
    analyzed_reviews = [(comment, analysis) for comment, analysis in [(str(comment), s.analyze(str(comment))) for comment in all_reviews]]
    
    # Devolver los comentarios como un objeto JSON
    return jsonify(analyzed_reviews)

@app.route('/read_csv')
def read_csv():
    # Name of the file to read
    csv_employee = 'Employee Sample Data.csv'
    # Get the path to the CSV file
    csv_employee_file = os.path.join(app.root_path, 'static', "files/"+csv_employee)
    
    # Read the CSV file
    with open(csv_employee_file, 'rb') as f:
        result = chardet.detect(f.read())
        f.seek(0)  # Reset the file pointer to the beginning
        data = pd.read_csv(f, encoding=result['encoding'])

    # Replace 'NaT' in 'Exit Date' with 'Active'
    return render_template('csv/csv_table.html', data=data.to_dict(orient='records'))

@app.route('/read_excel')
def read_excel():
    
    # Name of the file to read
    excel_employee = 'Employee Sample Data.xlsx'
    # Get the path to the Excel file
    excel_employee_file = os.path.join(app.root_path, 'static', "files/"+excel_employee)
    # Read the Excel file
    data = pd.read_excel(excel_employee_file)
    
    # Replace 'NaT' in 'Exit Date' with 'Active'
    data['Exit Date'] = data['Exit Date'].fillna('Active')
    
    # Render the template with the data from the Excel file
    return render_template('excel/excel_table.html', data=data.to_dict(orient='records'))



webview.create_window('Flask App', app, resizable=True)


if __name__ == '__main__':
    # Run the app    
    webview.start()

