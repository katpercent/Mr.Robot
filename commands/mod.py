import datetime
import asyncio
import discord
from discord.ext import commands
from pretty_help import EmojiMenu, PrettyHelp

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clear', description="Clear un nombre de message définis.", help="Clear un nombre de message définis.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=0):
        if amount > 0:
            await ctx.channel.purge(limit=amount + 1)
            success = await ctx.send(f"[+] {amount} messages has been deleted...")
            await success.add_reaction("✅")
            await asyncio.sleep(6)
            await success.delete()

    @commands.command(name='ban', description="ban", help="t'es con ou quoi")
    @commands.has_permissions(ban_members = True)    
    async def ban(self, ctx, member : discord.Member, reason=None):
        try:
            if reason == None:
                reason = "For being a jerk or a skid! (None)"
            await member.ban(reason = reason)
            success = await ctx.send(f"{member} has been ban from {ctx.guild.name} for {reason}")
            await member.send(f"{member} has been ban from {ctx.guild.name} for {reason}")
            await success.add_reaction("✅")
        except Exception as e:
            print(e)
        

async def setup(bot):
    await bot.add_cog(Mod(bot))