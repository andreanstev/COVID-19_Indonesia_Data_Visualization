import json
import pandas as pd
import matplotlib.pyplot as plt
#df = pd.read_json("https://data.covid19.go.id/public/api/update.json")
with open(r'D:\Myproject\pycode\data_analysis_covid19_indonesia\cov19-060820.json') as f:
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
dataharian = dataharian[["key_as_string","jumlah_meninggal", "jumlah_sembuh", "jumlah_positif", "jumlah_dirawat","jumlah_meninggal_kum", "jumlah_sembuh_kum", "jumlah_positif_kum", "jumlah_dirawat_kum"]]

#Data n hari terakhir
n = 157
dataharian_n = dataharian.iloc[157-n:157]
#Note: jumlah_meninggal + jumlah_sembuh + jumlah_dirawat = jumlah_positif
#Ada tiga kemungkinan yang dapat terjadi pada orang yang positif: sembuh, belum sembuh(dirawat), meninggal
#print(dataharian_n)

#Mengubah tipe data dict values menjadi list
def valueformat(df_col):
    n=0
    for i in df_col:
        df_col.iloc[n] = list(df_col.iloc[n].values())
        n+=1
    return df_col
dataharian_n["jumlah_meninggal"] = valueformat(dataharian_n["jumlah_meninggal"])
dataharian_n["jumlah_sembuh"] = valueformat(dataharian_n["jumlah_sembuh"])
dataharian_n["jumlah_positif"] = valueformat(dataharian_n["jumlah_positif"])
dataharian_n["jumlah_dirawat"] = valueformat(dataharian_n["jumlah_dirawat"])
dataharian_n["jumlah_meninggal_kum"] = valueformat(dataharian_n["jumlah_meninggal_kum"])
dataharian_n["jumlah_sembuh_kum"] = valueformat(dataharian_n["jumlah_sembuh_kum"])
dataharian_n["jumlah_positif_kum"] = valueformat(dataharian_n["jumlah_positif_kum"])
dataharian_n["jumlah_dirawat_kum"] = valueformat(dataharian_n["jumlah_dirawat_kum"])

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

#Mengkopi data kolom ke variabel list
def plotvalue(df_col,list_col):
    for i in df_col:
        list_col.append(i)
        
x_data = []
plotvalue(dataharian_n['Tanggal'], x_data)
y_data1 = []
plotvalue(dataharian_n['jumlah_meninggal'], y_data1)
y_data2 = []
plotvalue(dataharian_n['jumlah_sembuh'], y_data2)
y_data3 = []
plotvalue(dataharian_n['jumlah_positif'], y_data3)
y_data4 = []
plotvalue(dataharian_n['jumlah_dirawat'], y_data4)
y_data1_kum = []
plotvalue(dataharian_n['jumlah_meninggal_kum'], y_data1_kum)
y_data2_kum = []
plotvalue(dataharian_n['jumlah_sembuh_kum'], y_data2_kum)
y_data3_kum = []
plotvalue(dataharian_n['jumlah_positif_kum'], y_data3_kum)
y_data4_kum = []
plotvalue(dataharian_n['jumlah_dirawat_kum'], y_data4_kum)
x_data = pd.to_datetime(x_data, format='%Y/%m/%d')

#Grafik garis
plot1 = plt.plot(x_data, y_data1, color = 'r',label = 'Jumlah Meninggal')
plot2 = plt.plot(x_data, y_data2, color = 'b',label = 'Jumlah Sembuh')
plot3 = plt.plot(x_data, y_data3, color = 'm',label = 'Jumlah Positif')
plot4 = plt.plot(x_data, y_data4, color = 'y',label = 'Jumlah Dirawat')
highest_index = y_data3.index([pd.Series(y_data3).max()[0]]) #Mencari index dengan tingkat jumlah positif tertinggi
print(x_data[129]) #Mencari tanggal dengan tingkat jumlah positif tertinggi
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Penambahan")
plt.title("Grafik Laju Penambahan Kasus COVID-19")
plt.legend()
plt.show()

#Grafik garis
plot1 = plt.plot(x_data, y_data1_kum, color = 'r',label = 'Jumlah Meninggal')
plot2 = plt.plot(x_data, y_data2_kum, color = 'b',label = 'Jumlah Sembuh')
plot3 = plt.plot(x_data, y_data3_kum, color = 'm',label = 'Jumlah Positif')
plot4 = plt.plot(x_data, y_data4_kum, color = 'y',label = 'Jumlah Dirawat')
plt.xlabel("Tanggal")
plt.ylabel("Jumlah Kasus")
plt.title("Grafik Kasus COVID-19 Kumulatif")
plt.legend()
plt.show()

