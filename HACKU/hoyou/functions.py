from datetime import datetime
import os
import base64
from .models import Person,Record,Shuttai
import numpy as np
import pickle

def get_datetime(date_str,time_str):
    date_obj = datetime.strptime(date_str, '%Y-%m-%d') 
    time_obj = datetime.strptime(time_str, '%H:%M') 
    combined_datetime = datetime.combine(date_obj.date(), time_obj.time())
    return combined_datetime

#内積計算
def inner_product(vector):
    persons=Person.objects.all()
    max=-float('inf')
    id=None
    #登録してない人が通った場合はまた考えしょう
    for person in persons:
        if(isinstance(person.vector, np.ndarray)):
            m=np.dot(person.vector,vector)
            if m>max:
                max=m
                id=person.id
    return id

#person.idと出退勤のデータからRecordobjectの作成
def create_record(person_id,shuttai_data):
    person=Person.objects.get(id=person_id)
    Record.objects.create(person=person,shuttai=shuttai_data)
