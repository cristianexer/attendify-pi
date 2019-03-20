#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests as req
import json
from base64 import b64decode


api_endpoint = "http://35.197.206.56/attendance/create"

building_name = "INB"

room_id = "1302"


def json_format(di):
   return json.dumps(di, sort_keys=True, indent=4, separators=(',',': '))

def get_student_id(token):
   base64 = token.replace('-','+').replace('_','/')
   return json.loads(b64decode(base64 + '=' * (-len(base64) % 4)))['student_id']

def register_attendance(token):
   good = True
   try:
       student_id = get_student_id(token)
   except:
       print("No student ID")
       good = False
   if good == True:
       data = {'student_id':student_id, 'building_name':building_name, 'room_id':room_id}
       headers = {'Authorization': 'Bearer ' + token}
       res = req.post(url=api_endpoint, headers=headers, data=data)
       return json.loads(res.text)
   else:
       return {'res':'Failed to read student_id'}

reader = SimpleMFRC522()

try:
    print("Tap your phone or card")
    id, token = reader.read()
    print(id)
    print(token)
    res = register_attendance(token)
    print(res['response'])
finally:
    GPIO.cleanup()




