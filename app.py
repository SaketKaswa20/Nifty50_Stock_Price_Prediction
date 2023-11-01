import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import load_model
import streamlit as st


st.title('Stock Market Prediction')

user_input=st.text_input('Enter Stock Name', 'ASIANPAINT.csv')
df = pd.read_csv(user_input)

#Describing Data
st.subheader('Data from 2001 to 2021')
st.write(df.describe())

#Visualizations
st.subheader('Closing Price v/s Time Chart')
fig= plt.figure(figsize=(12,6))
plt.plot(df.Close)
st.pyplot(fig)

st.subheader('Closing Price v/s Time Chart with 100 Moving Average')
ma100= df.Close.rolling(100).mean()
fig= plt.figure(figsize=(12,6))
plt.plot(ma100, label= 'MA 100')
plt.plot(df.Close, label= 'Closing Price')
st.pyplot(fig)

st.subheader('Closing Price v/s Time Chart with 100 & 200 Moving Average')
ma100= df.Close.rolling(100).mean()
ma200= df.Close.rolling(200).mean()
fig= plt.figure(figsize=(12,6))
plt.plot(ma100, label='MA 100')
plt.plot(ma200, label='MA 200')
plt.plot(df.Close, label='Closing Price')
st.pyplot(fig)

#Splitting Data into Training and Testing

data_training= pd.DataFrame(df['Close'][0:int(len(df)*0.70)]) #Keeping 70% Data for training that's why 0.7
data_testing= pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

from sklearn.preprocessing import MinMaxScaler #To Scale data between 0 and 1
scaler= MinMaxScaler(feature_range=(0,1))

data_training_array= scaler.fit_transform(data_training)

#Load my model
model= load_model('keras_model.h5')

#Testing Part
past_100_days=data_training.tail(100)
final_df= past_100_days.append(data_testing, ignore_index=True)
input_data=scaler.fit_transform(final_df)

x_test=[]
y_test=[]

for i in range(100, input_data.shape[0]):
  x_test.append(input_data[i-100: i])
  y_test.append(input_data[i, 0])

x_test, y_test= np.array(x_test), np.array(y_test)
y_predicted= model.predict(x_test)

scaler= scaler.scale_

scale_factor=1/scaler[0]
y_predicted= y_predicted * scale_factor
y_test= y_test * scale_factor

#Final Visualization
st.subheader('Predictions v/s Original')
fig2=plt.figure(figsize=(12,6))
plt.plot(y_test, 'b', label= 'Original Price')
plt.plot(y_predicted, 'r', label= 'Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)

