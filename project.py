from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import pandas as pd
from sqlalchemy import create_engine

import sqlalchemy

app = Flask(__name__)
app.config["DEBUG"] = True

app.config['UPLOAD_EXTENSIONS'] = ['.csv']
UPLOAD_FOLDER = 'static/csv'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])

def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(file_path)
        Data =  pd.read_csv(file_path)
    return redirect(url_for('index'))

Data =  pd.read_csv('static/csv/Backtesting.csv')

engine = sqlalchemy.create_engine("oracle+cx_oracle://demopython:amira123@localhost/?service_name=xepdb1", arraysize=1000)
Data.to_sql('data', con = engine, if_exists = 'append', chunksize = 1000,index=False)
print("Record inserted successfully")

conn = engine.connect()
dat = conn.execute("SELECT * FROM data")
irisdf = pd.DataFrame(dat.fetchall())
irisdf.columns = dat.keys()
print(irisdf.columns)

# print(irisdf.head())
conn.close()

if __name__ == '__main__':
    app.run(debug=True)
