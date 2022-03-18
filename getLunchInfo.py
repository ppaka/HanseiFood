import requests
import json
import datetime

# now = str(datetime.datetime.now())
now = str(datetime.datetime.today() + datetime.timedelta(days=1))
year = now[:4]
month = now[5:7]
date = now[8:10]

url = f'https://schoolmenukr.ml/api/high/B100000662?year={now[:4]}&month={now[5:7]}&date={now[8:10]}&allergy=hidden'
response = requests.get(url)
school_menu = json.loads(response.text)
print(school_menu)

for i in school_menu['menu'][0]['lunch']:
    print(i)
