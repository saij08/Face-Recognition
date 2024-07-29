from datetime import date
from datetime import datetime
import csv
import os
import send_mail
import pandas as pd
import json
from json import JSONEncoder
from json import JSONDecoder
import numpy
import FRM
import mysql.connector
from mysql.connector import Error
import cv2

import os
from glob import glob

myconn = mysql.connector.connect(host = "localhost", user = "root",passwd = "",database="frams")
print(myconn)
mycursor = myconn.cursor()

def train_dataset():
        iterations = 0
        attendance = []

        cap_cam = cv2.VideoCapture(0)

        full_width = 900
        font = cv2.FONT_HERSHEY_PLAIN

        directory = os.getcwd()
        persons = glob(directory+'/data/*')
        known_face_encodings = []
        known_face_names = []
        fieldnames = []
        fieldnames.append('Date')
        fieldnames.append('Time')

        today = date.today()
        present_date = today.strftime("%d/%m/%Y")
        current_time = datetime.now()
        current_time = current_time.strftime("%H:%M:%S")
        attendance.append(present_date)
        attendance.append(current_time)

        for person_name in persons:
            Known_names = os.path.basename(person_name)
            path = os.path.join(person_name, '*.png')
            for img in glob(path):
                print(img)
                face_image = FRM.load_image_file(img)
                face_encoding = FRM.face_encodings(face_image)[0]
                known_face_encodings.append(face_encoding)
                known_face_names.append(Known_names)
                



        class NumpyArrayEncoder(JSONEncoder):
            def default(self, obj):
                if isinstance(obj, numpy.ndarray):
                    return obj.tolist()
                return JSONEncoder.default(self, obj)

        finaldata={"kfe":known_face_encodings}
        with open("om.json", "w") as write_file:
            json.dump(finaldata, write_file, cls=NumpyArrayEncoder)
        
        
            

        
    

def take():
    def face_id():
        iterations = 0
        attendance = []

        cap_cam = cv2.VideoCapture(0)

        full_width = 900
        font = cv2.FONT_HERSHEY_PLAIN

        directory = os.getcwd()
        persons = glob(directory+'/data/*')
        known_face_encodings = []
        known_face_names = []
        fieldnames = []
        fieldnames.append('Date')
        fieldnames.append('Time')

        today = date.today()
        present_date = today.strftime("%d/%m/%Y")
        current_time = datetime.now()
        current_time = current_time.strftime("%H:%M:%S")
        attendance.append(present_date)
        attendance.append(current_time)

        for person_name in persons:
            Known_names = os.path.basename(person_name)
            path = os.path.join(person_name, '*.png')
            for img in glob(path):
                print(img)
                face_image = FRM.load_image_file(img)
                known_face_names.append(Known_names)
                fieldnames.append(Known_names)
                attendance.append('A')


        
        with open("om.json", "r") as read_file:
            decodedArray = json.load(read_file)
            known_face_encodings= numpy.asarray(decodedArray["kfe"])
            

        




        face_locations = []
        face_encodings = []
        face_names = []
        process_this_frame = True

        while True:
            iterations+=1

            ret, frame = cap_cam.read()

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
           
            if process_this_frame:
              
                face_locations = FRM.face_locations(rgb_small_frame)
                face_encodings = FRM.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                checkdict={}
                for face_encoding in face_encodings:
                    
                    matches = FRM.compare_faces(known_face_encodings, face_encoding)
                    name = "Unknown"

                    if True in matches:
                        first_match_index = matches.index(True)
                        name = known_face_names[first_match_index]
                        attendance[first_match_index+2] = 'P'
                        checkdict[name]=present_date

                    face_names.append(name)
                
                print(face_names)
        
                
                
                   

            process_this_frame = not process_this_frame
            
            for (top, right, bottom, left), name in zip(face_locations, face_names):
              
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
               
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
         
            cv2.imshow('Video', frame)       
            
            # 
            if((iterations > 5000) or cv2.waitKey(25) &0xFF == ord('q')):

                for i in checkdict:
                    sql = "INSERT INTO "+i+" (presentdate) VALUES (%s)"
                    print(sql)
                    val = (checkdict[i])
                    print(val)
                    mycursor.execute(sql, (val,))
                    myconn.commit()
                    print(mycursor.rowcount, "record inserted.")

                cv2.waitKey(100)
                print('Lecture Over')
                data2write1=zip(fieldnames,attendance)
                data2write = dict(data2write1)
                with open('Attendance_sheet.csv', 'a', newline='') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                    writer.writerow(data2write)

                os.system("start EXCEL.EXE Attendance_sheet.csv")

                cap_cam.release()

                cv2.destroyAllWindows()
                break

    face_id()


    def find_absent(a_list):
        indices = []
        for i in range(len(a_list)):
           if a_list[i] == 'A':
              indices.append(i-2)
        return indices

    with open('Attendance_sheet.csv', newline='') as csvfile:
        data = list(csv.reader(csvfile))

    last_attendance_status = data[len(data)-1]
    print(last_attendance_status)

    absent_student_index = find_absent(last_attendance_status)

    print(absent_student_index)

    data=pd.read_csv('information.csv')


    name = data['name']
    email = data['email']

    for index in absent_student_index:
        send_mail.send(email[index],name[index])

    print('Mail sendto the parents of absend student')

