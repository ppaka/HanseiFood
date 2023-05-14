import json
from discord import app_commands, Interaction
import discord
from discord.ext import commands
import requests
import os

from schoolDataUtility import getSchoolData


NEIS_KEY = os.environ['NEIS_KEY']


class getLunchData(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='급식', description='해당 날짜의 급식을 가져옵니다')
    @app_commands.rename(yyyymmdd='date')
    @app_commands.describe(yyyymmdd='날짜를 yyyymmdd 형식으로 작성해주세요. (예: 20220505)')
    async def getDayLunch(self, interaction: Interaction, yyyymmdd: int) -> None:
        await interaction.response.defer(ephemeral=False)
        schoolData = getSchoolData(interaction.guild_id)

        if schoolData == None:
            embed = discord.Embed(
                title='에러...', description='학교 정보를 찾을 수 없어...', color=0xDC143C
            )
            embed.add_field(
                name='사용하시기 전에...', value='『/급식학교설정』 명령어로 설정해주세요!')
            embed.set_footer(text='paka#8285')
            await interaction.edit_original_response(embed=embed)
            return

        ymd = str(yyyymmdd)
        url = f'https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={NEIS_KEY}&Type=json&ATPT_OFCDC_SC_CODE={schoolData[0]}&SD_SCHUL_CODE={schoolData[1]}&MLSV_YMD={ymd}'
        response = requests.get(url)
        school_menu = json.loads(response.text)

        if school_menu.get('mealServiceDietInfo') == None:
            embed = discord.Embed(
                title='에러...', description='', color=0xFFA500)
            embed.add_field(name=f'{ymd} 급식 데이터를 조회하는 도중 오류가 발생했습니다.',
                            value='데이터를 불러오지 못했나봐요...', inline=False)
            embed.set_footer(text='paka#8285')
            await interaction.edit_original_response(embed=embed)
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
            embed.add_field(name=f'{ymd} 급식 데이터를 조회하지 못했습니다...',
                            value='어째서..?', inline=False)
            embed.set_footer(text='paka#8285')
            await interaction.edit_original_response(embed=embed)
        else:
            embed = discord.Embed(
                title='급식 정보', description=f'급식이야!', color=0xFAEBD7)
            embed.add_field(name='🍽', value=f'{data}', inline=False)
            embed.set_footer(text=f'YMD:{ymd} / paka#8285')
            await interaction.edit_original_response(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        getLunchData(bot)
    )
