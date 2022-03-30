import requests
import json
import datetime

f = open('key', 'r', encoding='utf-8')
key = f.read()
key = key.strip()
f.close()

# now = str(datetime.datetime.now())
now = str(datetime.datetime.today() + datetime.timedelta(days=1))
year = now[:4]
month = now[5:7]
date = now[8:10]

atpt_code = 'B10'
school_code = '7010911'
ymd = '20220330'

url = f'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={key}&Type=json&ATPT_OFCDC_SC_CODE={atpt_code}&SD_SCHUL_CODE={school_code}&MLSV_YMD={ymd}'
response = requests.get(url)
school_menu = json.loads(response.text)
#print(school_menu)
print(school_menu['mealServiceDietInfo'][0]['head'][1]['RESULT']['CODE'])
if school_menu['mealServiceDietInfo'][0]['head'][1]['RESULT']['CODE'] == 'INFO-000':
    print('정상')
    #school_menu = school_menu.replace('<br/>', '\n')
    splited_data = school_menu['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'].split('<br/>')
    for i in splited_data:
        print(i)
