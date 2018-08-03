import mysql.connector as sql
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def WholeFunct() :

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
	data_stat = {"dataframe":df, "std":deviasi, "min":minimal, "max":maksimal, "num_record":jumlah_data, "num_record_expected":expected, "sampling_min":h_mulai, "sampling_max":h_selesai}
	
	#creating matplotlib graph and save image
	df.plot.line(x='dt', y='WLevel', figsize=(15,8))
	plt.savefig("flask_dengkeng\static\img\whole.svg")
	plt.clf()

	values = [jumlah_data, (expected-jumlah_data)]
	colors = ["r", "y"]
	labels = ["Data Masuk", "Kekurangan Data"]
	explode = (0.2, 0)
	plt.pie(values, colors=colors, labels=labels, explode=explode, autopct='%1.2f%%', counterclock=False, shadow=True)
	plt.title('Jumlah Data')
	plt.legend(labels,loc=3)
	plt.savefig("flask_dengkeng\static\img\whole_pie.svg")	

	return data_stat


def SpecifiedFunction(mulai, selesai) :

	'''@return data_stat is dictionary that describe data_status from selected data
		@var expected is based on asumption that must be 1 data every 5 minutes
	'''
	h_mulai = mulai
	h_selesai = selesai
	
	query_ = """SELECT cast(concat(SamplingDate, ' ', SamplingTime) as datetime) as dt, WLevel 
				FROM `dengkeng` 
				where cast(concat(SamplingDate, ' ', SamplingTime) as datetime) >= "%s" 
					and cast(concat(SamplingDate, ' ', SamplingTime) as datetime) <= "%s" 
				ORDER BY `dt` ASC """%(h_mulai,h_selesai)

	db_connection = sql.connect(host='localhost', database='dengkeng', user='root', password='')
	df = pd.read_sql(query_, con=db_connection, index_col=None)
		

	jumlah_hari = int((h_selesai-h_mulai).days)+1

	deviasi = df["WLevel"].std()
	minimal = df["WLevel"].min()
	maksimal = df["WLevel"].max()
	jumlah_data = len(df)
	expected = int(((h_selesai-h_mulai).total_seconds()/60)/5)
	data_stat = {"dataframe":df, "std":deviasi, "min":minimal, "max":maksimal, "num_record":jumlah_data, "num_record_expected":expected, "sampling_min":h_mulai, "sampling_max":h_selesai}
	
	#creating matplotlib graph and save image
	df.plot.line(x='dt', y='WLevel', figsize=(15,8))
	plt.savefig("flask_dengkeng\static\img\whole_specified.svg")
	plt.clf()

	values = [jumlah_data, (expected-jumlah_data)]
	colors = ["r", "y"]
	labels = ["Data Masuk", "Kekurangan Data"]
	explode = (0.2, 0)
	plt.pie(values, colors=colors, labels=labels, explode=explode, autopct='%1.2f%%', counterclock=False, shadow=True)
	plt.title('Jumlah Data')
	plt.legend(labels,loc=3)
	plt.savefig("flask_dengkeng\static\img\whole_pie_specified.svg")	

	return data_stat



def DropDataTimeRange(df_, s_date, e_date):
	s_date = datetime.strptime('2012-01-20 09:24:08' , '%Y-%m-%d %H:%M:%S')
	e_date = datetime.strptime('2012-02-09 17:45:03' , '%Y-%m-%d %H:%M:%S')
	df_ = df_[(df_.dt < s_date) | (df_['dt'] > e_date)].reset_index(drop=True)

	h_mulai = df_["dt"].min()
	h_selesai = df_["dt"].max()
	jumlah_hari = int((h_selesai-h_mulai).days)+1

	deviasi = df_["WLevel"].std()
	minimal = df_["WLevel"].min()
	maksimal = df_["WLevel"].max()
	jumlah_data = len(df_)
	expected = int(((h_selesai-h_mulai).total_seconds()/60)/5)
	data_stat = {"s_date":s_date, "e_date":e_date, "dataframe":df_, "std":deviasi, "min":minimal, "max":maksimal, "num_record":jumlah_data, "num_record_expected":expected, "sampling_min":h_mulai, "sampling_max":h_selesai}

	#creating matplotlib graph and save image
	df_.plot.line(x='dt', y='WLevel', figsize=(15,8))
	plt.savefig("flask_dengkeng\static\img\whole_p1.svg")
	plt.clf()

	values = [jumlah_data, (expected-jumlah_data)]
	colors = ["r", "y"]
	labels = ["Data Masuk", "Kekurangan Data"]
	explode = (0.2, 0)
	plt.pie(values, colors=colors, labels=labels, explode=explode, autopct='%1.2f%%', counterclock=False, shadow=True)
	plt.title('Jumlah Data')
	plt.legend(labels,loc=3)
	plt.savefig("flask_dengkeng\static\img\whole_pie_p1.svg")

	return data_stat

def DropDuplicate(df_, keep):
	df_ = df_.drop_duplicates(['dt'], keep=keep) #keep : False, 'first', 'last'
	df_ = df_.reset_index(drop=True)

	h_mulai = df_["dt"].min()
	h_selesai = df_["dt"].max()
	jumlah_hari = int((h_selesai-h_mulai).days)+1

	deviasi = df_["WLevel"].std()
	minimal = df_["WLevel"].min()
	maksimal = df_["WLevel"].max()
	jumlah_data = len(df_)
	expected = int(((h_selesai-h_mulai).total_seconds()/60)/5)
	data_stat = {"dataframe":df_, "std":deviasi, "min":minimal, "max":maksimal, "num_record":jumlah_data, "num_record_expected":expected, "sampling_min":h_mulai, "sampling_max":h_selesai}

	#creating matplotlib graph and save image
	df_.plot.line(x='dt', y='WLevel', figsize=(15,8))
	plt.savefig("flask_dengkeng\static\img\whole_p1.svg")
	plt.clf()

	values = [jumlah_data, (expected-jumlah_data)]
	colors = ["r", "y"]
	labels = ["Data Masuk", "Kekurangan Data"]
	explode = (0.2, 0)
	plt.pie(values, colors=colors, labels=labels, explode=explode, autopct='%1.2f%%', counterclock=False, shadow=True)
	plt.title('Jumlah Data')
	plt.legend(labels,loc=3)
	plt.savefig("flask_dengkeng\static\img\whole_pie_p1.svg")
	
	return data_stat