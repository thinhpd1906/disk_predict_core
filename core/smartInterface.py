import os
import subprocess
from api.convert_input import ConvertInput
from core.model import ModelCNN
from api.authentication import Authentication
from api.util_functions import Util
from api.smart import Smart
import mysql.connector
import schedule 

class SmartInterface:
    def __init__(self):
        self.device_name = None
        self.info = {}
        self.results = []
        self.smart = {}
        self.serial_number = ""
        self.current_directory = ""
    def get_current_folder(self):
        current_directory = os.getcwd()
        self.current_directory = current_directory
    def get_device_serial_number(self):
        cmd = ['sudo', self.current_directory + '/getserialnumber.sh']
        data = subprocess.check_output(cmd)
        res = data.decode('utf-8')
        temp = res.split(':')
        self.serial_number = temp[1].splitlines()[0].strip()
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
    def scheduleAddSmart(self):
        authentication = Authentication()
        username, password = authentication.get_user_credentials()
        token = authentication.authenticate(username, password)
        if token:
            self.get_current_folder()
            self.get_device_name()
            self.get_device_serial_number()
            convertInput = ConvertInput()
            model = ModelCNN(self.current_directory)
            utils = Util()
            smart = Smart()
            def insert():
                self.get_smart_infor_linux()
                smart_infor, smart_important = convertInput.convert(self.smart)
                class_heath = model.predict(smart_infor)
                smart_important["class_prediction"] = class_heath[0].item()
                smart_important["serial_number"] = self.serial_number
                smart_important["date"] = utils.get_time_now()
                print(class_heath, smart_important)
                try:
                    smart.create_smart(token, smart_important)
                except mysql.connector.Error as err:
                    print("fail to insert smart infor")
            insert()
            schedule.every(60).seconds.do(insert) 
            while True: 
                schedule.run_pending() 