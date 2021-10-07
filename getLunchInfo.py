import requests
from bs4 import BeautifulSoup
import datetime
import re

now = str(datetime.datetime.now())
day = now[:4] + now[5:7] + now[8:10]

print(day)

req = requests.get("http://stu.sen.go.kr/sts_sci_md01_001.do?schulCode=B100000662&schulCrseScCode=4&schulKndScCode=04&schMmealScCode=2&schYmd=20201218")
#print(req.text)
soup = BeautifulSoup(req.text, "html.parser")
#print(soup)
element = soup.find_all("tr")
#print(element[2])
element = element[2].find_all('td')

element = element[5]  # num
element = str(element)
element = element.replace('[', '')
element = element.replace(']', '')
element = element.replace('<br/>', '\n')
element = element.replace('<td class="textC last">', '')
element = element.replace('<td class="textC">', '')
element = element.replace('</td>', '')
element = element.replace('(h)', '')
element = element.replace('.', '')
element = re.sub(r"\d", "", element)

print(element)
