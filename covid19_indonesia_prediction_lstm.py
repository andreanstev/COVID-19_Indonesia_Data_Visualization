import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler 
 
df = pd.read_csv(r'D:\Myproject\pycode\data_analysis_covid19_indonesia\cov19-060820.csv')
plt.figure(figsize=(20,10))
plt.title('Data Historis Kasus COVID-19')
plt.plot(df['jumlah_meninggal'], color = 'r' ,label = 'Jumlah Meninggal')
plt.plot(df['jumlah_sembuh'], color = 'b' ,label = 'Jumlah Sembuh')
plt.plot(df['jumlah_positif'], color = 'm' ,label = 'Jumlah Positif')
plt.plot(df['jumlah_dirawat'], color = 'y', label = 'Jumlah Dirawat')
plt.xlabel("Hari")
plt.ylabel("Jumlah")
plt.legend()
plt.show()

data = df.filter(['jumlah_sembuh','jumlah_positif','jumlah_dirawat'])
#print(data)
dataset = data.values #Mengubah data menjadi list
#print(dataset)
training_data_len = len(dataset)
scaler = MinMaxScaler()
scaled_dataset = scaler.fit_transform(dataset)

ft = len(data.columns) #Jumlah fitur yang digunakan utk membuat model
h=30 #Jumlah test
inp=40 #Jumlah input
train_data = scaled_dataset[0:training_data_len-h,:]
x_train = []
y_train = []
for i in range(inp, len(train_data)): 
  x_train.append(train_data[i-inp:i])
  y_train.append(train_data[i])
x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], ft))

learning_rate = 0.015
epoch = 25
LSTMnode1 = 50
LSTMnode2 = 100
Densenode = 25
model = Sequential()
model.add(LSTM(LSTMnode1, return_sequences=True, input_shape=(x_train.shape[1], ft)))
model.add(LSTM(LSTMnode2, return_sequences=False))
model.add(Dropout(0.1))
model.add(Dense(Densenode))
model.add(Dense(ft))
model.compile(optimizer = keras.optimizers.Adam(learning_rate=learning_rate), loss = 'mean_squared_error')
model.fit(x_train, y_train, batch_size=1, epochs=epoch)

test_data = scaled_dataset[training_data_len-(inp+h):training_data_len,:] #522 sampai 642, test_data.shape = (60, 1)
x_test = []
y_test = []
for i in range(inp, len(test_data)):
  x_test.append(test_data[i-inp:i])
  y_test.append(train_data[i])
x_test,y_test = np.array(x_test), np.array(y_test)
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], ft))

predictions = model.predict(x_test)
rmse = np.sqrt(np.mean((predictions[:,1] - y_test[:,1])**2))
print(rmse)
predictions = scaler.inverse_transform(predictions)

train = data[:training_data_len-h].iloc[:,1]
valid = data[training_data_len-h:training_data_len].iloc[:,1]
plot_prediksi = pd.Series(predictions[:,1], index = range(training_data_len-h,training_data_len))
plt.figure(figsize=(20,10))
plt.title('Prediksi Kasus Positif')
plt.xlabel('Tanggal', fontsize = 16 )
plt.ylabel('Jumlah', fontsize = 16 )
plt.plot(train)
plt.plot(valid)
plt.plot(plot_prediksi)
str1 = 'Learning rate: {}'.format(learning_rate)
str2 = 'Epoch: {}'.format(epoch)
str3 = 'Jumlah Dense Node: {}'.format(Densenode)
str4 = 'Jumlah LSTM Node 2: {}'.format(LSTMnode2)
str5 = 'Jumlah LSTM Node 1: {}'.format(LSTMnode1)
str6 = 'Besar input: {}'.format(inp)
str7 = 'Jumlah test data: {}'.format(h)
plt.text(4,200,str1)
plt.text(4,300,str2)
plt.text(4,400,str3)
plt.text(4,500,str4)
plt.text(4,600,str5)
plt.text(4,700,str6)
plt.text(4,800,str7)
plt.legend(['Train','Val','Predictions'], loc = 'lower right')
plt.show()
