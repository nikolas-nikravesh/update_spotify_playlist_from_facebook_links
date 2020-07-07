import requests
import json

def post(url, headers=None):
   print("Sending request...")
   response = requests.post(url, headers=headers)
   print("[POST] Response from server: {}".format(response))

   if not response.ok:
      raise Exception("Error in response from request: {}".format(response.text))

   return response

def get(url, headers=None):
   print("Sending request...")
   response = requests.get(url, headers=headers)
   print("[GET] Response from server: {}".format(response))
   
   if not response.ok:
      raise Exception("Error in response from request: {}".format(response.text))

   data = json.loads(response.text.encode('UTF-8'))
   return response, data