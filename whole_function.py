#BREAKDOWN 2 : WHOLE_FUNCTION REV-1

import mysql.connector as sql
import pandas as pd
from datetime import datetime, timedelta

h_mulai = datetime.strptime("2017-01-24", "%Y-%m-%d") #Hari mulai perhitungan
h_selesai = datetime.strptime("2017-01-25", "%Y-%m-%d") #Hari selesai perhitungan

query_ = """SELECT cast(concat(SamplingDate, ' ', SamplingTime) as datetime) as dt, WLevel 
   FROM `dengkeng`
   ORDER BY `dt` ASC"""

db_connection = sql.connect(host='localhost', database='dengkeng', user='root', password='')
db_cursor = db_connection.cursor()
db_cursor.execute(query_)
table_rows = db_cursor.fetchall()

df = pd.read_sql(query_, con=db_connection, index_col=None)

'''
#OPSI 1 - membuat dataframe baru sesuai where clause (sedikit boros memory)
def whole(df,h_mulai,h_selesai) :
	df2 = df[(df['dt'] >= h_mulai) & (df['dt'] < (h_selesai + timedelta(days=1)))] #Harus dilebihkan satu hari agar hasil sama dengan perhitungan mysql
	
	jumlah_hari = int((h_selesai-h_mulai).days)+1
	jumlah_data = len(df2)
	#prosentase = jumlah_data/(288*jumlah_hari)*100 #Perhitungan prosentase data yang masuk

	deviasi = df2["WLevel"].std()
	minimal = df2["WLevel"].min()
	maksimal = df2["WLevel"].max()
	jumlah_data = len(df[(df['dt'] >= h_mulai) & (df['dt'] < (h_selesai + timedelta(days=1)))])
	expected = (288*jumlah_hari)
	data_stat = {"std":deviasi, "min":minimal, "max":maksimal, "num_record":jumlah_data, "num_record_expected":expected, "sampling_min":h_mulai, "sampling_max":h_selesai}
	return data_stat
'''

#OPSI 2 - tanpa membuat dataframe baru (sedikit boros script, sulit memahami ulang script)
def whole(df,h_mulai,h_selesai) :
 '''
 @param df is dataframe object from mysql table that declared before
 @param h_mulai is date object that declared before
 @param h_selesai is date object that declared before
 @return data_stat is dictionary that describe data_status from selected data
 '''
	jumlah_hari = int((h_selesai-h_mulai).days)+1
	jumlah_data = len(df[(df['dt'] >= h_mulai) & (df['dt'] < (h_selesai + timedelta(days=1)))])
	#prosentase = jumlah_data/(288*jumlah_hari)*100 #Perhitungan prosentase data yang masuk

	deviasi = df[(df['dt'] >= h_mulai) & (df['dt'] < (h_selesai + timedelta(days=1)))]["WLevel"].std()
	minimal = df[(df['dt'] >= h_mulai) & (df['dt'] < (h_selesai + timedelta(days=1)))]["WLevel"].min()
	maksimal = df[(df['dt'] >= h_mulai) & (df['dt'] < (h_selesai + timedelta(days=1)))]["WLevel"].max()
	jumlah_data = len(df[(df['dt'] >= h_mulai) & (df['dt'] < (h_selesai + timedelta(days=1)))])
	expected = (288*jumlah_hari)
	data_stat = {"std":deviasi, "min":minimal, "max":maksimal, "num_record":jumlah_data, "num_record_expected":expected, "sampling_min":h_mulai, "sampling_max":h_selesai}
	return data_stat


status_data = whole(df,h_mulai,h_selesai)
print(status_data)

'''
'''