import discord
import os
import asyncio
from discord.ext import commands
from pretty_help import EmojiMenu, PrettyHelp
from commands.configs.configs import Configs
import vt

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=Configs.prefix, help_command=PrettyHelp(),intents=intents)

os.system("clear")

@bot.event
async def on_ready():
    print(f'Logged in as: {bot.user.name} Version: {discord.__version__}')
    for guild in bot.guilds:
        print("Joined {}".format(guild.name))
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.listening, name=Configs.activitydescription))
    voice_channel = bot.get_channel(Configs.connectonstart)
    await voice_channel.connect()

@bot.event
async def on_member_join(member):
    try:
        channelmemberjoin = bot.get_channel(Configs.logsjoin)
        channelmemberjoin2 = bot.get_channel(Configs.logsjoin2)
        channelmemberrule = bot.get_channel(Configs.chanrule)
        guild = bot.get_guild(Configs.guild)
        role = guild.get_role(1138958621204549725)
        member_count = len([member for member in guild.members if role in member.roles])
        embedjoin = discord.Embed(title="Welcome", description=f"{member.mention} vient de nous rejoindre, Nous sommes désormais {member_count} !", color=0x000000)
        embedjoin.set_thumbnail(url=member.avatar.url)
        embedjoin.set_footer(text="fsociety00.dat")
        await channelmemberjoin2.send(embed=embedjoin)

        await channelmemberjoin.send(f"{member.mention} vient de nous rejoindre, Nous sommes désormais {member_count} !")
        attention = await channelmemberrule.send(f"{member.mention}")
        await asyncio.sleep(2)
        await attention.delete()
    except Exception as e:
        print(e)

async def load_extensions():
    for filename in os.listdir('./commands'):
        if filename.endswith('.py'):
            try:
                await bot.load_extension(f'commands.{filename[:-3]}')
                print(f'[+] {filename[:-3]} Loaded')
            except Exception as error:
                print(f'[-] {filename[:-3]} have a problem')
                print("An exception occurred:", error)


async def main():
    async with bot:
        await load_extensions()
        await bot.start(Configs.token)

asyncio.run(main())
