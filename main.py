import datetime
import json
import os
import discord
import random
from discord import *
from discord import Intents
from discord.ext import commands
from discord import Game
from discord import Status
import requests
from schoolDataUtility import *

NEIS_KEY = os.environ['NEIS_KEY']
APP_ID = '823346336190693407'
DISCORD_TOKEN = os.environ['DISCORD_TOKEN']

intents = Intents.default()
intents.message_content = True


class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='',
            intents=intents,
            sync_command=True,
            application_id=APP_ID
        )
        self.initial_extension = [
            'Cogs.register',
            'Cogs.getLunchData'
        ]

    async def setup_hook(self):
        for ext in self.initial_extension:
            await self.load_extension(ext)
        await bot.tree.sync()

    async def on_command_error(self, context: commands.context.Context, exception, /) -> None:
        # if '내모모모모모모모급' in context.message.content:
        #     print('명령어 오류')
        if type(exception) != commands.errors.CommandNotFound:
            return await super().on_command_error(context, exception)

    async def on_ready(self):
        print('login as')
        print(self.user.name)
        print(self.user.id)
        print('===============')
        game = Game('급식실 앞에서 손소독')
        await self.change_presence(status=Status.online, activity=game)


async def findFoodData(ctx: commands.context.Context, dayAddAmount, msg):
    schoolData = getSchoolData(ctx.guild.id)

    if schoolData == None:
        embed = discord.Embed(
            title='오류 발생!', description='학교 정보를 찾을 수 없어...', color=0xDC143C
        )
        embed.add_field(
            name='사용하시기 전에...', value='『/학교설정』 명령어로 설정해주세요!')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    isToday = dayAddAmount == 0
    if isToday:
        nowDate = datetime.datetime.today()
    else:
        nowDate = datetime.datetime.today() + datetime.timedelta(days=dayAddAmount)
    nowStr = str(nowDate)
    year = nowStr[:4]
    month = nowStr[5:7]
    date = nowStr[8:10]
    ymd = year+month+date
    num = nowDate.weekday()

    if num == 5 or num == 6:
        embed = discord.Embed(
            title='오류 발생!', description=' ', color=0xDC143C
        )

        dayString = '토'
        if num == 6:
            dayString = '일'

        if random.randrange(0, 2) == 1:
            embed.add_field(name=f'{date}일 급식 정보를 가져오지 못했다구!',
                            value=f'{dayString}요일에 급식이 나온다고 생각하는거야?!')
        else:
            embed.add_field(name=f'{date}일 급식 정보를 가져올 수 없습니다...',
                            value=f'{dayString}요일에 급식이 나와..?')
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    url = f'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={NEIS_KEY}&Type=json&ATPT_OFCDC_SC_CODE={schoolData[0]}&SD_SCHUL_CODE={schoolData[1]}&MLSV_YMD={ymd}'
    response = requests.get(url)
    school_menu = json.loads(response.text)

    if school_menu.get('mealServiceDietInfo') == None:
        embed = discord.Embed(
            title='오류 발생!', description='', color=0xFFA500)
        embed.add_field(name=f'{date}일 급식 데이터를 조회하는 도중 오류가 발생했습니다.',
                        value='데이터를 불러오지 못했나봐요...', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
        return

    splited_data = school_menu['mealServiceDietInfo'][1]['row'][0]['DDISH_NM'].split(
        '<br/>')
    data = ''
    for i in splited_data:
        data = data + '\n' + i.strip()

    data = data.strip()

    if data == '':
        embed = discord.Embed(
            title='오류 발생!', description='', color=0xFFA500)
        embed.add_field(name=f'{date}일 급식 데이터를 조회하지 못했습니다...',
                        value='어째서..?', inline=False)
        embed.set_footer(text='paka#8285')
        await ctx.send(embed=embed)
    else:
        if isToday:
            color = 0xF2CB61
        else:
            if dayAddAmount > 0:
                color = 0xFAEBD7
            else:
                color = 0xFFA7A7

        embed = discord.Embed(
            title='급식 정보', description=f'{msg} 급식이야!', color=color)
        embed.add_field(name='🍽', value=f'{data}', inline=False)
        embed.set_footer(text=f'{month}월 {date}일 / paka#8285')
        await ctx.send(embed=embed)


bot = MyBot()


@bot.command(name='어제급식', pass_context=True, aliases=['어급'])
async def getInfoLastday(ctx: commands.context.Context):
    await findFoodData(ctx, -1, '어제')


@bot.command(name='오늘급식', pass_context=True, aliases=['오급'])
async def getInfo(ctx: commands.context.Context):
    await findFoodData(ctx, 0, '오늘')


@bot.command(name='내일급식', pass_context=True, aliases=['내급'])
async def getInfoNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 1, '내일')


@bot.command(name='내일모레급식', pass_context=True, aliases=['내모급'])
async def getInfoNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 2, '내일 모레')


@bot.command(name='내일모레모레급식', pass_context=True, aliases=['내모모급'])
async def getInfoNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 3, '내일 모레 모레')


@bot.command(name='내일모레모레모레급식', pass_context=True, aliases=['내모모모급'])
async def getInfoNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 4, '내일 모레 모레 모레')


@bot.command(name='내일모레모레모레모레급식', pass_context=True, aliases=['내모모모모급'])
async def getInfoNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 5, '내일 모레 모레 모레 모레')


@bot.command(name='내일모레모레모레모레모레급식', pass_context=True, aliases=['내모모모모모급'])
async def getInfoNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 6, '내일 모레 모레 모레 모레 모레')


@bot.command(name='내일모레모레모레모레모레모레급식', pass_context=True, aliases=['내모모모모모모급'])
async def getInfoNextNextday(ctx: commands.context.Context):
    await findFoodData(ctx, 7, '내일 모레 모레 모레 모레 모레 모레')

bot.run(token=DISCORD_TOKEN)
