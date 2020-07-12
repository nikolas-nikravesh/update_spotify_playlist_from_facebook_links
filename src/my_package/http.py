import requests
import json
import logging

# Send a POST request
def post(url, headers=None):
   logging.info("Sending POST request")
   response = requests.post(url, headers=headers)
   logging.info("[POST] Response from server: {}".format(response))

   if not response.ok:
      logging.error("Error response from server: %s", response.text)
      raise Exception("Error in response from request: {}".format(response.text))

   return response

# Send a GET request
def get(url, headers=None):
   logging.info("Sending GET request")
   response = requests.get(url, headers=headers)
   logging.info("[GET] Response from server: {}".format(response))

   if not response.ok:
      logging.error("Error response from server: %s", response.text)
      raise Exception("Error in response from request: {}".format(response.text))

   data = json.loads(response.text.encode('UTF-8'))
   return response, data