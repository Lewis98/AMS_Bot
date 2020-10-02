import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix="♪")
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

@client.command(pass_context = True)
async def checkMe(ctx):
    user = ctx.message.author
    await ctx.send(f"Checking " + str(user) + "!")

    # Check Student ID
    
    valid = True
    if valid:
        role = discord.utils.get(user.server.roles, name="Paid Member")
        await client.add_roles(user, role)


client.run(token)