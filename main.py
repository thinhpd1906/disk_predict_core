# importing libraries
import os
import pandas as pd
from pandas import ExcelWriter
from api.convert_input import ConvertInput
import numpy as np
from core.model import ModelCNN
import subprocess
import schedule 
import time 
from api.connect_db import fconnect_db, close_connection, fconnect_db_prod
import mysql.connector
from api.constants import SMART_IMPORTANT_TABLE_FIELD
from api.util_functions import get_time_now
from api.authentication import authenticate, get_user_credentials
from api.smart import create_smart
# from subprocess import Popen
# import os
# os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0import tensorflow as tf

# from tensorflow import keras
# model = keras.models.load_model("C:/Users/phant/Downloads/my_model2.keras")
dt_1 = [[ 120, 243348344, 129.324528720867, 75.51483793169844, 91, 0, 100, 11, 100, 0, 88, 3.334065343e-315, 116.33913545770258, 29.485817003292947, 75, 22449, 100, 0, 100, 11, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 79.0, 21.0, 100.0, 0.0, 100.0, 2.0, 96.0, 9614.0, 21.0, 21.0, 112.2143920633918, 1.9035123564770473, 100, 0, 100, 0, 200, 0, 100.0, 1.10666e-319, 100.0, 1.286134885e-313, 100.0, 6.52686781186e-313], [ 118, 172187072, 129.324528720867, 75.51483793169844, 91, 0, 100, 11, 100, 0, 88, 3.33873486e-315, 116.33913545770258, 29.485817003292947, 75, 22473, 100, 0, 100, 11, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 79.0, 21.0, 100.0, 0.0, 100.0, 2.0, 96.0, 9614.0, 21.0, 21.0, 112.2143920633918, 1.9035123564770473, 100, 0, 100, 0, 200, 0, 100.0, 1.10784e-319, 100.0, 1.2864070776e-313, 100.0, 6.52810484493e-313], [ 114, 63032056, 129.324528720867, 75.51483793169844, 91, 0, 100, 11, 100, 0, 88, 3.343213225e-315, 116.33913545770258, 29.485817003292947, 75, 22497, 100, 0, 100, 11, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 79.0, 21.0, 100.0, 0.0, 100.0, 2.0, 96.0, 9614.0, 21.0, 21.0, 112.2143920633918, 1.9035123564770473, 100, 0, 100, 0, 200, 0, 100.0, 1.10903e-319, 100.0, 1.28668742133e-313, 100.0, 6.52932880645e-313], [ 117, 160490680, 129.324528720867, 75.51483793169844, 91, 0, 100, 11, 100, 0, 88, 3.347598715e-315, 116.33913545770258, 29.485817003292947, 75, 22521, 100, 0, 100, 11, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 79.0, 21.0, 100.0, 0.0, 100.0, 2.0, 96.0, 9614.0, 21.0, 21.0, 112.2143920633918, 1.9035123564770473, 100, 0, 100, 0, 200, 0, 100.0, 1.1102e-319, 100.0, 1.28697187647e-313, 100.0, 6.5304834733e-313], [ 112, 42289416, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.35120877e-315, 116.33913545770258, 29.485817003292947, 75, 22545, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 79.0, 21.0, 100.0, 0.0, 100.0, 2.0, 96.0, 9947.0, 21.0, 21.0, 112.2143920633918, 1.9035123564770473, 100, 0, 100, 0, 200, 0, 100.0, 1.11135e-319, 100.0, 1.2872650891e-313, 100.0, 6.531595232e-313], [ 114, 59292192, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.351678047e-315, 116.33913545770258, 29.485817003292947, 75, 22569, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 79.0, 21.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11234.0, 21.0, 21.0, 112.2143920633918, 1.9035123564770473, 100, 0, 100, 0, 200, 0, 100.0, 1.1123e-319, 100.0, 1.28727084745e-313, 100.0, 6.53210282003e-313], [ 117, 129528496, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.35526461e-315, 116.33913545770258, 29.485817003292947, 75, 22592, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 79.0, 21.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 21.0, 21.0, 112.2143920633918, 1.9035123564770473, 100, 0, 100, 0, 200, 0, 100.0, 1.1134e-319, 100.0, 1.28755395773e-313, 100.0, 6.53325321824e-313], [ 120, 240345120, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.358680903e-315, 116.33913545770258, 29.485817003292947, 75, 22614, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 79.0, 21.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 21.0, 21.0, 112.2143920633918, 1.9035123564770473, 100, 8, 100, 8, 200, 0, 100.0, 1.11446e-319, 100.0, 1.28803089027e-313, 100.0, 6.53399720225e-313], [ 112, 44920712, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.360733455e-315, 116.33913545770258, 29.485817003292947, 75, 22641, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 78.0, 22.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 22.0, 22.0, 112.2143920633918, 1.9035123564770473, 100, 8, 100, 8, 200, 0, 100.0, 1.1158e-319, 100.0, 1.28835135864e-313, 100.0, 6.53421131874e-313], [ 108, 20750744, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.36429324e-315, 116.33913545770258, 29.485817003292947, 75, 22665, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 78.0, 22.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 22.0, 22.0, 112.2143920633918, 1.9035123564770473, 100, 8, 100, 8, 200, 0, 100.0, 1.117e-319, 100.0, 1.2887331017e-313, 100.0, 6.53498457273e-313], [ 116, 102186000, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.369246764e-315, 116.33913545770258, 29.485817003292947, 75, 22689, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 78.0, 22.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 22.0, 22.0, 112.2143920633918, 1.9035123564770473, 100, 8, 100, 8, 200, 0, 100.0, 1.11817e-319, 100.0, 1.2895441927e-313, 100.0, 6.5364080478e-313], [ 119, 207304720, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.37454456e-315, 116.33913545770258, 29.485817003292947, 75, 22713, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 78.0, 22.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 22.0, 22.0, 112.2143920633918, 1.9035123564770473, 100, 8, 100, 8, 200, 0, 100.0, 1.1193e-319, 100.0, 1.2905213999e-313, 100.0, 6.5377840527e-313], [ 113, 52042776, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.37946967e-315, 116.33913545770258, 29.485817003292947, 75, 22736, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 78.0, 22.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 22.0, 22.0, 112.2143920633918, 1.9035123564770473, 100, 16, 100, 16, 200, 0, 100.0, 1.1205e-319, 100.0, 1.29119979254e-313, 100.0, 6.5391128623e-313], [ 120, 1736784, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.38475333e-315, 116.33913545770258, 29.485817003292947, 75, 22761, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 81.0, 19.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 19.0, 19.0, 112.2143920633918, 1.9035123564770473, 100, 16, 100, 16, 200, 0, 100.0, 1.12173e-319, 100.0, 1.291920279e-313, 100.0, 6.54050638616e-313], [ 117, 133557880, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.38944674e-315, 116.33913545770258, 29.485817003292947, 74, 22785, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 81.0, 19.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 19.0, 19.0, 112.2143920633918, 1.9035123564770473, 100, 16, 100, 16, 200, 0, 100.0, 1.1229e-319, 100.0, 1.29238962653e-313, 100.0, 6.5416626559e-313], [ 103, 5948304, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.39359903e-315, 116.33913545770258, 29.485817003292947, 74, 22808, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 81.0, 19.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 19.0, 19.0, 112.2143920633918, 1.9035123564770473, 100, 16, 100, 16, 200, 0, 100.0, 1.12405e-319, 100.0, 1.29257340175e-313, 100.0, 6.54280220334e-313], [ 118, 191747632, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.398214095e-315, 116.33913545770258, 29.485817003292947, 74, 22833, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 81.0, 19.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 19.0, 19.0, 112.2143920633918, 1.9035123564770473, 100, 40, 100, 40, 200, 0, 100.0, 1.1253e-319, 100.0, 1.29287567457e-313, 100.0, 6.5438977926e-313], [ 117, 120280536, 129.324528720867, 75.51483793169844, 91, 0, 100, 12, 100, 0, 88, 3.40282153e-315, 116.33913545770258, 29.485817003292947, 74, 22857, 100, 0, 100, 12, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 0.0, 96.0, 4.0, 81.0, 19.0, 100.0, 0.0, 100.0, 2.0, 95.0, 11612.0, 19.0, 19.0, 112.2143920633918, 1.9035123564770473, 100, 40, 100, 40, 200, 0, 100.0, 1.12647e-319, 100.0, 1.29322399836e-313, 100.0, 6.54508348214e-313]]
# a_array = dt_3
# class to hold all the
# details about the device
class Device():
    def __init__(self):
        self.device_name = None
        self.info = {}
        self.results = []
        self.smart = {}
        self.serial_number = ""
        self.current_directory = ""
    # get the details of the device
    def get_current_folder(self):
        current_directory = os.getcwd()
        self.current_directory = current_directory
    def get_device_serial_number(self):
        cmd = ['sudo', self.current_directory + '/getserialnumber.sh']
        data = subprocess.check_output(cmd)
        res = data.decode('utf-8')
        temp = res.split(':')
        self.serial_number = temp[1].splitlines()[0].strip()
        # print("serial num", self.serial_number)
    def get_smart_infor_linux(self):
        command = ['sudo', self.current_directory + '/getsmart.sh', self.device_name]
        data = subprocess.check_output(command)
        res = data.decode('utf-8')
        res = res.splitlines()
        index = res.index('=== START OF SMART DATA SECTION ===')
        disk_smart = {}
        for i in range((index+4), len(res)):
            if(res[i] == ''):
                break;
            line = res[i]
            temp = line.split(':')
            disk_smart[temp[0]] = temp[1].strip()
        self.smart = self.handle_smart_value(disk_smart)

    def get_device_name(self):
        cmd = 'smartctl --scan'
        data = os.popen(cmd)
        res = data.read()
        temp = res.split(' ')
        temp = temp[0].split('/')
        name = temp[2]
        self.device_name = name
 
 
    # get the device info (sda or sdb)
    def get_device_info(self):
        cmd = 'sudo smartctl -i /dev/' + self.device_name
        data = os.popen(cmd)
        res = data.read().splitlines()
        device_info = {}
 
        for i in range(4, len(res) - 1):
            line = res[i]
            temp = line.split(':')
            device_info[temp[0]] = temp[1]
        self.info = device_info
    
    def get_smart_infor_window(self):
        cmd = 'smartctl -a /dev/' + self.device_name 
        data = os.popen(cmd)
        res = data.read().splitlines()
        index = res.index('=== START OF SMART DATA SECTION ===')
        disk_smart = {}
        for i in range((index+4), len(res)):
            if(res[i] == ''):
                break;
            line = res[i]
            temp = line.split(':')
            disk_smart[temp[0]] = temp[1].strip()
        self.smart = self.handle_smart_value(disk_smart)

    def handle_smart_value(self, disk_smart: dict):
        smart_handled = {}
        for key, value in disk_smart.items():
            if "," in value:
                value = value.replace(',', '')
            if "." in value:
                value = value.replace('.', '')
            if key == "Temperature":
               temp = value.split(' ')
               smart_handled[key] = int(temp[0])
            elif key == "Host Read Commands":
                smart_handled[key] = int(value)
            elif key == "Host Write Commands":
                smart_handled[key] = int(value)
            elif key == "Power Cycles":
                smart_handled[key] = int(value)
            elif key == "Power On Hours":
                smart_handled[key] = int(value)
            elif key == "Unsafe Shutdowns":
                smart_handled[key] = int(value) 
            else:
                smart_handled[key] = value
        return smart_handled
def create_insert_smart_important():
    insert_query = "INSERT INTO smart_important ({}) VALUES ({})"
    columns = ", ".join([str(value) for value in SMART_IMPORTANT_TABLE_FIELD.values()])
    placeholders = ", ".join(["%(" + value + ")s" for value in SMART_IMPORTANT_TABLE_FIELD.values()])
    insert_query = insert_query.format(columns, placeholders)
    return insert_query


if __name__ == '__main__':
    username, password = get_user_credentials()
    token = authenticate(username, password)
    if token:
        device = Device()
        device.get_current_folder()
        device.get_device_name() 
        device.get_device_serial_number()
        convertInput = ConvertInput()
        model = ModelCNN(device.current_directory)
        insert_query = create_insert_smart_important()
        def test(): 
            device.get_smart_infor_linux()
            smart_infor, smart_important = convertInput.convert(device.smart)
            class_heath = model.predict(smart_infor)
            smart_important["class_prediction"] = class_heath[0].item()
            smart_important["serial_number"] = device.serial_number
            smart_important["date"] = get_time_now()
            print(class_heath, smart_important)
            try:
                create_smart(token, smart_important)
                # connection, cursor = fconnect_db()       
                # connection, cursor = fconnect_db_prod()       
                # cursor.execute(insert_query, smart_important)
                # connection.commit()
            except mysql.connector.Error as err:
                # print("Error: ", err)
                print("fail to insert smart infor")
            # finally:
                # close_connection(connection, cursor)
        test()
        schedule.every(60).seconds.do(test) 
        while True: 
            schedule.run_pending() 
            # time.sleep(1)
    else: 
        print("")

    
    
     
    


