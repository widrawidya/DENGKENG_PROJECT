#BREAKDOWN 1 : PROSENTASE DATA ANTARA START DAN END DATE HARDCODE REV-1

import mysql.connector as sql
import pandas as pd
from datetime import datetime

per_hari = 288 #Data yang harus masuk setiap hari (setiap 5 menit sekali)
daysOfMonths = [ 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def isLeapYear(year): #Perhitungan Tahun Kabisat (sumber wikipedia)
 return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0


def Count_Days(year1, month1, day1):
 if month1 ==2:
  if isLeapYear(year1):
   if day1 < daysOfMonths[month1-1]+1:
    return year1, month1, day1+1
   else:
    if month1 ==12:
     return year1+1,1,1
    else:
     return year1, month1 +1 , 1
  else: 
   if day1 < daysOfMonths[month1-1]:
    return year1, month1, day1+1
   else:
    if month1 ==12:
     return year1+1,1,1
    else:
     return year1, month1 +1 , 1
 else:
  if day1 < daysOfMonths[month1-1]:
    return year1, month1, day1+1
  else:
   if month1 ==12:
    return year1+1,1,1
   else:
     return year1, month1 +1 , 1


def daysBetweenDates(y1, m1, d1, y2, m2, d2,end_day):
 if y1 > y2:
  m1,m2 = m2,m1
  y1,y2 = y2,y1
  d1,d2 = d2,d1
 days=0
 while(not(m1==m2 and y1==y2 and d1==d2)):
  y1,m1,d1 = Count_Days(y1,m1,d1)
  days+=1
 if end_day:
  days+=1
 return days


h_mulai = datetime.strptime("2017-01-23", "%Y-%m-%d") #Hari mulai perhitungan
h_selesai = datetime.strptime("2017-02-23", "%Y-%m-%d") #Hari selesai perhitungan

query_ = """SELECT cast(concat(SamplingDate, ' ', SamplingTime) as datetime) as dt, WLevel 
   FROM `dengkeng`
   WHERE `SamplingDate` >= "%s" AND `SamplingDate` <= "%s" 
   ORDER BY `dengkeng`.`SamplingDate` ASC"""%(h_mulai,h_selesai)

db_connection = sql.connect(host='localhost', database='dengkeng', user='root', password='')
db_cursor = db_connection.cursor()
db_cursor.execute(query_)
table_rows = db_cursor.fetchall()
df = pd.DataFrame(table_rows)

jumlah_hari = daysBetweenDates(h_mulai.year, h_mulai.month, h_mulai.day, h_selesai.year, h_selesai.month, h_selesai.day, True) #h_mulai harus < h_selesai, True = hitung selisih +1, false hitung selisih saja
prosentase = (len(df)*1.0)/(per_hari*jumlah_hari)*100 #Perhitungan prosentase data yang masuk

print(df)
print("Hari Mulai\t\t: %s"%datetime.strftime(h_mulai, "%Y-%m-%d"))
print("Hari Selesai\t\t: %s"%datetime.strftime(h_selesai, "%Y-%m-%d"))
print("Jumlah Hari\t\t: %s hari"%jumlah_hari)
print("Prosentase data masuk\t: %s"%prosentase)

'''
CATATAN
Data yang ada di dalam Dataframe dan select query masih sama 
'''