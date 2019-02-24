import requests as req
import json
from base64 import b64decode


api_endpoint = "https://attendify.appspot.com/attendance/create"

endpoint = "https://www.google.com"

mock_endpoint = "https://login-mock-xam.herokuapp.com/login"

building_name = "INB"

room_id = "1302"


def json_format(di):
   return json.dumps(di, sort_keys=True, indent=4, separators=(',',': '))

def get_student_id(token):
   base64Url = token.split('.')[1]
   base64 = base64Url.replace('-','+').replace('_','/')
   return json.loads(b64decode(base64 + '=' * (-len(base64) % 4)))


def register_attendance(token):
   student_id = get_student_id(token)
   data = {'student_id':student_id, 'building_name':building_name, 'room_id':room_id}
   headers = {'Authorization': 'Bearer ' + token}
   res = req.post(url=api_endpoint, headers=headers, data=data)
   return res

def get_page(url):
   return req.get(url=url, headers={'Accept-Encoding':'identity'})


def send_mock_req(payload):
  return req.post(url=mock_endpoint,headers={'Content-Type':'application/json'} , data=payload)

temp = { 'email':'test1@gmail.com', 'password':'test'}

login_mock = send_mock_req(json_format(temp))

response = json.loads(login_mock.text)

s_id = get_student_id(response['token'])['user_id']

print(s_id)


