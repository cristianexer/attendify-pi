#!/usr/bin/env python

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import requests as req
import json
import jwt

api_endpoint = "http://35.197.206.56/student"

secret_key = "msc_computer_science_admin"

def create_token(key):
   return jwt.encode({'app':'attendify'},key,algorithm='HS256')

def get_student_id(email):
   headers = {'Authorization': 'Bearer ' + create_token(secret_key)}
   res = req.get(url=api_endpoint, headers=headers, data={'email':email})
   return json.loads(res.text)

reader = SimpleMFRC522()

try:
    email = raw_input('Student email:')
    res = get_student_id(email)
    if res['student_id']:
        print('Tap your card')
        reader.write(res['student_id'])
        print('Written Successful')
    else:
        print(res['response'])
finally:
    GPIO.cleanup()
