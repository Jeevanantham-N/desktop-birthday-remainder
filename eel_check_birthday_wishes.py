import eel
import csv
import datetime
from datetime import date
import plyer
import time
import sys
import signal

eel.init('/home/jeevanantham/Built/GRL_27_2_2020/web')


@eel.expose()
def py_Date_of_birth():


    class Date_of_birth():

        def __init__(self):
            self.csvpath = "/home/jeevanantham/Built/GRL_27_2_2020/Dob.csv"
            self.uncheck_dob_list = []
            self.main_dob = []

        def import_csv(self):
            with open(self.csvpath,errors = "replace") as file:
                reader = csv.reader(file)
                self.uncheck_dob_list = list(reader)
            Date_of_birth.sort_dob(self)

        def sort_dob(self):
            self.uncheck_dob_list = sorted(self.uncheck_dob_list)
            for i in range(0,len(self.uncheck_dob_list)):
                a_mon = self.uncheck_dob_list[i][0].split('.')[0]
                a_date = self.uncheck_dob_list[i][0].split('.')[1]
                min_date = a_date
                a_index = i
                b_index = i
                for j in range(i+1,len(self.uncheck_dob_list)):
                    b_mon = self.uncheck_dob_list[j][0].split('.')[0]
                    b_date = self.uncheck_dob_list[j][0].split('.')[1]
                    if a_mon == b_mon:
                        if int(min_date) > int(b_date):
                            min_date = b_date
                            b_index = j
                    else:
                        break
                if a_index == b_index:
                    pass
                else:
                    self.uncheck_dob_list[a_index],self.uncheck_dob_list[b_index] = self.uncheck_dob_list[b_index],self.uncheck_dob_list[a_index]

            self.main_dob = self.uncheck_dob_list
            Date_of_birth.notify(self)

        def notify(self):
            while True: 
                flag = 0
                notify_people = []
                for i in range(0,len(self.main_dob)):
                    current_date = date.today()
                    current_year  = current_date.year
                    current_date = str(current_date)
                    today_date = date(int(current_date.split('-')[0]),int(current_date.split('-')[1]),int(current_date.split('-')[2]))
                    dob_date = date(current_year,int(self.main_dob[i][0].split('.')[0]),int(self.main_dob[i][0].split('.')[1]))
                    delta = (dob_date-today_date).days
                    if (flag == 0) and (delta>=0):
                        flag = 1
                        start_index = i

                    if delta < 0:
                        continue
                    if delta<7:
                        notify_people.append(i)
                    else:  
                        break
                person = ""
                
                if len(notify_people) > 0:
                    for i in notify_people:
                        person += self.main_dob[i][1]+"    " + self.main_dob[i][0]+'\n'
                    person = person[slice(len(person)-1)]
                    # plyer.notification.notify(title = "Birthday wishes" , message = person,app_icon="/home/jeevanantham/Pictures/birthday.png")
                    sys.stdout.flush()
                    eel.view_js_function(notify_people,start_index,self.main_dob)
                    time.sleep(10)
                else:
                    sys.stdout.flush()
                    time.sleep(518400)

    obj1 = Date_of_birth()
    obj1.import_csv()

@eel.expose
def py_close():
    exit()


def keyboardInterruptHandler(signal, frame):
    print("KeyboardInterrupt")
    eel.window_close()

eel.start("index.html",size = (210,200),block=False)


while True:
    eel.sleep(1.0)