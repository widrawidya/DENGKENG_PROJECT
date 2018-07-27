from flask import Flask, render_template, url_for, jsonify
from datetime import datetime, timedelta
from flask_dengkeng import app
from flask_dengkeng.modules import WholeFunct, SpecifiedFunction
from flask_dengkeng.forms import DatePicker

import os


#content
posts = [
	{
		'author': 'Corey Schafer',
		'title': 'Blog Post 1',
		'content': 'First post content',
		'date_posted': 'April 20, 2018'
	},
	{
		'author': 'Jane Doe',
		'title': 'Blog Post 2',
		'content': 'Second post content',
		'date_posted': 'April 21, 2018'
	}
]


#Utama
@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts, title='Home')


@app.route("/about")
def about():
	return render_template('about.html', title='About')


@app.route("/view")
def view():
	return render_template('view.html', title='View')


@app.route("/anomali")
def anomali():
	return render_template('anomali.html', title='Anomali')


@app.route("/perbaikan")
def perbaikan():
	return render_template('perbaikan.html', title='Perbaikan')	


#Fungsional
@app.route("/view/whole")
def whole():
	data = WholeFunct()
	return render_template('whole.html', data=data, title='whole')


@app.route("/view/specified", methods=['GET', 'POST'])
def specified():	
	form = DatePicker() 
	data = ""
	if form.validate_on_submit():
		#dumps(datetime.now(), default=json_serial)
		mulai = datetime.strptime((form.dt_mulai.data.strftime('%Y-%m-%d')), "%Y-%m-%d")
		selesai = datetime.strptime((form.dt_selesai.data.strftime('%Y-%m-%d')), "%Y-%m-%d")
		#mulai = form.dt_mulai.data.strftime('%Y-%m-%d')
		#selesai = form.dt_selesai.data.strftime('%Y-%m-%d')
		data = SpecifiedFunction(mulai, selesai)
	return render_template('specified.html', data=data, title='whole', form=form)



if __name__ == '__main__':
	app.run(debug=True)