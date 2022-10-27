import requests
import json
import dotenv
import os

from getSavedSchoolJsonPath import getSavedSchoolJsonPath

dotenv.load_dotenv()
NIES_KEY = os.getenv('NIES_KEY')


def getSchoolData(guildId):
    path = getSavedSchoolJsonPath()

    try:
        with open(path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            file.close()
            return (str(json_data[str(guildId)][0]), str(json_data[str(guildId)][1]))
    except KeyError as err:
        print('설정되어지지 않은 서버')
        return None
    except FileNotFoundError as err:
        print('파일이 존재하지 않습니다')
        return None
    except json.decoder.JSONDecodeError as err:
        print('올바른 Json 파일 형식이 아닙니다')
        return None


def getSchoolInfo(nies_key, school_name):
    url = f'https://open.neis.go.kr/hub/schoolInfo?KEY={nies_key}&Type=json&SCHUL_NM={school_name}'
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        if data['schoolInfo'][0]['head'][1]['RESULT']['CODE'] == 'INFO-000':
            return data
    except:
        return False
