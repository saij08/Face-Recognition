from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import tkinter as tk 
from tkinter import filedialog
import os
import cv2

import mysql.connector
from mysql.connector import Error
import time

project_name = "Attendance System"
myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "",database="frams")
print(myconn)
mycursor = myconn.cursor()



from tkinter import Tk, Label, Entry, Toplevel, Canvas

from PIL import Image, ImageDraw, ImageTk, ImageFont
import generate_new_attendance_sheet
import Take_attendance

from Take_attendance import train_dataset

########################################################################################



def start_GUI():
    GUI_page = Tk()
    GUI_page.geometry("1350x690+0+0")
    GUI_page.configure(background="#ffffff")

    global B_color
    global F_color
    B_color = "#FFFFFF"
    F_color = "#000000"

    textbox = tk.Entry(GUI_page)
    textbox.place(x = 250,y = 325 ,height=30, width=350)

    
    def add_student():
        value=textbox.get()
        if(value!=""):
            directory = value
                 
            parent_dir = "C:/Users/saija/Downloads/face recognition attendance monitoring system-20231227T044536Z-001/face recognition attendance monitoring system/data"
            path = os.path.join(parent_dir, directory)    
            os.makedirs(path)

            videoCaptureObject = cv2.VideoCapture(0)
            result = True
            save_path = os.path.join(path,value+".png") 
            
            while(result):
                ret,frame = videoCaptureObject.read()
                imagename=save_path
                cv2.imshow('frame',frame)
                if cv2.waitKey(1)== ord("q"):
                    cv2.imwrite(imagename,frame)
                    result=False
                    textbox.insert(0,"Student Added Successfully-: ")
                    mycursor.execute(f"CREATE TABLE {value} (presentdate VARCHAR(255))")
                
            
            videoCaptureObject.release()
            cv2.destroyAllWindows()  



    def LOGIN():

        def take_attendance():
            print('Take Attendance')
            Take_attendance.take()



        def generate_sheet():
            print('Generate ')
            generate_new_attendance_sheet.generate()
            
        label2 = Label(GUI_page, text=project_name)
        label2.configure(background=B_color)
        label2.configure(foreground=F_color)
        label2.config(font=("Times new roman", 25))
        label2.place(x = 25,y=20,height=40, width=1300)


        B1 = Button(GUI_page, text = "Take Attendance", command = take_attendance)
        B1.place(x = 250,y = 450 ,height=100, width=350)
        B1.configure(background="#808080")
        B1.configure(foreground=F_color)
        B1.config(font=("Times new roman", 25))

        B3 = Button(GUI_page, text = "Train", command = train_dataset)
        B3.place(x = 750,y = 250 ,height=100, width=350)
        B3.configure(background="#808080")
        B3.configure(foreground=F_color)
        B3.config(font=("Times new roman", 25))

        B4 = Button(GUI_page, text = "Add Student", command = add_student)
        B4.place(x = 250,y = 250 ,height=70, width=350)
        B4.configure(background="#808080")
        B4.configure(foreground=F_color)
        B4.config(font=("Times new roman", 25))
        sname = Label(GUI_page, text = "Enter Name-: ").place(x = 250,y = 360)
        

        B1 = Button(GUI_page, text = "Generate New Sheet", command = generate_sheet)
        B1.place(x = 750,y = 450 ,height=100, width=350)
        B1.configure(background="#808080")
        B1.configure(foreground=F_color)
        B1.config(font=("Times new roman", 25))

        GUI_page.mainloop()

    LOGIN()

start_GUI()


