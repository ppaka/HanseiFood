from discord import app_commands, Interaction
from discord.ext import commands


class getLunchData(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='급식', description='해당 날짜의 급식을 가져옵니다')
    @app_commands.rename(date='date')
    @app_commands.describe(date='날짜를 yyyymmdd 형식으로 작성해주세요. (예: 20220505)')
    async def getDayLunch(self, interaction: Interaction, date: int) -> None:
        print('dsadsad')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        getLunchData(bot)
    )