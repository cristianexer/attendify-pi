#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests as req
import json
import jwt
import time

api_endpoint = "http://35.197.206.56/attendance/create"

building_name = "INB"

room_id = "1302"

secret_key = "msc_computer_science"

def create_token(id):
   return jwt.encode({'student_id':id},secret_key,algorithm='HS256')


def register_attendance(id):
   good = True
   try:
       token = create_token(id)
   except:
       print("No student ID")
       good = False
   if good == True:
       data = {'student_id':id, 'building_name':building_name, 'room_id':room_id}
       headers = {'Authorization': 'Bearer ' + token}
       res = req.post(url=api_endpoint, headers=headers, data=data)
       return json.loads(res.text)
   else:
       return {'res':'Failed to read student_id'}



while True:
    reader = SimpleMFRC522()
    try:
        print("Tap your phone or card")
        id, student_id = reader.read()
        print(student_id)
        res = register_attendance(student_id)
        print(res['response'])
    finally:
        GPIO.cleanup()
    print('\nWait 10seconds')
    time.sleep(10)
    print('\nTime elapsed \n')



