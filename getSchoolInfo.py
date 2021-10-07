import requests
import json
url = 'https://schoolmenukr.ml/code/api?q=한세사이버보안고등학교'
response = requests.get(url)
school_infos = json.loads(response.text)
print(school_infos)
