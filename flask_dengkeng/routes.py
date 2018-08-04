from flask import Flask, render_template, url_for, jsonify
from datetime import datetime, timedelta
from flask_dengkeng import app
from flask_dengkeng.modules import WholeFunct, SpecifiedFunction, DropDataTimeRange, DropDuplicate
from flask_dengkeng.forms import DatePicker, DatePickerSpecified, DropSubmit

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
data_p1=[]


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
	return render_template('perbaikan.html', title='Perbaikan Data')	
	

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
		mulai = datetime.strptime((form.dt_mulai.data.strftime('%Y-%m-%d')), "%Y-%m-%d")
		selesai = datetime.strptime((form.dt_selesai.data.strftime('%Y-%m-%d')), "%Y-%m-%d")
		data = SpecifiedFunction(mulai, selesai)
	return render_template('specified.html', data=data, title='whole', form=form)


@app.route("/perbaikan/whole", methods=['GET', 'POST'])
def p_whole():
	global data_p1
	form_p1 = DatePickerSpecified()
	form_p2 = DropSubmit()
	data = WholeFunct()
	data_p1.append(data.copy())
	data_p2 = False
	if form_p1.validate_on_submit():
		min_dt = datetime.strptime((form_p1.start_dt.data.strftime('%Y-%m-%d %H:%M:%S')) , '%Y-%m-%d %H:%M:%S')
		max_dt = datetime.strptime((form_p1.start_dt.data.strftime('%Y-%m-%d %H:%M:%S')) , '%Y-%m-%d %H:%M:%S')
		data_p1.append(DropDataTimeRange(data_p1[-1]['dataframe'], min_dt, max_dt))
		data_p2 = True
		return render_template('p_whole.html', data=data, data_p1=data_p1[-1], data_p2=data_p2, title='Hasil pil 1', form_p1=form_p1, form_p2=form_p2)

	if form_p2.validate_on_submit():
		keep = form_p2.keep.data
		data_p1.append(DropDuplicate(data_p1[-1]['dataframe'], keep))
		data_p2 = True
		return render_template('p_whole.html', data=data, data_p1=data_p1[-1], data_p2=data_p2, title='Hasil pil 2', form_p1=form_p1, form_p2=form_p2)

	return render_template('p_whole.html', data=data, data_p1=data_p1, data_p2=data_p2, title='Perbaikan Keseluruhan data', form_p1=form_p1, form_p2=form_p2)


if __name__ == '__main__':
	app.run(debug=True)