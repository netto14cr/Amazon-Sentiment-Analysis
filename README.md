# Amazon-Sentiment-Analysis

## Description

This Python application is a Flask-based desktop app that performs sentiment analysis on Amazon reviews, reads and displays data from CSV and Excel files, and provides a user interface through a webview window. The sentiment analysis and data reading are done through specific endpoints, and the results are displayed in the webview window.


## Functionalities

This Python application is a Flask web application that provides several functionalities:

* Home Page (/): The home page of the application, which renders the main/index.html template.

* Sentiment Analysis (/sentiment): This page renders the sentiment/review.html template. It's designed to perform sentiment analysis on Amazon reviews.

* Get Comments (/get_comments): This endpoint reads a CSV file named 'Amazon Reviews.csv', performs sentiment analysis on the reviews in the file, and returns the results as a JSON object.

* Read CSV (/read_csv): This endpoint reads a CSV file named 'Employee Sample Data.csv', and renders a template (csv/csv_table.html) with the data from the CSV file.

* Read Excel (/read_excel): This endpoint reads an Excel file named 'Employee Sample Data.xlsx', replaces 'NaT' values in the 'Exit Date' column with 'Active', and renders a template (excel/excel_table.html) with the data from the Excel file.

## Installation

Before installing the project, it's recommended to create a virtual environment to isolate the project dependencies. Here's how you can do it:

```bash
# Create a virtual environment
python -m venv env

# Activate the virtual environment
# On Windows, use:
env\Scripts\activate

# On Unix or MacOS, use:
source env/bin/activate

## Usage

After installing the project, you can run it in one of the following ways:

1. Run the Python script directly:

'''bash console
    python app.py

2. If you have the distribution version of the application, you can run the executable file app.exe located in the dist directory. Simply double-click the file to run the application.
