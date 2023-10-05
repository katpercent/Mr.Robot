import datetime
import asyncio
import discord
import random
from discord.ext import commands, tasks
from pretty_help import EmojiMenu, PrettyHelp
from commands.configs.configs import Configs

class Ticketsbutton(discord.ui.View): 
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Open a Ticket")
        async def openticket(self, interaction: discord.Interaction, Button: discord.ui.Button):
            try:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    interaction.user: discord.PermissionOverwrite(read_messages=True),
                    interaction.guild.get_role(Configs.supportticketrole): discord.PermissionOverwrite(read_messages=True)
                }
                ticket_channel = await interaction.guild.create_text_channel(
                    f"ticket-{interaction.user.name}",
                    category= interaction.guild.get_channel(Configs.categorytickets),
                    overwrites=overwrites
                )
                embed = discord.Embed(
                    title="Ticket Created",
                    description=f"Hello {interaction.user.mention}, your ticket has been created in {ticket_channel.mention}."
                                " Please explain the reason for creating this ticket.",
                    color=0x000000
                )
                await ticket_channel.send(embed=embed)
            except Exception as e:
                print(e)

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='tickets', description="Send a embed with a button for open a ticket.", help="Send a embed with a button for open a ticket.")
    async def tickets(self, ctx):
        embed = discord.Embed(title="Tickets", description="Contactez l'administration du serveur en appuyant sur le bouton.", color=0x000000)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/mrrobot/images/8/87/ECorp.png")
        embed.add_field(name="Si le bouton ne fonctionnent plus, exécuter cette commande :", value=Configs.prefix+"openticket", inline=False)
        embed.set_image(url="https://i.imgur.com/oSeKEHG.jpeg")
        embed.set_footer(text="fsociety07.dat")
        await ctx.send(embed=embed, view=Ticketsbutton())
        await ctx.message.delete()

    @commands.command(name='giveaway', description="Start a giveaway", help="option : duration: int in hour and prize: str")
    @commands.is_owner()
    async def giveaway(self, ctx, duration: int, *, prize: str):
        embedgw = discord.Embed(title="Giveaway", description=f"React with ✅ to participate!\n\nPrize: {prize}\n\nTime left: {duration} min", color=0x000000)
        embedgw.set_footer(text=f"Hosted by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        giveaway_msg = await ctx.send(embed=embedgw)
        await giveaway_msg.add_reaction("✅")
        await ctx.message.delete()
        await asyncio.sleep(duration * 3600)
        giveaway_msg = await ctx.channel.fetch_message(giveaway_msg.id)
        participants = []
        async for user in giveaway_msg.reactions[0].users():
            if not user.bot:
                participants.append(user)
        if len(participants) <= 1:
            embednowin = discord.Embed(title="Giveaway Ended", description="Not enough participants. No winner.", color=0xFF0000)
            await ctx.send(embed=embednowin)
            return
        winner = random.choice(participants)
        embedwin = discord.Embed(title="Giveaway Ended", description=f"Winner: {winner.mention}\n\nPrize: {prize}", color=0x00FF00)
        embedwin.set_footer(text=f"Hosted by {ctx.author.display_name}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embedwin)

    @commands.command(name='massrole', description="Ajoute un rôle à tout le monde", help="Ajoute un rôle à tout le monde")
    @commands.is_owner()
    async def massrole(self, ctx, role: discord.Role):
        for member in ctx.guild.members:
            try:
                await member.add_roles(role)
            except:
                pass

    """
    @commands.command(name='massdm', description="Envoie une pub a tout le monde.", help="Envoie une pub a tout le monde.")
    async def massdm(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(title="Evil Corp", description="Evil Corp is an exciting community hub where cybersecurity experts, technology enthusiasts come together to exchange knowledge, share advice, discuss cyber security, and make ctf.", color=0x000000)
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        embed.set_thumbnail(url="https://static.wikia.nocookie.net/mrrobot/images/8/87/ECorp.png")
        embed.add_field(name="Link to join.", value="https://discord.gg/evilcorp", inline=False)
        embed.set_image(url="https://i.imgur.com/oSeKEHG.jpeg")
        embed.set_footer(text="fsociety.dat")
        for member in ctx.guild.members:
            if member.id == 622541545916334080 or member.id == 431502422431760394 or member.id == 355402435893919754:
                pass
            else :
                try:
                    await member.send(embed=embed)
                except:
                    pass
    """

    @commands.command(name='stock', description="Stock for the tools", help="Stock for the tools")
    @commands.is_owner()
    async def stock(self, ctx, toolstype: str):
        guild = ctx.guild
        if toolstype == "free":
            try:
                loadgreen = discord.utils.get(ctx.guild.emojis, name=Configs.greenemoji)
                loadorange = discord.utils.get(ctx.guild.emojis, name=Configs.orangeemoji)
                loadred = discord.utils.get(ctx.guild.emojis, name=Configs.redemoji)
                verified = discord.utils.get(ctx.guild.emojis, name="nameoftheemoji")
                embed = discord.Embed(title="Stock", description=f"{str(loadred)} Soon", color=0x000000)
                embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                embed.set_thumbnail(url="https://static.wikia.nocookie.net/mrrobot/images/8/87/ECorp.png")
                embed.add_field(name=f"Ufonet DDOS tool {str(verified)}", value="https://github.com/epsylon/ufonet", inline=False)
                embed.add_field(name=f"Rubeus Active directory tool {str(verified)}", value="https://github.com/GhostPack/Rubeus", inline=False)
                embed.add_field(name=f"SharpUp Windows vuln identifier {str(verified)}", value="https://github.com/GhostPack/SharpUp", inline=False)
                embed.add_field(name=f"LinPEAS Linux privilege escalation {str(verified)}", value="https://github.com/carlospolop/PEASS-ng/tree/master/linPEAS", inline=False)
                embed.add_field(name=f"WinPEAS Windows privilege escalation {str(verified)}", value="https://github.com/carlospolop/PEASS-ng/tree/master/winPEAS", inline=False)
                embed.add_field(name=f"Get-GPPPassword Windows password extraction {str(verified)}", value="https://github.com/PowerShellMafia/PowerSploit/blob/master/Exfiltration/Get-GPPPassword.ps1", inline=False)
                embed.add_field(name=f"Invoke-Obfuscation Script obfuscator {str(verified)}", value="https://github.com/PowerShellMafia/PowerSploit/blob/master/Exfiltration/Get-GPPPassword.ps1", inline=False)
                embed.add_field(name=f"LaZagne Local password extractor {str(verified)}", value="https://github.com/AlessandroZ/LaZagne", inline=False)
                embed.add_field(name=f"Powershell RAT Python based backdoor {str(verified)}", value="https://github.com/Viralmaniar/Powershell-RAT", inline=False)
                embed.add_field(name=f"Discord username sniper {str(verified)}", value="https://github.com/fknMega/discord-username-sniper", inline=False)
                embed.set_image(url="https://i.imgur.com/oSeKEHG.jpeg")
                embed.set_footer(text="fsociety05.dat")
            except Exception as e:
                print(e)

        elif toolstype == "paid":
            try:
                loadgreen = discord.utils.get(ctx.guild.emojis, name=Configs.greenemoji)
                loadorange = discord.utils.get(ctx.guild.emojis, name=Configs.orangeemoji)
                loadred = discord.utils.get(ctx.guild.emojis, name=Configs.redemoji)
                embed = discord.Embed(title="Stock", description=f"{str(loadgreen)} Do a ticket to have\n{str(loadorange)} In developement\n{str(loadred)} Soon", color=0x000000)
                embed.set_thumbnail(url="https://static.wikia.nocookie.net/mrrobot/images/8/87/ECorp.png")
                embed.add_field(name=f"Python Token grabber {str(loadorange)}", value="linkoftheshop", inline=False)
                embed.add_field(name=f"Raid discord bot {str(loadorange)}", value="linkoftheshop", inline=False)
                embed.add_field(name=f"Cobalt Strike {str(loadgreen)}", value="linkoftheshop", inline=False)
                embed.set_image(url="https://i.imgur.com/oSeKEHG.jpeg")
                embed.set_footer(text="fsociety05.dat")
            except Exception as e:
                print(e)
        else:
            embed = discord.Embed(title="Choose the good option", description="\n"+Configs.prefix+"stock free\n"+Configs.prefix+"stock paid", color=0x000000)
            embed.set_image(url="https://i.imgur.com/oSeKEHG.jpeg")
            embed.set_footer(text="fsociety00.dat")

        await ctx.send(embed=embed)
        await ctx.message.delete()

    @tasks.loop(minutes=1)
    async def scammerishere(self):
        try:
            channel = bot.get_channel(Configs.scammer)
            async for message in channel.history():
                for member in guild.members:
                    if member.id in message:
                        channelmemberjoin = bot.get_channel(Configs.logsjoin)
                        await channelmemberjoin.send(f"{member.mention} est un scammer d'après https://discord.gg/ScammerAlert")
        except Exception as e:
            print(e)

    @commands.command(name='e', description="send a embed", help="option : tools & form & payements & social")
    @commands.is_owner()
    async def embed(self, ctx, typeembed):
        if typeembed == "tools":
            embed = discord.Embed(title="Tools", description="Regardez les threads pour voir les tools.", color=0x000000)
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/mrrobot/images/8/87/ECorp.png")
            embed.add_field(name="Free Tools", value="<#"+Configs.freechannel+">", inline=False)
            embed.add_field(name="Paid Tools", value="<#"+Configs.paidchannel+">", inline=False)
            embed.set_image(url="https://i.imgur.com/oSeKEHG.jpeg")
            embed.set_footer(text="fsociety04.dat")

        elif typeembed == "form":
            embed = discord.Embed(title="Candidature pour être modérat(eur/rice) à l'essai", description="ALLSAFE recherche des personnes motivées pour compléter son équipe.\n\nQuelles sont les missions de l'équipe de Allsafe ?\n\n• Accueillir les nouveaux membres sur le server.\n• Modérer le serveur\n• Aidé les membres et échangé avec les membres\n\nQuelles sont les exigences à respecter pour postuler ?\n\n• Avoir 16 ans\n• Ne pas avoir reçu de sanctions graves\n• Etre un membre du serveur depuis plus de 7 jours.\n\nCe poste est bénévole.\n\nSi vous n'avez pas de retours sous 15 jours, considérez que votre candidature est refusée.", color=0x000000)
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/mrrobot/images/8/87/ECorp.png")
            embed.add_field(name="Formulaire de recrutement", value="formulairederecrutement", inline=False)
            embed.set_image(url="https://i.imgur.com/LyUWpsv.jpg")
            embed.set_footer(text="fsociety03.dat")

        elif typeembed == "apayements":
            embed = discord.Embed(title="Paiements acceptés ci-dessous // Payments accepted below", description="BTC and LTC", color=0x000000)
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/mrrobot/images/8/87/ECorp.png")
            embed.set_footer(text="fsociety02.dat")

        elif typeembed == "payements":
            embed = discord.Embed(title="Paiements acceptés ci-dessous", color=0x000000)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/mrrobot/images/8/87/ECorp.png")
            embed.add_field(name="LTC", value="MMsBxXfhz4W9io78bE4yp573nauHDpUvDs", inline=False)
            embed.add_field(name="BTC", value="345n7nGXGRbgf4csKHh1C7RbJwKXFtVcPk", inline=False)
            embed.set_footer(text="fsociety02.dat")

        elif typeembed == "social":
            embed = discord.Embed(title="Réseaux sociaux", color=0x000000)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            embed.set_thumbnail(url="https://static.wikia.nocookie.net/mrrobot/images/8/87/ECorp.png")
            embed.add_field(name="> Discord", value="discordlink", inline=False)
            embed.add_field(name="> Telegram", value="telegramtelegram", inline=False)
            embed.add_field(name="> Github", value="https://github.com/kgbcyber", inline=False)
            embed.set_image(url="https://i.imgur.com/oSeKEHG.jpeg")
            embed.set_footer(text="fsociety01.dat")

        else:
            embed = discord.Embed(title="Choose the good option", description="\n\n"+Configs.prefix+"e apayements\n"+Configs.prefix+"e form\n"+Configs.prefix+"e payements\n"+Configs.prefix+"e tools\n"+Configs.prefix+"e social", color=0x000000)
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            embed.set_image(url="https://i.imgur.com/oSeKEHG.jpeg")
            embed.set_footer(text="fsociety00.dat")

        await ctx.send(embed=embed)
        await ctx.message.delete()


    """test command"""
    @commands.command(name='reset', description="Réinitialise le canal.", help="Réinitialise le canal.")
    @commands.is_owner()
    async def reset(self, ctx, amount=0):
        await ctx.channel.purge(limit=10000)
        await ctx.send(f"[+] Le canal a été réinitialisé...")
    
    @commands.command(name='reply', description="le bot te repond avec ce que tu veut dire", help=Configs.prefix+"reply whatyouwanttosay")
    @commands.is_owner()
    async def reply(self, ctx, sentence):
        await ctx.reply(f"{sentence}")
    
    @commands.command(name='say', description="le bot répéte", help=Configs.prefix+"say whatyouwanttosay")
    @commands.is_owner()
    async def say(self, ctx, sentence):
        await ctx.send(f"{sentence}")

async def setup(bot):
    await bot.add_cog(Owner(bot))
