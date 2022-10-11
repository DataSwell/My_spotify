import os
import requests
import base64, json


client_id = os.environ.get('Sptify_ClientID')
client_sec = os.environ.get('Spoitify_ClientSec')


authURL = 'https://account.spotify.com/api/token'

auth_header = {}
auth_data = {}

#def getAccessToken(clientID, CLientSecret):
message = f"{client_id}:{client_sec}"
message_bytes = message.encode('ascii')
base64_bytes = base64.b64encode(message_bytes)
base64_message = base64_bytes.decode('ascii')
        
auth_header['Authorization'] = "Basic " + base64_message
auth_data['grant_type'] = "client_credentials"

res = requests.post(authURL, headers=auth_header, data=auth_data)

print(res)
res_json = res.json()
