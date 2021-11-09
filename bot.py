import discord
from discord import embeds
from get_enviroment import COMMAND_PREFIX, OWNER, TOKEN
from discord import Embed
from discord.ext import commands
from discord.ext.commands.core import command
from time import time
import datetime
import sys
import os

import datetime

hammericon = "https://images-ext-2.discordapp.net/external/OKc8xu6AILGNFY3nSTt7wGbg-Mi1iQZonoLTFg85o-E/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/591633652493058068/e6011129c5169b29ed05a6dc873175cb.png?width=670&height=670"

intents = discord.Intents.default()
# intents.members = True
# intents.messages = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents)

bot.remove_command("help")

#
#   HELP SECITON
#
@commands.command(name="help")
async def helpp(ctx):
    # Define each page

    descr = f"""Hammer is a multiuse bot focused on moderation, which its goal is to improve your discord community.    
    For an extense command description, use ``{COMMAND_PREFIX}help [command name]``
    **Hammer's commands:**
    {COMMAND_PREFIX}help
    {COMMAND_PREFIX}whois [user]
    {COMMAND_PREFIX}ban [user] <reason>
    {COMMAND_PREFIX}kick [user] <reason>
    {COMMAND_PREFIX}warn [user] <reason>
    """
    embed = Embed(title="Hammer Bot Help", description=descr)

    embed.set_footer(
        text=f"Hammer | Command executed by {ctx.message.author}",
        icon_url="https://images-ext-2.discordapp.net/external/OKc8xu6AILGNFY3nSTt7wGbg-Mi1iQZonoLTFg85o-E/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/591633652493058068/e6011129c5169b29ed05a6dc873175cb.png?width=670&height=670",
    )

    await ctx.send(embed=embed)


def sendNotifOwner(text, id):
    discord.User(id).send(text)


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="you")
    )
    print("HAMMER BOT Ready!", datetime.datetime.now())
    # sendNotifOwner("Bot UP:", OWNER)
    print("I'm on:")
    print(len(bot.guilds), "servers")
    print(sum(1 for x in bot.get_all_channels()), "channels")
    print(sum(1 for x in bot.get_all_members()), "members")


debug = False


@commands.command()
async def hello(ctx):
    await ctx.send("Hammer is back!")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(
            f"**[ERROR 404]** Please pass in all requirements :hammer_pick:. ```{error}```\nDo  {COMMAND_PREFIX}help command for more help"
        )
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            "[**ERROR 403]** You don't have the correct permission to do that :hammer:"
        )


@commands.command()
async def whois(ctx, member: discord.Member):
    try:
        username, discriminator = str(member).split("#")
        isbot = ":white_check_mark:" if member.bot else ":negative_squared_cross_mark:"
        descr = f"""
            **Nick:** {member.nick}
            **Username:** {username}
            **Discriminator:** {discriminator}
            **Created account at:** {member.created_at}
            **Joined server at:** {member.joined_at}
            **Is bot:** {isbot}
            **User ID:** {member.id}
            **Avatar URL:** [Click Here]({member.avatar_url})
            **Top role:** {member.top_role}
            """
        embed = Embed(title=f"Who is {member} ?", description=descr)

        embed.set_thumbnail(url=member.avatar_url)

        embed.set_footer(
            text=f"Hammer | Command executed by {ctx.message.author}",
            icon_url=hammericon,
        )
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(e)


@commands.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member == ctx.message.author:
        await ctx.channel.send("You cannot ban yourself")
        return
    if reason == None:
        reason = "bad behaviour 💥"
    message = f"You have been banned from {ctx.guild.name} for {reason}"

    if not debug:
        await member.ban(reason=reason)
    descr = f"The user {member} has been banned for {reason}"
    embed = Embed(title=f"{member} has been banned! :hammer_pick:", description=descr)
    embed.set_image(url="https://i.imgflip.com/19zat3.jpg")
    embed.set_footer(
        text=f"Hammer | Command executed by {ctx.message.author}",
        icon_url=hammericon,
    )

    embed.set_thumbnail(url=member.avatar_url)
    await ctx.send(embed=embed)
    await member.send(message)


@commands.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member == ctx.message.author:
        await ctx.channel.send("You cannot kick yourself")
        return
    if reason == None:
        reason = "bad behaviour 💥"
    message = f"You have been kicked from {ctx.guild.name} for {reason}"
    if not debug:
        await member.kick(reason=reason)
    descr = f"The user {member} has been kicked for {reason}"
    embed = Embed(title=f"{member} has been kicked! :hammer_pick:", description=descr)
    embed.set_footer(
        text=f"Hammer | Command executed by {ctx.message.author}",
        icon_url=hammericon,
    )
    embed.set_thumbnail(url=member.avatar_url)
    # # embed.image = member.image
    await ctx.send(embed=embed)
    await member.send(message)


@commands.command()
@commands.has_permissions(kick_members=True)
async def warn(ctx, member: discord.Member, *, reason=None):
    if member == ctx.message.author:
        await ctx.channel.send("You cannot warn yourself :(")
        return
    if reason == None:
        reason = "bad behaviour 💥"
    message = f"You have been warned for {reason}"

    descr = f"The user {member} has been warned for {reason}"
    embed = Embed(title=f"{member} has been warned! :hammer_pick:", description=descr)
    embed.set_footer(
        text=f"Hammer | Command executed by {ctx.message.author}",
        icon_url=hammericon,
    )
    embed.set_thumbnail(url=member.avatar_url)

    await ctx.send(embed=embed)
    await member.send(message)


@commands.command()
async def evaluate(ctx, *, code):
    if str(ctx.message.author.id) == str(OWNER):
        print("RECIEVED:", code)
        # t = ctx.message.author.id,"used the command eval at", datetime.now()
        # print(t)
        args = {
            "discord": discord,
            "sys": sys,
            "os": os,
            "imp": __import__,
            "ctx": ctx,
            "bot": bot,
        }
        try:
            exec(f"async def func(): return {code}", args)
            a = time()
            response = await eval("func()", args)
            await ctx.send(
                f"```py\n{response}```    |    ```{type(response).__name__}``` `| {(time() - a) / 1000} ms`"
            )
        except Exception as e:
            await ctx.send(f"Error occurred:```\n{type(e).__name__}: {str(e)}```")
    else:
        return


bot.add_command(evaluate)
bot.add_command(hello)
bot.add_command(kick)
bot.add_command(ban)
bot.add_command(warn)
bot.add_command(helpp)
bot.add_command(whois)
bot.run(TOKEN)
