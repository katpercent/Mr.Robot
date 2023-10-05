import discord
from discord.ext import commands, tasks
from commands.configs.configs import Configs
import asyncio
import yt_dlp as youtube_dl
import vt

class Members(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.updateonline.start()

    @tasks.loop(minutes=5)
    async def updateonline(self):
        guild = self.bot.get_guild(Configs.guild)
        voice_channel = guild.get_channel(Configs.onlinecompteur)
        
        online_members = sum(1 for member in guild.members if member.status == discord.Status.online)
        idle_members = sum(1 for member in guild.members if member.status == discord.Status.idle)
        dnd_members = sum(1 for member in guild.members if member.status == discord.Status.dnd)
        name = f"🟢 {online_members} ⛔️ {dnd_members} 🌙 {idle_members}"
        await voice_channel.edit(name=name)

    @updateonline.before_loop
    async def before_updateonline(self):
        await self.bot.wait_until_ready()

    async def update_channel_name(self, guild, role_id, channel_id):
        role = guild.get_role(role_id)
        channel = self.bot.get_channel(channel_id)
        member_count = len([member for member in guild.members if role in member.roles])
        await channel.edit(name=f'🎴・Membres : {member_count}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Update the channel name when a member joins
        await self.update_channel_name(member.guild, Configs.rolemember, Configs.membercompteur)

    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Update the channel name when a member leaves
        try:
            await self.update_channel_name(member.guild, Configs.rolemember, Configs.membercompteur)
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # Update the channel name when a member leaves
        try:
            channel = self.bot.get_channel(Configs.logsjoin)
            async for message in channel.history():
                for embed in message.embeds:
                    print(embed.description, member.id)
                    if f"{member.id}" in embed.description:
                        await message.delete()
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        # Update the channel name when a member's roles change
        if before.roles != after.roles:
            await self.update_channel_name(after.guild, Configs.rolemember, Configs.membercompteur)


    @commands.command(name='pp', description="récuperer la photo de profil", help="récuperer la photo de profil")
    async def pp(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title="Avatar", description=f"Avatar of {member.mention}", color=0x000000)
        embed.set_image(url=member.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name='openticket', description="Open a support ticket", help="Open a support ticket")
    async def openticket(self, ctx):
        overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.author: discord.PermissionOverwrite(read_messages=True),
            ctx.guild.get_role(Configs.supportticketrole): discord.PermissionOverwrite(read_messages=True)
        }
        ticket_channel = await ctx.guild.create_text_channel(
            f"ticket-{ctx.author.name}",
            category=bot.get_channel(Configs.categorytickets),
            overwrites=overwrites
        )
        embed = discord.Embed(
            title="Ticket Created",
            description=f"Hello {ctx.author.mention}, your ticket has been created in {ticket_channel.mention}."
                        " Please explain the reason for creating this ticket.",
            color=0x000000
        )
        await ticket_channel.send(embed=embed)
        await ctx.message.delete()

    @commands.command(name='verify', description="Verify user with a flag", help="Verify user with a flag")
    async def verify(self, ctx, flag: str):
        if flag == "flagofthectf":
            channel = self.bot.get_channel(Configs.sucessctf)
            role = ctx.guild.get_role(Configs.rolectf1)
            await ctx.message.delete()
            embed = discord.Embed(
                title="CTF #1",
                description=f"{ctx.author.mention} found the flag of the first ctf, you got a role.",
                color=0x000000
            )
            try:
                await channel.send(embed=embed)
                await ctx.author.add_roles(role)
            except:
                pass
        else:
            await ctx.message.delete()
            await ctx.send("You haven't found the flag.", delete_after=3)

async def setup(bot):
    await bot.add_cog(Members(bot))