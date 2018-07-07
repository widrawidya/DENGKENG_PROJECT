#BREAKDOWN 2 : WHOLE_FUNCTION REV-2

import mysql.connector as sql
import pandas as pd
from datetime import datetime, timedelta

def whole() :

	'''@return data_stat is dictionary that describe data_status from selected data'''
	
	query_ = """SELECT cast(concat(SamplingDate, ' ', SamplingTime) as datetime) as dt, WLevel 
				FROM `dengkeng`
				ORDER BY `dt` ASC"""

	db_connection = sql.connect(host='localhost', database='dengkeng', user='root', password='')
	df = pd.read_sql(query_, con=db_connection, index_col=None)
		
	h_mulai = df["dt"].min()
	h_selesai = df["dt"].max()

	jumlah_hari = int((h_selesai-h_mulai).days)+1
	jumlah_data = len(df)
	#prosentase = jumlah_data/(288*jumlah_hari)*100 #Perhitungan prosentase data yang masuk

	deviasi = df["WLevel"].std()
	minimal = df["WLevel"].min()
	maksimal = df["WLevel"].max()
	jumlah_data = len(df)
	expected = (288*jumlah_hari)
	data_stat = {"std":deviasi, "min":minimal, "max":maksimal, "num_record":jumlah_data, "num_record_expected":expected, "sampling_min":h_mulai, "sampling_max":h_selesai}
	return data_stat


status_data = whole()
print(status_data)

'''
'''