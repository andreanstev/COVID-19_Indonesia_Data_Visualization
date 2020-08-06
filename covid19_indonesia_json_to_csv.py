import json
import re
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
dataharian = dataharian[["key_as_string","jumlah_meninggal", "jumlah_sembuh", "jumlah_positif", "jumlah_dirawat"]]

#Note: jumlah_meninggal + jumlah_sembuh + jumlah_dirawat = jumlah_positif
#Ada tiga kemungkinan yang dapat terjadi pada orang yang positif: sembuh, belum sembuh(dirawat), meninggal

#Mengubah tipe data dict values menjadi list
def valueformat(df_col):
    n=0
    for i in df_col:
        df_col.iloc[n] = list(df_col.iloc[n].values())
        n+=1
    return df_col
dataharian["jumlah_meninggal"] = valueformat(dataharian["jumlah_meninggal"])
dataharian["jumlah_sembuh"] = valueformat(dataharian["jumlah_sembuh"])
dataharian["jumlah_positif"] = valueformat(dataharian["jumlah_positif"])
dataharian["jumlah_dirawat"] = valueformat(dataharian["jumlah_dirawat"])

n=0
for i in dataharian["key_as_string"]:
    dataharian["key_as_string"].iloc[n] = dataharian["key_as_string"].iloc[n].replace("T00:00:00.000Z","")
    dataharian["key_as_string"].iloc[n] = dataharian["key_as_string"].iloc[n].replace("-","/")
    #print(dataharian["jumlah_dirawat"].iloc[n])
    n+=1
dataharian = dataharian.rename(columns={"key_as_string": "Tanggal"})
dataharian.to_csv('D:\Myproject\pycode\data_analysis_covid19_indonesia\cov19-060820.csv')
