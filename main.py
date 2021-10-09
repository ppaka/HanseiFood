import asyncio
import os
from typing import NoReturn, Union
from warnings import catch_warnings
from discord import emoji, reaction
from discord.embeds import Embed
import requests
from bs4 import BeautifulSoup
import datetime
import re
import json

import discord
from discord.ext import commands

client = commands.Bot(command_prefix='!')
wait_for_reaction = dict()


@client.event
async def on_ready():
    print(f'다음으로 로그인 합니다\n{client.user.name}')
    print(client.user.id)
    print('--------')
    await client.change_presence(activity=discord.Game(name='!급식오늘 또는... !급식내일'))


def getSchoolInfo(school):
    url = f'https://schoolmenukr.ml/code/api?q={school}'
    try:
        response = requests.get(url)
        school_infos = json.loads(response.text)
        return (school_infos["school_infos"][0]["name"], school_infos["school_infos"][0]["address"], school_infos["school_infos"][0]["code"])
    except:
        return False


class Register:
    ctx: commands.context.Context = None
    cache: str = None

    async def register(self, ctx, cache):
        self.ctx = ctx
        self.cache = cache

        embed = discord.Embed(
            title='학교 설정', description='정말 이 학교가 맞아?', color=0xFF7F50
        )
        embed.add_field(name='학교 이름', value=cache[0])
        embed.add_field(name='학교 위치', value=cache[1])
        embed.add_field(name='학교 코드', value=cache[2])
        embed.set_footer(text='반응을 눌러 결정해주세요  /  paka#8285')
        msg = await ctx.send(embed=embed)

        wait_for_reaction[ctx.guild.id] = (
            ctx.author.id, msg.id, (cache[0], cache[1], cache[2]))
        await msg.add_reaction("⭕")
        await msg.add_reaction("❌")

        sec = 10
        while sec != 0:
            sec = sec - 1
            if not wait_for_reaction.get(ctx.guild.id):
                return
            await asyncio.sleep(1)

        wait_for_reaction.pop(ctx.guild.id)
        await msg.delete()
        embed = discord.Embed(
            title='작업 취소', description=' ', color=0xB22222
        )
        embed.add_field(name='타임아웃!', value='10초 안에 반응을 클릭해주세요')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)


@client.command(name='급식학교설정', pass_context=True)
async def setSchool(ctx: commands.context.Context, school: str):
    if not ctx.author.guild_permissions.administrator:
        embed = discord.Embed(
            title='에러...', description=' ', color=0xFF0000
        )
        embed.add_field(name='오직 관리자 권한을 가진 유저만 이 명령어를 사용할 수 있습니다...',
                        value='관리자에게 부탁해 보세요..?')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    if wait_for_reaction.get(ctx.guild.id):
        embed = discord.Embed(
            title='에러...', description=' ', color=0xFF0000
        )
        embed.add_field(name='이미 서버에서 진행중인 작업이 있습니다...',
                        value='작업이 끝날때까지 기다려주세요')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return
    cache = getSchoolInfo(school)

    if cache == False:
        embed = discord.Embed(
            title='에러...', description=' ', color=0xFF0000
        )
        embed.add_field(name='정보를 가져오는데 문제가 발생했습니다...', value='정확한 이름을 입력해주세요')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
    else:
        await Register().register(ctx, cache)


@setSchool.error
async def setSchool_error(ctx: commands.context.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title='명령어 사용 에러...', description=' ', color=0xDC143C
        )
        embed.add_field(
            name='사용법', value='!급식학교설정 "학교이름"')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: Union[discord.Member, discord.User]):
    if user.bot:
        return
    msg = wait_for_reaction.get(reaction.message.guild.id)
    if msg == None:
        return
    else:
        if user.id == msg[0]:
            if reaction.message.id == msg[1]:
                if reaction.emoji == "⭕":
                    wait_for_reaction.pop(reaction.message.guild.id)
                    await reaction.message.delete()
                    json_data = dict()
                    try:
                        with open(os.getcwd()+'\\savedschools.json', 'r', encoding='utf-8') as file:
                            json_data = json.load(file)
                            file.close()
                    except FileNotFoundError as err:
                        print("파일이 존재하지 않습니다")
                    except json.decoder.JSONDecodeError as err:
                        print("올바른 Json 파일 형식이 아닙니다")

                    with open(os.getcwd()+'\\savedschools.json', 'w', encoding='utf-8') as file:
                        json_data[str(reaction.message.guild.id)
                                  ] = str(msg[2][2])
                        json.dump(json_data, file, indent="\t")
                        file.close()

                    print(str(reaction.message.guild.id) +
                          " / " + "학교 설정: "+str(msg[2][2]))

                    embed = discord.Embed(
                        title='성공!', description=' ', color=0x7FFF00
                    )
                    embed.add_field(name='서버의 학교 정보가 설정되었습니다!',
                                    value='『!급식오늘』 을 입력해보아요!')
                    embed.set_footer(text='paka#8285')
                    await reaction.message.channel.send(embed=embed)
                elif reaction.emoji == "❌":
                    wait_for_reaction.pop(reaction.message.guild.id)
                    await reaction.message.delete()

                    embed = discord.Embed(
                        title='작업 취소', description=' ', color=0xDC143C
                    )
                    embed.add_field(name='학교 설정 작업을 취소했습니다...',
                                    value='이걸 취소하네?!')
                    embed.set_footer(text='paka#8285')
                    await reaction.message.channel.send(embed=embed)


def getSchoolCode(guildId):
    try:
        with open(os.getcwd()+'\\savedschools.json', 'r', encoding='utf-8') as file:
            json_data = json.load(file)
            file.close()
            return str(json_data[str(guildId)])
    except KeyError as err:
        print("설정되어지지 않은 서버")
        return None
    except FileNotFoundError as err:
        print("파일이 존재하지 않습니다")
        return None
    except json.decoder.JSONDecodeError as err:
        print("올바른 Json 파일 형식이 아닙니다")
        return None


@client.command(name='급식오늘', pass_context=True)
async def getInfo(ctx: commands.context.Context):
    # now = str(datetime.datetime.now())
    # day = now[:4] + now[5:7] + now[8:10]

    schoolCode = getSchoolCode(ctx.guild.id)

    if (schoolCode == None):
        embed = discord.Embed(
            title='에러...', description='학교 정보를 찾을 수 없어...', color=0xDC143C
        )
        embed.add_field(
            name='사용하시기 전에...', value='『!급식학교설정』 명령어로 설정해주세요!')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    to_tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)  # 오늘 날짜에 이틀을 더함
    realTomorrow = datetime.datetime.today()
    schYmd = realTomorrow.strftime("%Y.%m.%d")

    #local_date2 = to_tomorrow.strftime("%Y.%m.%d")  # 위에서 구한 날짜를 년.월.일 형식으로 저장
    local_weekday2 = to_tomorrow.weekday()  # 위에서  구한 날짜의 요일값을 저장
    #schYmd = local_date2  # str
    num = local_weekday2  # int 0월1화2수3목4금5토6일

    # 현실 날짜 읽을때는 항상 1일 빼서 읽기

    if num == 6:
        embed = discord.Embed(
            title='에러...', description=' ', color=0xDC143C
        )
        embed.add_field(name='토요일 급식 정보를 가져올 수 없습니다...',
                        value='토요일에 급식이 나와..?')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return
    elif num == 0:
        embed = discord.Embed(
            title='에러...', description=' ', color=0xDC143C
        )
        embed.add_field(name='일요일 급식 정보를 가져올 수 없습니다...',
                        value='일요일에 급식이 나와..?')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    req = requests.get(
        f"http://stu.sen.go.kr/sts_sci_md01_001.do?schulCode={schoolCode}&schulCrseScCode=4&schulKndScCode=04&schMmealScCode=2&schYmd={schYmd}")
    soup = BeautifulSoup(req.text, "html.parser")
    element = soup.find_all("tr")
    element = element[2].find_all('td')

    try:
        element = element[num]
    except IndexError:
        embed = discord.Embed(
            title='에러...', description='', color=0xFFA500)
        embed.add_field(name='급식 데이터를 조회하지 못했습니다...',
                        value='어째서..?', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

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
    element = element.replace('amp;', '')
    element = element.replace('@', '')
    data = element

    if data == ' ':
        embed = discord.Embed(
            title='에러...', description='', color=0xFFA500)
        embed.add_field(name='급식 데이터를 조회하지 못했습니다...',
                        value='어째서..?', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
    elif data == '':
        embed = discord.Embed(
            title='에러...', description='', color=0xFFA500)
        embed.add_field(name='급식 데이터를 조회하지 못했습니다...',
                        value='어째서..?', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='급식 정보', description='오늘 급식이야!', color=0xF2CB61)
        embed.add_field(name='🍽', value=f'{data}', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)


@client.command(name='급식내일', pass_context=True)
async def getInfoNextday(ctx: commands.context.Context):
    schoolCode = getSchoolCode(ctx.guild.id)

    if (schoolCode == None):
        embed = discord.Embed(
            title='에러...', description='학교 정보를 찾을 수 없어...', color=0xDC143C
        )
        embed.add_field(
            name='사용하시기 전에...', value='『!급식학교설정』 명령어로 설정해주세요!')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    to_tomorrow = datetime.datetime.today() + datetime.timedelta(days=2)  # 오늘 날짜에 이틀을 더함
    realTomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    schYmd = realTomorrow.strftime("%Y.%m.%d")

    #local_date2 = to_tomorrow.strftime("%Y.%m.%d")  # 위에서 구한 날짜를 년.월.일 형식으로 저장
    local_weekday2 = to_tomorrow.weekday()  # 위에서  구한 날짜의 요일값을 저장
    #schYmd = local_date2  # str
    num = local_weekday2  # int 0월1화2수3목4금5토6일

    # 현실 날짜 읽을때는 항상 1일 빼서 읽기

    if num == 6:
        embed = discord.Embed(
            title='에러...', description=' ', color=0xDC143C
        )
        embed.add_field(name='토요일 급식 정보를 가져올 수 없습니다...',
                        value='토요일에 급식이 나와..?')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return
    elif num == 0:
        embed = discord.Embed(
            title='에러...', description=' ', color=0xDC143C
        )
        embed.add_field(name='일요일 급식 정보를 가져올 수 없습니다...',
                        value='일요일에 급식이 나와..?')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    req = requests.get(
        f"http://stu.sen.go.kr/sts_sci_md01_001.do?schulCode={schoolCode}&schulCrseScCode=4&schulKndScCode=04&schMmealScCode=2&schYmd={schYmd}")
    soup = BeautifulSoup(req.text, "html.parser")
    element = soup.find_all("tr")
    element = element[2].find_all('td')

    try:
        element = element[num]
    except IndexError:
        embed = discord.Embed(
            title='에러...', description='', color=0xFFA500)
        embed.add_field(name='급식 데이터를 조회하지 못했습니다...',
                        value='어째서..?', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

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
    element = element.replace('amp;', '')
    element = element.replace('@', '')
    data = element

    if data == ' ':
        embed = discord.Embed(
            title='에러...', description='', color=0xFFA500)
        embed.add_field(name='급식 데이터를 조회하지 못했습니다...',
                        value='어째서..?', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
    elif data == '':
        embed = discord.Embed(
            title='에러...', description='', color=0xFFA500)
        embed.add_field(name='급식 데이터를 조회하지 못했습니다...',
                        value='어째서..?', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='급식 정보', description='내일 급식이야!', color=0xFAEBD7)
        embed.add_field(name='🍽', value=f'{data}', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)


# client.run("ODIzMzQ2MzM2MTkwNjkzNDA3.YFffBw.9_simUyqJPuBJ2DcAMyNjrMO5KU") #real
client.run("NzM1MTA2NjA1NDM1MDYwMjI1.XxbbYA.qpDbsDm-8vxI5Gy7bvKGrfDg7Ac")  # test
