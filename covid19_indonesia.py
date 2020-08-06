import json
import re
import pandas as pd
import matplotlib.pyplot as plt
#df = pd.read_json("https://data.covid19.go.id/public/api/update.json")
with open(r'C:\Users\Lenovo\Desktop\cov19.json') as f:
    data_json = json.loads(f.read())
#print(data_json["update"])
df=pd.DataFrame(data_json)
#Dict data penambahan kasus COVID19
penambahan = df["update"].iloc[5]

#Dict data total kasus COVID19
total = df["update"].iloc[7]

#Dict data harian kasus COVID19
harian = df["update"].iloc[6]

#Ubah dict data harian menjadi dataframe
dataharian = pd.DataFrame.from_dict(harian)
print(dataharian.columns)#Cetak daftar kolom
dataharian = dataharian[["key_as_string","jumlah_meninggal", "jumlah_sembuh", "jumlah_positif", "jumlah_dirawat"]]

#Data n hari terakhir
n = 10
dataharian_n = dataharian.iloc[157-n:157]
#Note: jumlah_meninggal + jumlah_sembuh + jumlah_dirawat = jumlah_positif
#Ada tiga kemungkinan yang dapat terjadi pada orang yang positif: sembuh, belum sembuh(dirawat), meninggal
#print(dataharian_n)

#Mengubah tipe data dict values menjadi list
n=0
for i in dataharian_n["jumlah_meninggal"]:
    dataharian_n["jumlah_meninggal"].iloc[n] = list(dataharian_n["jumlah_meninggal"].iloc[n].values())
    #print(dataharian_n["jumlah_meninggal"].iloc[n])
    n+=1
n=0
for i in dataharian_n["jumlah_sembuh"]:
    dataharian_n["jumlah_sembuh"].iloc[n] = list(dataharian_n["jumlah_sembuh"].iloc[n].values())
    #print(dataharian_n["jumlah_sembuh"].iloc[n])
    n+=1
n=0
for i in dataharian_n["jumlah_positif"]:
    dataharian_n["jumlah_positif"].iloc[n] = list(dataharian_n["jumlah_positif"].iloc[n].values())
    #print(dataharian_n["jumlah_positif"].iloc[n])
    n+=1
n=0
for i in dataharian_n["jumlah_dirawat"]:
    dataharian_n["jumlah_dirawat"].iloc[n] = list(dataharian_n["jumlah_dirawat"].iloc[n].values())
    #print(dataharian_n["jumlah_dirawat"].iloc[n])
    n+=1

#Mengganti format tanggal 
n=0
for i in dataharian_n["key_as_string"]:
    dataharian_n["key_as_string"].iloc[n] = dataharian_n["key_as_string"].iloc[n].replace("T00:00:00.000Z","")
    dataharian_n["key_as_string"].iloc[n] = dataharian_n["key_as_string"].iloc[n].replace("-","/")
    #print(dataharian_n["jumlah_dirawat"].iloc[n])
    n+=1
dataharian_n = dataharian_n.rename(columns={"key_as_string": "Tanggal"})
#dataharian_n['Tanggal'] = pd.to_datetime(dataharian_n['Tanggal'])
print(dataharian_n)

#dataharian_n = dataharian_n.set_index('Tanggal')

x_data = []
for i in dataharian_n['Tanggal']:
    x_data.append(i)
y_data1 = []
for i in dataharian_n['jumlah_meninggal']:
    y_data1.append(i)
y_data2 = []
for i in dataharian_n['jumlah_sembuh']:
    y_data2.append(i)
y_data3 = []
for i in dataharian_n['jumlah_positif']:
    y_data3.append(i)
y_data4 = []
for i in dataharian_n['jumlah_dirawat']:
    y_data4.append(i)
print(x_data)
pd.to_datetime(x_data, format='%Y/%m/%d')

#Grafik garis
plot1 = plt.plot(x_data, y_data1, color = 'r',label = 'Jumlah Meninggal')
plot2 = plt.plot(x_data, y_data2, color = 'b',label = 'Jumlah Sembuh')
plot3 = plt.plot(x_data, y_data3, color = 'm',label = 'Jumlah Positif')
plot4 = plt.plot(x_data, y_data4, color = 'y',label = 'Jumlah Dirawat')
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Kematian")
plt.title("Grafik Kasus COVID-19")
plt.legend()
plt.show()