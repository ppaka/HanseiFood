import asyncio
from discord import app_commands, Interaction
from discord.ext import commands
from discord.ui import Button, View
from discord import ButtonStyle
import discord
import dotenv, os, json
from schoolDataUtility import getSchoolInfo

dotenv.load_dotenv()
NIES_KEY = os.getenv('NIES_KEY')
wait_for_reaction = dict()
wating_data = dict()
cooltimes = dict()
base_path = os.path.dirname(os.path.abspath(__file__))
path = base_path.replace('\\', '/') + '/..' + '/' + 'savedschools.json'


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='확인', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        await interaction.response.defer()
        msg = wait_for_reaction.pop(interaction.guild_id)
        cooltimes.pop(interaction.guild_id)
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
            json_data[str(interaction.guild_id)] = [
                msg[2][(wating_data[interaction.guild_id][0])][0], 
                msg[2][(wating_data[interaction.guild_id][0])][2]]
            json.dump(json_data, file, indent='\t')
            file.close()
        print(str(interaction.guild_id) +
            ' / ' + '학교 설정: ' + msg[2][(wating_data[interaction.guild_id][0])][0] 
            + ' | '+msg[2][(wating_data[interaction.guild_id][0])][2])
        wating_data.pop(interaction.guild_id)
        embed = discord.Embed(
            title='성공!', description=' ', color=0x7FFF00
        )
        embed.add_field(name='서버의 학교 정보가 설정되었습니다!',
                        value='『오늘급식』 을 입력해보아요!')
        embed.set_footer(text='paka#8285')
        await interaction.edit_original_response(embed=embed, view=None)

    @discord.ui.button(label='취소', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        await interaction.response.defer()
        wait_for_reaction.pop(interaction.guild_id)
        cooltimes.pop(interaction.guild_id)
        wating_data.pop(interaction.guild_id)
        
        embed = discord.Embed(
            title='작업 취소', description=' ', color=0xDC143C
        )
        embed.add_field(name='학교 설정 작업을 취소했습니다...',
                        value='이걸 취소하네?!')
        embed.set_footer(text='paka#8285')
        await interaction.edit_original_response(embed=embed, view=None)


class ConfirmNext(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label='확인', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        await interaction.response.defer()
        cooltimes.pop(interaction.guild_id)
        json_data = dict()
        msg = wait_for_reaction.pop(interaction.guild_id)
        try:
            with open(path, 'r', encoding='utf-8') as file:
                json_data = json.load(file)
                file.close()
        except FileNotFoundError as err:
            print('파일이 존재하지 않습니다')
        except json.decoder.JSONDecodeError as err:
            print('올바른 Json 파일 형식이 아닙니다')
        with open(path, 'w', encoding='utf-8') as file:
            json_data[str(interaction.guild_id)] = [
                msg[2][(wating_data[interaction.guild_id][0])][0], 
                msg[2][(wating_data[interaction.guild_id][0])][2]]
            json.dump(json_data, file, indent='\t')
            file.close()
        print(str(interaction.guild_id) +
            ' / ' + '학교 설정: ' + msg[2][(wating_data[interaction.guild_id][0])][0] 
            + ' | '+msg[2][(wating_data[interaction.guild_id][0])][2])
        wating_data.pop(interaction.guild_id)
        embed = discord.Embed(
            title='성공!', description=' ', color=0x7FFF00
        )
        embed.add_field(name='서버의 학교 정보가 설정되었습니다!',
                        value='『오늘급식』 을 입력해보아요!')
        embed.set_footer(text='paka#8285')
        await interaction.edit_original_response(embed=embed, view=None)

    @discord.ui.button(label='취소', style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        await interaction.response.defer()
        wait_for_reaction.pop(interaction.guild_id)
        cooltimes.pop(interaction.guild_id)
        wating_data.pop(interaction.guild_id)
        
        embed = discord.Embed(
            title='작업 취소', description=' ', color=0xDC143C
        )
        embed.add_field(name='학교 설정 작업을 취소했습니다...',
                        value='이걸 취소하네?!')
        embed.set_footer(text='paka#8285')
        await interaction.edit_original_response(embed=embed, view=None)

    @discord.ui.button(label='다음', style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        cooltimes[interaction.guild_id] = 10
        wating_data[interaction.guild_id][0] = (wating_data[
            interaction.guild_id][0]+1) % wating_data[interaction.guild_id][1]
        # print('카운트 갱신: ', wating_data[interaction.guild_id][0])
        embed = discord.Embed(
            title='학교 설정', description='정말 이 학교가 맞아?', color=0xFF7F50
        )
        embed.add_field(
            name='학교 이름', value=wating_data[interaction.guild_id][2][wating_data[interaction.guild_id][0]][3])
        embed.add_field(
            name='학교 위치', value=wating_data[interaction.guild_id][2][wating_data[interaction.guild_id][0]][4])
        embed.add_field(
            name='학교 코드', value=wating_data[interaction.guild_id][2][wating_data[interaction.guild_id][0]][2])
        embed.add_field(
            name='시도교육청 이름', value=wating_data[interaction.guild_id][2][wating_data[interaction.guild_id][0]][1])
        embed.add_field(
            name='시도교육청 코드', value=wating_data[interaction.guild_id][2][wating_data[interaction.guild_id][0]][0])
        embed.set_footer(text='반응을 눌러 결정해주세요  /  paka#8285')
        await interaction.edit_original_response(embed=embed)

class register(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='학교설정', description='급식봇을 이용하기 위해 학교를 등록합니다!')
    @app_commands.rename(sch_name='school_name')
    @app_commands.describe(sch_name='학교이름')
    async def request_get(self, interaction: Interaction, sch_name: str) -> None:
        await interaction.response.defer(ephemeral=False)
        school_info = getSchoolInfo(NIES_KEY, sch_name)

        if school_info == False:
            embed = discord.Embed(
            title='에러...', description=' ', color=0xFF0000
            )
            embed.add_field(name='정보를 가져오는데 문제가 발생했습니다', value='정확한 이름을 입력해주세요...')
            embed.set_footer(text='paka#8285')
            await interaction.edit_original_response(embed=embed)
            return

        count = len(school_info['schoolInfo'][1]['row'])
        data = []

        for i in school_info['schoolInfo'][1]['row']:
            # print('----------')
            # print('교육청 코드: ' + i['ATPT_OFCDC_SC_CODE'])
            # print('교육청 이름: ' + i['ATPT_OFCDC_SC_NM'])
            # print('학교 코드: ' + i['SD_SCHUL_CODE'])
            # print('학교 이름: ' + i['SCHUL_NM'])
            # print('학교 주소: ' + i['ORG_RDNMA'])
            # print('----------')
            data.append((i['ATPT_OFCDC_SC_CODE'], i['ATPT_OFCDC_SC_NM'],
                        i['SD_SCHUL_CODE'], i['SCHUL_NM'], i['ORG_RDNMA']))

        wating_data[interaction.guild_id] = [0, count, data, 'waiting']

        embed = discord.Embed(title='학교 설정', description='정말 이 학교가 맞아?', color=0xFF7F50)
        embed.add_field(name='학교 이름', value=data[0][3])
        embed.add_field(name='학교 위치', value=data[0][4])
        embed.add_field(name='학교 코드', value=data[0][2])
        embed.add_field(name='시도교육청 이름', value=data[0][1])
        embed.add_field(name='시도교육청 코드', value=data[0][0])
        embed.set_footer(text='버튼을 눌러 결정해주세요  /  paka#8285')
        wait_for_reaction[interaction.guild_id] = (interaction.user.id, interaction.guild_id, data)

        if count == 1:
            view = Confirm()
        else:
            view = ConfirmNext()
        await interaction.edit_original_response(embed=embed, view=view)

        cooltimes[interaction.guild_id] = 10
        while cooltimes.get(interaction.guild_id) != 0:
            if not cooltimes.get(interaction.guild_id):
                return
            cooltimes[interaction.guild_id] -= 1
            if not wait_for_reaction.get(interaction.guild_id):
                return
            await asyncio.sleep(1)

        if not cooltimes.get(interaction.guild_id):
            return

        wait_for_reaction.pop(interaction.guild_id)
        cooltimes.pop(interaction.guild_id)
        wating_data.pop(interaction.guild_id)
        embed = discord.Embed(title='작업 취소', description=' ', color=0xB22222)
        embed.add_field(name='타임아웃!', value='10초 안에 반응을 클릭해주세요')
        embed.set_footer(text='paka#8285')
        await interaction.edit_original_response(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        register(bot)
    )
