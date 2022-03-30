import requests
import json

f = open('key', 'r', encoding='utf-8')
key = f.read()
key = key.strip()
f.close()

schoolName = '선유중학교'
url = f'https://open.neis.go.kr/hub/schoolInfo?KEY={key}&Type=json&SCHUL_NM={schoolName}'
response = requests.get(url)
school_infos = json.loads(response.text)
print(school_infos)

print(school_infos['schoolInfo'][0]['head'][1]['RESULT']['CODE'])
if school_infos['schoolInfo'][0]['head'][1]['RESULT']['CODE'] == 'INFO-000':
    print('정상')
    for i in school_infos['schoolInfo'][1]['row']:
        print('교육청 코드: ' + i['ATPT_OFCDC_SC_CODE'])
        print('교육청 이름: ' + i['ATPT_OFCDC_SC_NM'])
        print('학교 코드: ' + i['SD_SCHUL_CODE'])
        print('학교 이름: ' + i['SCHUL_NM'])
        print('학교 주소: ' + i['ORG_RDNMA'])
