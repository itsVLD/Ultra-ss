
import tkinter as tk
from tkinter import Scrollbar, Canvas

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



def funcpredict():
    data = arduino.readline()
    strdata = data.decode('utf-8')
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
            print("Crack")
            add_rectangle("red")
        else:
            add_rectangle("green")


def add_rectangle(color):
    global y_position
    if color == "red":
        canvas.create_rectangle(50, y_position, 150, y_position + 50, fill="red")
    elif color == "green":
        canvas.create_rectangle(50, y_position, 150, y_position + 50, fill="green")
    
    y_position += 60
    canvas.configure(scrollregion=canvas.bbox("all"))  

root = tk.Tk()
root.after(100,funcpredict())
root.title("Track Simulation")
root.geometry("800x700")


frame = tk.Frame(root)
frame.pack(fill=tk.BOTH, expand=True)

canvas = Canvas(frame)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

canvas.configure(yscrollcommand=scrollbar.set)

y_position = 10



root.mainloop()



