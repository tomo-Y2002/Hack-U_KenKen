from datetime import datetime
import os
import base64

def get_datetime(date_str,time_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d') 
    time_obj = datetime.strptime(time_str, '%H:%M') 
    combined_datetime = datetime.combine(date_obj.date(), time_obj.time())
    return combined_datetime