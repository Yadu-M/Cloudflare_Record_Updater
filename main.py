import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ZONE_ID = os.getenv('ZONE_ID')
ACCOUNT_EMAIL = os.getenv('ACCOUNT_EMAIL')
CLOUDFLARE_API = os.getenv('CLOUDFLARE_API')

BASE_URL = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/'

f = open('record_update.log', 'a')

ip = requests.get('https://api.ipify.org?format=json').json()['ip']
dns_list = requests.get(BASE_URL, headers={
  'Content-Type': 'application/json',
  'X-Auth-Email': ACCOUNT_EMAIL,
  'Authorization': f'Bearer {CLOUDFLARE_API}' 
}).json()

for record in dns_list['result']:
  res = requests.put(f'{BASE_URL}{record["id"]}', headers={
    'Content-Type': 'application/json',
    'X-Auth-Email': ACCOUNT_EMAIL,
    'Authorization': f'Bearer {CLOUDFLARE_API}' 
  }, data=json.dumps({
    'content': ip,
    'name': record['name'],
    'proxied': record['proxied'],
    'type': record['type'],
    'comment': f'Updated record on {datetime.now().ctime()}'
  })).json()
  
  if not res['success']:
    f.close()
    raise Exception(f'Couldn\'t update record: {res["result"]["name"]}')
  
  f.write(f'[record] {res["result"]["name"]} updated on {res["result"]["modified_on"]}\n')

f.write('\n')
f.close()