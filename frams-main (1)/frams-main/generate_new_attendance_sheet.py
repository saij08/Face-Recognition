import os
from glob import glob
import csv

def generate():
    directory = os.getcwd()
    persons = glob(directory+'/data/*')

    fieldnames = ['Date', 'Time']
    names = []
    for person_name in persons:
        Known_names = os.path.basename(person_name)
        path = os.path.join(person_name, '*.png')
        for img in glob(path):
            print(img)
            fieldnames.append(Known_names)
            names.append(Known_names)
    print(fieldnames)


    with open('Attendance_sheet.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    os.system("start EXCEL.EXE Attendance_sheet.csv")



    fieldnamess = ['name','email']
    with open('information.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnamess)
        writer.writeheader()

    for name in names:
        with open('information.csv', 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnamess)
            data2write = {'name':name}
            writer.writerow(data2write)

    os.system("start EXCEL.EXE information.csv")

    print()
    print()
    print("Don't Forget to write email id in 'information.csv' sheet")



