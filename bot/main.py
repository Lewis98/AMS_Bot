import discord
from discord.ext import commands
import os
import re # Regex

client = commands.Bot(command_prefix=".")
token = os.getenv("bot_token")

@client.event
async def on_ready():
    await client.change_presence(
        status = discord.Status.online,
    )
    print("I am online")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong!")

@client.command()
async def checkme(ctx, *args):

    if len(args) != 1:
        await ctx.send("Correct useage - checkme {Student ID}")
        return
    

    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="Paid Member")

    if role in user.roles:
        await ctx.send(f"{user.display_name} is already a paid member!")
        return

    arg = args[0]

    if not re.search('^[0-9]{7,8}$', arg):
        
        await ctx.send(f"{str(arg)} is not a valid Student ID")
        return
    
    else:

        await ctx.send(f"Checking '{arg}' for '{str(user.display_name)}'!")
        await ctx.send(arg)

        # validateID(arg)

        valid = True

        if valid:
            await ctx.send(f"{user.display_name} has paid!")
            await discord.Member.add_roles(user, role)


client.run(token)