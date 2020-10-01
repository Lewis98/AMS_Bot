import discord
from discord.ext import commands
import os

client = commands.Bot(command_prefix=".")
token = os.getenv("bot_token")

@client.event
async def on_ready():
    await client.change_presence(
        status = discord.Status.idle, 
        activity = discord.Game("Listening to .help")
    )
    print("I am online")


@client.command()
async def ping(ctx):
    await ctx.send(f"Pong!")


client.run(token)