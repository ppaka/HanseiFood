import json
import requests

url = 'https://open.neis.go.kr/hub/mealServiceDietInfo?Type=json&pIndex=1&pSize=100&ATPT_OFCDC_SC_CODE=B10&SD_SCHUL_CODE=7010911&MLSV_YMD=20230615'
response = requests.get(url)
data = json.loads(response.text)
print(data)

if data.get('mealServiceDietInfo') == None:
    print('데이터 에러')

if data['mealServiceDietInfo'][0]['head'][1]['RESULT']['CODE'] == 'INFO-000':
    print(data['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'])
else:
    print(data['mealServiceDietInfo'][0]['head'][1]['RESULT']['CODE'].split('<br/>'))
