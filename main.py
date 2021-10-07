import requests
from bs4 import BeautifulSoup
import datetime
import re

import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')


@client.event
async def on_ready():
    print(f'다음으로 로그인 합니다\n{client.user.name}')
    print(client.user.id)
    print('--------')
    await client.change_presence(activity=discord.Game(name='!급식오늘 또는... !급식내일'))


@client.command(name='급식오늘', pass_context=True)
async def getInfo(ctx):
    # now = str(datetime.datetime.now())
    # day = now[:4] + now[5:7] + now[8:10]
    to_tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)    #오늘 날짜에 하루를 더함
    local_date2 = to_tomorrow.strftime("%Y.%m.%d")    #위에서 구한 날짜를 년.월.일 형식으로 저장
    local_weekday2 = to_tomorrow.weekday()    #위에서  구한 날짜의 요일값을 저장
    schYmd = local_date2 #str
    
    num = local_weekday2 #int 0월1화2수3목4금5토6일
    # print(day)

    req = requests.get(f"http://stu.sen.go.kr/sts_sci_md01_001.do?schulCode=B100000662&schulCrseScCode=4&schulKndScCode=04&schMmealScCode=2&schYmd={schYmd}")
    soup = BeautifulSoup(req.text, "html.parser")
    element = soup.find_all("tr")
    element = element[2].find_all('td')

    element = element[num]
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
    data = element

    embed = discord.Embed(
            title='급식 정보', description='오늘 급식이야!', color=0xF2CB61)
    embed.add_field(name='🍽', value=f'{data}', inline=False)
    embed.set_footer(text='paka#8285')
    await ctx.send(embed=embed)


@client.command(name='급식내일', pass_context=True)
async def getInfoNextday(ctx):
    # now = str(datetime.datetime.now())
    # day = now[:4] + now[5:7] + now[8:10]
    to_tomorrow = datetime.datetime.today() + datetime.timedelta(days=1) + datetime.timedelta(days=1)    #오늘 날짜에 하루를 더함
    local_date2 = to_tomorrow.strftime("%Y.%m.%d")    #위에서 구한 날짜를 년.월.일 형식으로 저장
    local_weekday2 = to_tomorrow.weekday()    #위에서  구한 날짜의 요일값을 저장
    schYmd = local_date2 #str
    
    num = local_weekday2 #int 0월1화2수3목4금5토6일
    # print(day)

    req = requests.get(f"http://stu.sen.go.kr/sts_sci_md01_001.do?schulCode=B100000662&schulCrseScCode=4&schulKndScCode=04&schMmealScCode=2&schYmd={schYmd}")
    soup = BeautifulSoup(req.text, "html.parser")
    element = soup.find_all("tr")
    element = element[2].find_all('td')

    element = element[num]
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
    data = element

    embed = discord.Embed(
            title='급식 정보', description='내일 급식이야!', color=0xF2CB61)
    embed.add_field(name='🍽', value=f'{data}', inline=False)
    embed.set_footer(text='paka#8285')
    await ctx.send(embed=embed)


client.run("ODIzMzQ2MzM2MTkwNjkzNDA3.YFffBw.9_simUyqJPuBJ2DcAMyNjrMO5KU")
