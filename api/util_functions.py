from datetime import datetime

class Util: 
    def get_time_now(self): 
        now = datetime.now()
        return now.strftime('%Y-%m-%d %H:%M')