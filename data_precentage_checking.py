#BREAKDOWN 1 : PROSENTASE DATA ANTARA START DAN END DATE HARDCODE REV-2

import mysql.connector as sql
import pandas as pd
from datetime import datetime, timedelta

per_hari = 288 #Data yang harus masuk setiap hari (setiap 5 menit sekali)

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

jumlah_hari = int((h_selesai-h_mulai).days)+1
jumlah_data = len(df[(df['dt'] >= h_mulai) & (df['dt'] < (h_selesai + timedelta(days=1)))])
#df2 = df[(df['dt'] >= h_mulai) & (df['dt'] < (h_selesai + timedelta(days=1)))] #Harus dilebihkan satu hari agar hasil sama dengan perhitungan mysql

prosentase = jumlah_data*1.0/(per_hari*jumlah_hari)*100 #Perhitungan prosentase data yang masuk

#print(df2)

print("Hari Mulai\t\t: %s"%datetime.strftime(h_mulai, "%Y-%m-%d"))
print("Hari Selesai\t\t: %s"%datetime.strftime(h_selesai, "%Y-%m-%d"))
print("Jumlah Hari\t\t: %s hari"%jumlah_hari)
print("Data Masuk\t\t: %s data"%jumlah_data)
print("Estimasi Data\t\t: %s data"%(per_hari*jumlah_hari))
print("Prosentase data masuk\t: %.2f %%"%prosentase)

'''
CATATAN
Ada sedikit selisih antara hasil query where clause di sql langsung dan di dataframe pandas
'''