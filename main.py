import discord
from discord.ext import commands
import asyncio
import os
from typing import Union
import requests
import datetime
import json
import os

client = commands.Bot(command_prefix='', help_command=None)
wait_for_reaction = dict()
wating_data = dict()
cooltimes = dict()
base_path = os.path.dirname(os.path.abspath(__file__))
path = base_path.replace('\\', '/') + '/' + 'savedschools.json'

f = open(base_path.replace('\\', '/') + '/' + 'key', 'r', encoding='utf-8')
key = f.read().strip()
f.close()


@client.event
async def on_ready():
    print(f'다음으로 로그인 합니다\n{client.user.name}')
    print(client.user.id)
    print('--------')
    await client.change_presence(activity=discord.Game(name='오늘급식 | 내일급식'))


def getSchoolInfo(school_name):
    url = f'https://open.neis.go.kr/hub/schoolInfo?KEY={key}&Type=json&SCHUL_NM={school_name}'
    try:
        response = requests.get(url)
        data = json.loads(response.text)
        if data['schoolInfo'][0]['head'][1]['RESULT']['CODE'] == 'INFO-000':
            return data
    except:
        return False


def getSchoolData(guildId):
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


class Register:
    ctx: commands.context.Context = None
    cache = None

    async def register(self, ctx, cache):
        self.ctx = ctx
        self.cache = cache

        count = len(cache['schoolInfo'][1]['row'])
        data = []

        for i in cache['schoolInfo'][1]['row']:
            print('----------')
            print('교육청 코드: ' + i['ATPT_OFCDC_SC_CODE'])
            print('교육청 이름: ' + i['ATPT_OFCDC_SC_NM'])
            print('학교 코드: ' + i['SD_SCHUL_CODE'])
            print('학교 이름: ' + i['SCHUL_NM'])
            print('학교 주소: ' + i['ORG_RDNMA'])
            print('----------')
            data.append((i['ATPT_OFCDC_SC_CODE'], i['ATPT_OFCDC_SC_NM'],
                        i['SD_SCHUL_CODE'], i['SCHUL_NM'], i['ORG_RDNMA']))

        wating_data[ctx.guild.id] = [0, count, data]

        embed = discord.Embed(
            title='학교 설정', description='정말 이 학교가 맞아?', color=0xFF7F50
        )

        embed.add_field(name='학교 이름', value=data[0][3])
        embed.add_field(name='학교 위치', value=data[0][4])
        embed.add_field(name='학교 코드', value=data[0][2])
        embed.add_field(name='시도교육청 이름', value=data[0][1])
        embed.add_field(name='시도교육청 코드', value=data[0][0])
        embed.set_footer(text='반응을 눌러 결정해주세요  /  paka#8285')
        msg = await ctx.send(embed=embed)

        wait_for_reaction[ctx.guild.id] = (ctx.author.id, msg.id, data)
        if count > 1:
            await msg.add_reaction('⭕')
            await msg.add_reaction('❌')
            await msg.add_reaction('➡️')
        else:
            await msg.add_reaction('⭕')
            await msg.add_reaction('❌')

        cooltimes[ctx.guild.id] = 10
        while cooltimes[ctx.guild.id] != 0:
            if not cooltimes.get(ctx.guild.id):
                return
            cooltimes[ctx.guild.id] = cooltimes[ctx.guild.id] - 1
            if not wait_for_reaction.get(ctx.guild.id):
                return
            await asyncio.sleep(1)

        wait_for_reaction.pop(ctx.guild.id)
        cooltimes.pop(ctx.guild.id)
        wating_data.pop(ctx.guild.id)
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
        embed.add_field(name='오직 관리자 권한을 가진 유저만 이 명령어를 사용할 수 있습니다',
                        value='관리자에게 부탁해 보세요..?')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    if wait_for_reaction.get(ctx.guild.id):
        embed = discord.Embed(
            title='에러...', description=' ', color=0xFF0000
        )
        embed.add_field(name='이미 서버에서 진행중인 작업이 있습니다',
                        value='작업이 끝날때까지 기다려주세요...')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    cache = getSchoolInfo(school)
    # print(cache)

    if cache == False:
        embed = discord.Embed(
            title='에러...', description=' ', color=0xFF0000
        )
        embed.add_field(name='정보를 가져오는데 문제가 발생했습니다', value='정확한 이름을 입력해주세요...')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
    else:
        await Register().register(ctx, cache)


@setSchool.error
async def setSchool_error(ctx: commands.context.Context, error: commands.CommandError):
    if isinstance(error, commands.MissingRequiredArgument):
        print('명령어 사용 오류')
        embed = discord.Embed(
            title='명령어 사용 에러...', description=' ', color=0xDC143C
        )
        embed.add_field(name='사용법', value='급식학교설정 [학교이름]')
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
                if reaction.emoji == '⭕':
                    wait_for_reaction.pop(reaction.message.guild.id)
                    cooltimes.pop(reaction.message.guild.id)
                    await reaction.message.delete()
                    json_data = dict()
                    try:
                        with open(path, 'r', encoding='utf-8') as file:
                            json_data = json.load(file)
                            file.close()
                    except FileNotFoundError as err:
                        print('파일이 존재하지 않습니다')
                    except json.decoder.JSONDecodeError as err:
                        print('올바른 Json 파일 형식이 아닙니다')

                    with open(path, 'w', encoding='utf-8') as file:
                        json_data[str(reaction.message.guild.id)] = [
                            msg[2][(wating_data[reaction.message.guild.id][0])][0], msg[2][(wating_data[reaction.message.guild.id][0])][2]]
                        json.dump(json_data, file, indent='\t')
                        file.close()

                    print(str(reaction.message.guild.id) +
                          ' / ' + '학교 설정: ' + msg[2][(wating_data[reaction.message.guild.id][0])][0] + ' | '+msg[2][(wating_data[reaction.message.guild.id][0])][2])

                    wating_data.pop(reaction.message.guild.id)
                    embed = discord.Embed(
                        title='성공!', description=' ', color=0x7FFF00
                    )
                    embed.add_field(name='서버의 학교 정보가 설정되었습니다!',
                                    value='『오늘급식』 을 입력해보아요!')
                    embed.set_footer(text='paka#8285')
                    await reaction.message.channel.send(embed=embed)
                elif reaction.emoji == '❌':
                    wait_for_reaction.pop(reaction.message.guild.id)
                    cooltimes.pop(reaction.message.guild.id)
                    wating_data.pop(reaction.message.guild.id)
                    await reaction.message.delete()

                    embed = discord.Embed(
                        title='작업 취소', description=' ', color=0xDC143C
                    )
                    embed.add_field(name='학교 설정 작업을 취소했습니다...',
                                    value='이걸 취소하네?!')
                    embed.set_footer(text='paka#8285')
                    await reaction.message.channel.send(embed=embed)
                elif reaction.emoji == '➡️':
                    cooltimes[reaction.message.guild.id] = 10
                    wating_data[reaction.message.guild.id][0] = (wating_data[
                        reaction.message.guild.id][0]+1) % wating_data[reaction.message.guild.id][1]
                    print('카운트 갱신: ', wating_data[reaction.message.guild.id][0])
                    embed = discord.Embed(
                        title='학교 설정', description='정말 이 학교가 맞아?', color=0xFF7F50
                    )
                    embed.add_field(
                        name='학교 이름', value=wating_data[reaction.message.guild.id][2][wating_data[reaction.message.guild.id][0]][3])
                    embed.add_field(
                        name='학교 위치', value=wating_data[reaction.message.guild.id][2][wating_data[reaction.message.guild.id][0]][4])
                    embed.add_field(
                        name='학교 코드', value=wating_data[reaction.message.guild.id][2][wating_data[reaction.message.guild.id][0]][2])
                    embed.add_field(
                        name='시도교육청 이름', value=wating_data[reaction.message.guild.id][2][wating_data[reaction.message.guild.id][0]][1])
                    embed.add_field(
                        name='시도교육청 코드', value=wating_data[reaction.message.guild.id][2][wating_data[reaction.message.guild.id][0]][0])
                    embed.set_footer(text='반응을 눌러 결정해주세요  /  paka#8285')
                    msg = await reaction.message.edit(embed=embed)


@client.command(name='오늘급식', pass_context=True)
async def getInfo(ctx: commands.context.Context):
    schoolData = getSchoolData(ctx.guild.id)

    if (schoolData == None):
        embed = discord.Embed(
            title='에러...', description='학교 정보를 찾을 수 없어...', color=0xDC143C
        )
        embed.add_field(
            name='사용하시기 전에...', value='『급식학교설정』 명령어로 설정해주세요!')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    nowDate = datetime.datetime.today()
    nowStr = str(nowDate)  # 다음날
    year = nowStr[:4]
    month = nowStr[5:7]
    date = nowStr[8:10]
    ymd = year+month+date
    num = nowDate.weekday()

    if num == 5:
        embed = discord.Embed(
            title='에러...', description=' ', color=0xDC143C
        )
        embed.add_field(name=f'{date}일 급식 정보를 가져올 수 없습니다...',
                        value='토요일에 급식이 나와..?')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return
    elif num == 6:
        embed = discord.Embed(
            title='에러...', description=' ', color=0xDC143C
        )
        embed.add_field(name=f'{date}일 급식 정보를 가져올 수 없습니다...',
                        value='일요일에 급식이 나와..?')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    url = f'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={key}&Type=json&ATPT_OFCDC_SC_CODE={schoolData[0]}&SD_SCHUL_CODE={schoolData[1]}&MLSV_YMD={ymd}'
    response = requests.get(url)
    school_menu = json.loads(response.text)

    if school_menu.get('mealServiceDietInfo') == None:
        embed = discord.Embed(
            title='에러...', description='', color=0xFFA500)
        embed.add_field(name=f'{date}일 급식 데이터를 조회하는 도중 오류가 발생했습니다.',
                        value='데이터를 불러오지 못했나봐요...', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    splited_data = school_menu['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'].split(
        '<br/>')
    data = ''
    for i in splited_data:
        data = data + '\n' + i

    data = data.strip()

    if data == '':
        embed = discord.Embed(
            title='에러...', description='', color=0xFFA500)
        embed.add_field(name=f'{date}일 급식 데이터를 조회하지 못했습니다...',
                        value='어째서..?', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='급식 정보', description='오늘 급식이야!', color=0xF2CB61)
        embed.add_field(name='🍽', value=f'{data}', inline=False)
        embed.set_footer(text=f'{month}월 {date}일 / paka#8285')
        await ctx.send(embed=embed)


@client.command(name='오급', pass_context=True)
async def getInfoShort(ctx: commands.context.Context):
    await getInfo(ctx)


@client.command(name='내일급식', pass_context=True)
async def getInfoNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 1, '내일')


@client.command(name='내급', pass_context=True)
async def getInfoNextdayShort(ctx: commands.context.Context):
    await getInfoNextday(ctx)


@client.command(name='내일모레급식', pass_context=True)
async def getInfoNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 2, '내일 모레')


@client.command(name='내일모레모레급식', pass_context=True)
async def getInfoNextNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 3, '내일 모레 모레')


@client.command(name='내일모레모레모레급식', pass_context=True)
async def getInfoNextNextNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 4, '내일 모레 모레 모레')


@client.command(name='내일모레모레모레모레급식', pass_context=True)
async def getInfoNextNextNextNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 5, '내일 모레 모레 모레 모레')


@client.command(name='내일모레모레모레모레모레급식', pass_context=True)
async def getInfoNextNextNextNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 6, '내일 모레 모레 모레 모레 모레')


@client.command(name='내일모레모레모레모레모레모레급식', pass_context=True)
async def getInfoNextNextNextNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 7, '내일 모레 모레 모레 모레 모레 모레')


async def findFoodData(ctx: commands.context.Context, dayAddAmount, msg):
    schoolData = getSchoolData(ctx.guild.id)

    if (schoolData == None):
        embed = discord.Embed(
            title='에러...', description='학교 정보를 찾을 수 없어...', color=0xDC143C
        )
        embed.add_field(
            name='사용하시기 전에...', value='『급식학교설정』 명령어로 설정해주세요!')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    nowDate = datetime.datetime.today() + datetime.timedelta(days=dayAddAmount)
    nowStr = str(nowDate)  # 다음날
    year = nowStr[:4]
    month = nowStr[5:7]
    date = nowStr[8:10]
    ymd = year+month+date
    num = nowDate.weekday()

    if num == 5:
        embed = discord.Embed(
            title='에러...', description=' ', color=0xDC143C
        )
        embed.add_field(name=f'{date}일 급식 정보를 가져올 수 없습니다...',
                        value='토요일에 급식이 나와..?')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return
    elif num == 6:
        embed = discord.Embed(
            title='에러...', description=' ', color=0xDC143C
        )
        embed.add_field(name=f'{date}일 급식 정보를 가져올 수 없습니다...',
                        value='일요일에 급식이 나와..?')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    url = f'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={key}&Type=json&ATPT_OFCDC_SC_CODE={schoolData[0]}&SD_SCHUL_CODE={schoolData[1]}&MLSV_YMD={ymd}'
    response = requests.get(url)
    school_menu = json.loads(response.text)

    if school_menu.get('mealServiceDietInfo') == None:
        embed = discord.Embed(
            title='에러...', description='', color=0xFFA500)
        embed.add_field(name=f'{date}일 급식 데이터를 조회하는 도중 오류가 발생했습니다.',
                        value='데이터를 불러오지 못했나봐요...', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    splited_data = school_menu['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'].split(
        '<br/>')
    data = ''
    for i in splited_data:
        data = data + '\n' + i

    data = data.strip()

    if data == '':
        embed = discord.Embed(
            title='에러...', description='', color=0xFFA500)
        embed.add_field(name=f'{date}일 급식 데이터를 조회하지 못했습니다...',
                        value='어째서..?', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            title='급식 정보', description=f'{msg} 급식이야!', color=0xFAEBD7)
        embed.add_field(name='🍽', value=f'{data}', inline=False)
        embed.set_footer(text=f'{month}월 {date}일 / paka#8285')
        await ctx.send(embed=embed)


client.run('ODIzMzQ2MzM2MTkwNjkzNDA3.YFffBw.9_simUyqJPuBJ2DcAMyNjrMO5KU')  # real
# client.run('NzM1MTA2NjA1NDM1MDYwMjI1.XxbbYA.qpDbsDm-8vxI5Gy7bvKGrfDg7Ac')  # test
