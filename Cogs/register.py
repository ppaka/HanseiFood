import asyncio
from discord import app_commands, Interaction
from discord.ext import commands
import discord
import os
import json
from getSavedSchoolJsonPath import getSavedSchoolJsonPath
from schoolDataUtility import getSchoolInfo

NEIS_KEY = os.environ["NEIS_KEY"]
wait_for_reaction = dict()
waiting_data = dict()
cool_times = dict()


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="확인", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.stop()
        await interaction.response.defer()
        msg = wait_for_reaction.pop(interaction.guild_id)
        cool_times.pop(interaction.guild_id)
        json_data = dict()
        try:
            with open(getSavedSchoolJsonPath(), "r", encoding="utf-8") as file:
                json_data = json.load(file)
                file.close()
        except FileNotFoundError as err:
            print("파일이 존재하지 않습니다")
        except json.decoder.JSONDecodeError as err:
            print("올바른 Json 파일 형식이 아닙니다")
        with open(getSavedSchoolJsonPath(), "w", encoding="utf-8") as file:
            json_data[str(interaction.guild_id)] = [
                msg[2][(waiting_data[interaction.guild_id][0])][0],
                msg[2][(waiting_data[interaction.guild_id][0])][2],
            ]
            json.dump(json_data, file, indent="\t")
            file.close()
        print(
            str(interaction.guild_id)
            + " / "
            + "학교 설정: "
            + msg[2][(waiting_data[interaction.guild_id][0])][0]
            + " | "
            + msg[2][(waiting_data[interaction.guild_id][0])][2]
        )
        waiting_data.pop(interaction.guild_id)
        embed = discord.Embed(title="성공!", description=" ", color=0x7FFF00)
        embed.add_field(name="서버의 학교 정보가 설정되었습니다!", value="『오늘급식』 을 입력해보아요!")
        embed.set_footer(text="ppaka")
        await interaction.edit_original_response(embed=embed, view=None)

    @discord.ui.button(label="취소", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        await interaction.response.defer()
        wait_for_reaction.pop(interaction.guild_id)
        cool_times.pop(interaction.guild_id)
        waiting_data.pop(interaction.guild_id)

        embed = discord.Embed(title="작업 취소", description=" ", color=0xDC143C)
        embed.add_field(name="학교 설정 작업을 취소했습니다.", value="")
        embed.set_footer(text="ppaka")
        await interaction.edit_original_response(embed=embed, view=None)


class ConfirmNext(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="확인", style=discord.ButtonStyle.green)
    async def confirm(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        self.stop()
        await interaction.response.defer()
        cool_times.pop(interaction.guild_id)
        json_data = dict()
        msg = wait_for_reaction.pop(interaction.guild_id)
        try:
            with open(getSavedSchoolJsonPath(), "r", encoding="utf-8") as file:
                json_data = json.load(file)
                file.close()
        except FileNotFoundError as err:
            print("파일이 존재하지 않습니다")
        except json.decoder.JSONDecodeError as err:
            print("올바른 Json 파일 형식이 아닙니다")
        with open(getSavedSchoolJsonPath(), "w", encoding="utf-8") as file:
            json_data[str(interaction.guild_id)] = [
                msg[2][(waiting_data[interaction.guild_id][0])][0],
                msg[2][(waiting_data[interaction.guild_id][0])][2],
            ]
            json.dump(json_data, file, indent="\t")
            file.close()
        print(
            str(interaction.guild_id)
            + " / "
            + "학교 설정: "
            + msg[2][(waiting_data[interaction.guild_id][0])][0]
            + " | "
            + msg[2][(waiting_data[interaction.guild_id][0])][2]
        )
        waiting_data.pop(interaction.guild_id)
        embed = discord.Embed(title="성공!", description=" ", color=0x7FFF00)
        embed.add_field(name="서버의 학교 정보가 설정되었습니다!", value="『오늘급식』 을 입력해보아요!")
        embed.set_footer(text="ppaka")
        await interaction.edit_original_response(embed=embed, view=None)

    @discord.ui.button(label="취소", style=discord.ButtonStyle.red)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        await interaction.response.defer()
        wait_for_reaction.pop(interaction.guild_id)
        cool_times.pop(interaction.guild_id)
        waiting_data.pop(interaction.guild_id)

        embed = discord.Embed(title="작업 취소", description=" ", color=0xDC143C)
        embed.add_field(name="학교 설정 작업을 취소했습니다.", value="")
        embed.set_footer(text="ppaka")
        await interaction.edit_original_response(embed=embed, view=None)

    @discord.ui.button(label="다음", style=discord.ButtonStyle.secondary)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        cool_times[interaction.guild_id] = 10
        waiting_data[interaction.guild_id][0] = (
            waiting_data[interaction.guild_id][0] + 1
        ) % waiting_data[interaction.guild_id][1]
        # print('카운트 갱신: ', waiting_data[interaction.guild_id][0])
        embed = discord.Embed(title="학교 설정", description="정말 이 학교가 맞아?", color=0xFF7F50)
        embed.add_field(
            name="학교 이름",
            value=waiting_data[interaction.guild_id][2][
                waiting_data[interaction.guild_id][0]
            ][3],
        )
        embed.add_field(
            name="학교 위치",
            value=waiting_data[interaction.guild_id][2][
                waiting_data[interaction.guild_id][0]
            ][4],
        )
        embed.add_field(
            name="학교 코드",
            value=waiting_data[interaction.guild_id][2][
                waiting_data[interaction.guild_id][0]
            ][2],
        )
        embed.add_field(
            name="시도교육청 이름",
            value=waiting_data[interaction.guild_id][2][
                waiting_data[interaction.guild_id][0]
            ][1],
        )
        embed.add_field(
            name="시도교육청 코드",
            value=waiting_data[interaction.guild_id][2][
                waiting_data[interaction.guild_id][0]
            ][0],
        )
        embed.set_footer(text="반응을 눌러 결정해주세요  /  ppaka")
        await interaction.edit_original_response(embed=embed)


class register(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="학교설정", description="급식봇을 이용하기 위해 학교를 등록합니다!")
    @app_commands.rename(sch_name="school_name")
    @app_commands.describe(sch_name="학교이름")
    async def request_get(self, interaction: Interaction, sch_name: str) -> None:
        await interaction.response.defer(ephemeral=False)

        if type(interaction.user) != discord.Member:
            raise TypeError("interaction.user is not User Type")

        if not interaction.user.guild_permissions.administrator:
            embed = discord.Embed(title="에러...", description=" ", color=0xFF0000)
            embed.add_field(
                name="오직 관리자 권한을 가진 유저만 이 명령어를 사용할 수 있습니다.", value="서버 관리자에게 부탁해보세요!"
            )
            embed.set_footer(text="ppaka")
            await interaction.edit_original_response(embed=embed)
            return

        if wait_for_reaction.get(interaction.guild_id):
            embed = discord.Embed(title="에러...", description=" ", color=0xFF0000)
            embed.add_field(name="이미 서버에서 진행중인 작업이 있습니다.", value="작업이 끝날때까지 기다려주세요...")
            embed.set_footer(text="ppaka")
            await interaction.edit_original_response(embed=embed)
            return

        school_info = getSchoolInfo(NEIS_KEY, sch_name)

        if school_info == None:
            embed = discord.Embed(title="에러...", description=" ", color=0xFF0000)
            embed.add_field(name="데이터를 가져오는데 문제가 발생했습니다.", value="")
            embed.set_footer(text="ppaka")
            await interaction.edit_original_response(embed=embed)
            return

        count = len(school_info["schoolInfo"][1]["row"])  # type: ignore
        data = []

        for i in school_info["schoolInfo"][1]["row"]:  # type: ignore
            # print('----------')
            # print('교육청 코드: ' + i['ATPT_OFCDC_SC_CODE'])
            # print('교육청 이름: ' + i['ATPT_OFCDC_SC_NM'])
            # print('학교 코드: ' + i['SD_SCHUL_CODE'])
            # print('학교 이름: ' + i['SCHUL_NM'])
            # print('학교 주소: ' + i['ORG_RDNMA'])
            # print('----------')
            data.append(
                (
                    i["ATPT_OFCDC_SC_CODE"],  # type: ignore
                    i["ATPT_OFCDC_SC_NM"],  # type: ignore
                    i["SD_SCHUL_CODE"],  # type: ignore
                    i["SCHUL_NM"],  # type: ignore
                    i["ORG_RDNMA"],  # type: ignore
                )
            )

        waiting_data[interaction.guild_id] = [0, count, data, "waiting"]

        embed = discord.Embed(title="학교 설정", description="정말 이 학교가 맞아?", color=0xFF7F50)
        embed.add_field(name="학교 이름", value=data[0][3])
        embed.add_field(name="학교 위치", value=data[0][4])
        embed.add_field(name="학교 코드", value=data[0][2])
        embed.add_field(name="시도교육청 이름", value=data[0][1])
        embed.add_field(name="시도교육청 코드", value=data[0][0])
        embed.set_footer(text="버튼을 눌러 결정해주세요  /  ppaka")
        wait_for_reaction[interaction.guild_id] = (
            interaction.user.id,
            interaction.guild_id,
            data,
        )

        if count == 1:
            view = Confirm()
        else:
            view = ConfirmNext()
        await interaction.edit_original_response(embed=embed, view=view)

        cool_times[interaction.guild_id] = 10
        while cool_times.get(interaction.guild_id) != 0:
            if not cool_times.get(interaction.guild_id):
                return
            cool_times[interaction.guild_id] -= 1
            if not wait_for_reaction.get(interaction.guild_id):
                return
            await asyncio.sleep(1)

        if not cool_times.get(interaction.guild_id):
            return

        wait_for_reaction.pop(interaction.guild_id)
        cool_times.pop(interaction.guild_id)
        waiting_data.pop(interaction.guild_id)
        embed = discord.Embed(title="작업 취소", description=" ", color=0xB22222)
        embed.add_field(name="타임아웃!", value="10초 안에 반응을 클릭해주세요...")
        embed.set_footer(text="ppaka")
        await interaction.edit_original_response(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(register(bot))
