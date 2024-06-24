import os

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