import numpy as np

import pandas as pd

df=pd.read_csv('track_data.csv')

df.head()

X=df.iloc[:,:-1].values
y=df.iloc[:,1].values

df.shape

from sklearn.model_selection import train_test_split

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=1/3,random_state=0)

from sklearn.linear_model import LinearRegression
lr=LinearRegression()
lr.fit(X_train,y_train)
 
t = X_test[0]


import serial
import time
from csv import writer

arduino = serial.Serial(port='COM10',  baudrate=115200, timeout=.1)

times = 0

while True:
    data = arduino.readline()
    strdata = data.decode('utf-8')
    times += 0.5
    time.sleep(0.5)
    if strdata != '' and strdata != '\n':
        num = float(strdata)
        predict = lr.intercept_ + lr.coef_*num
        ''' with open('track_data.csv','a') as dta:
                     list = [num,1]
                     wrt = writer(dta)
                     wrt.writerow(list)'''
        #print(predict)
        if (predict<0.4):
            print("Crack at ",times*6,"cm of width: ", predict/30, "cm and Depth: ",- predict/100, " cm")
