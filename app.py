import sys
import os
import webbrowser

from flask import Flask, jsonify, render_template, request ,send_file,redirect, url_for,make_response

import pandas as pd
import chardet
import webview
import Sentiment.Sentiment as sentiment

from PyPDF2 import PdfReader, PdfWriter
from openpyxl import Workbook
from datetime import datetime

import tabula
from tempfile import NamedTemporaryFile
from datetime import datetime
import pandas as pd
import xlsxwriter

import fitz  # PyMuPDF
import camelot



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


from datetime import datetime

@app.route('/split_pdf', methods=['POST'])
def split_pdf():
    pdf_file = request.files['pdf_file']
    pages = request.form['pages']
    
    # Parse the pages input to handle ranges and individual pages
    pages_to_split = []
    for part in pages.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            pages_to_split.extend(range(start, end + 1))
        else:
            pages_to_split.append(int(part))
    
    pdf = PdfReader(pdf_file)
    output_pdf = PdfWriter()

    for page_num in pages_to_split:
        output_pdf.add_page(pdf.pages[page_num - 1])

    # Generate the filename with current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    output_filename = f'extracted_pages_{current_datetime}.pdf'
    output_path = os.path.join(app.root_path, 'static', 'pdf', output_filename)

    with open(output_path, 'wb') as output:
        output_pdf.write(output)

    return redirect(url_for('remaining_pdf', filename=output_filename))




@app.route('/download_xlsx/<filename>')
def download_xlsx(filename):
    pdf_path = os.path.join(app.root_path, 'static', 'pdf', filename)
    
    # Extract tables from the PDF
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream', strip_text='\n', suppress_stdout=True)
    
    # Save each table as a separate sheet in the Excel file
    excel_filename = f"{filename.split('.')[0]}.xlsx"
    excel_path = os.path.join(app.root_path, 'static', 'excel', excel_filename)
    
    with pd.ExcelWriter(excel_path) as writer:
        for i, table in enumerate(tables):
            df = table.df
            df.to_excel(writer, sheet_name=f'Sheet_{i+1}', index=False)
    
    # Return the Excel file for download
    return send_file(excel_path, as_attachment=True)




@app.route('/remaining_pdf/<filename>')
def remaining_pdf(filename):
    return render_template('pdf/remaining_pdf.html', filename=filename)


@app.route('/download_pdf')
def download_pdf():
    return send_file('extracted_pages.pdf', as_attachment=True)



@app.route('/view_pdf_tables/<filename>')
def view_pdf_tables(filename):
    pdf_path = os.path.join(app.root_path, 'static', 'pdf', filename)
    tables = camelot.read_pdf(pdf_path, pages='all', flavor='stream')

    # Render the tables in an HTML template
    return render_template('pdf/view_pdf_tables.html', tables=tables)


@app.route('/view_pdf')
def view_pdf():
    return render_template('pdf/split_PDF.html')


webview.create_window('Flask App', app, resizable=True)


if __name__ == '__main__':
    # Run the app    
    webview.start()
    
    #---- For development ----
    #url = "http://localhost:5000/"
    #webbrowser.open(url)
    #app.run(debug=True)
