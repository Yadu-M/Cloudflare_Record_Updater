import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv

def main():
  
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
    time = datetime.now().ctime()
    res = requests.put(f'{BASE_URL}{record["id"]}', headers={
      'Content-Type': 'application/json',
      'X-Auth-Email': ACCOUNT_EMAIL,
      'Authorization': f'Bearer {CLOUDFLARE_API}' 
    }, data=json.dumps({
      'content': ip,
      'name': record['name'],
      'proxied': record['proxied'],
      'type': record['type'],
      'comment': f'Updated record on {time}'
    }))
    
    if not res.ok:
      f.write(f'[error] PUT request failed on {time}\n')
      f.close()
      return
    
    data = res.json()
    
    if not data['success']:
      f.write(f'[error ]Couldn\'t update record: {data["result"]["name"]}\n')
      f.close()
      return
    
    f.write(f'[record] {data["result"]["name"]} updated on {data["result"]["modified_on"]}\n')

  f.write('\n')
  f.close()
  
if __name__ == '__main__':
  main()