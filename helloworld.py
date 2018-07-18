import pandas as pd

from flask import *
#from flask import Flask, render_template, flash
#from flask.ext.wtf import Form
#from wtforms import StringField, SubmitField
#from wtforms.validators import DataRequired

import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

from io import BytesIO,StringIO

import mysql.connector as sql

from datetime import datetime, timedelta



DEBUG = True
app = Flask(__name__)
#app.config["SECRET_KEY"] = "secret_key 1"

'''
class MyForm(Form):
 name = StringField(label='Name', validators=[DataRequired()])
 starting = SubmitField(label='Starting')
 ending = SubmitField(label='Ending')
'''

@app.route("/")
def home():
 return render_template("index.html")


#@app.route("/index/", methods=["GET", "POST"])
@app.route("/index/", methods=["POST"])
def index():
 if request.form["options"] == "whole":
  return redirect(url_for("whole"))
 else:
  return home()


@app.route("/whole/")
def whole():
 
 '''@return data_stat is dictionary that describe data_status from selected data
  @var expected is based on asumption that must be 1 data every 5 minutes
 '''
 
 query_ = """SELECT cast(concat(SamplingDate, ' ', SamplingTime) as datetime) as dt, WLevel 
    FROM `dengkeng`
    ORDER BY `dt` ASC"""

 db_connection = sql.connect(host='localhost', database='dengkeng', user='root', password='')
 df = pd.read_sql(query_, con=db_connection, index_col=None)
  
 h_mulai = df["dt"].min()
 h_selesai = df["dt"].max()

 jumlah_hari = int((h_selesai-h_mulai).days)+1

 deviasi = df["WLevel"].std()
 minimal = df["WLevel"].min()
 maksimal = df["WLevel"].max()
 jumlah_data = len(df)
 expected = int(((h_selesai-h_mulai).total_seconds()/60)/5)
 data_stat = {"std":deviasi, "min":minimal, "max":maksimal, "num_record":jumlah_data, "num_record_expected":expected, "sampling_min":h_mulai, "sampling_max":h_selesai}
 return str(data_stat)



if __name__ == "__main__":
 app.run(debug=True)