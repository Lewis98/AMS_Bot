import discord
from discord.ext import commands
import os
import re # Regex
import hashlib

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
    role_pend = discord.utils.get(user.guild.roles, name="Pending")

    if role in user.roles:
        await ctx.send(f"{user.display_name} is already a paid member!")
        return

    arg = args[0]

    if not re.search('^[0-9]{7,8}$', arg):
        
        await ctx.send(f"{str(arg)} is not a valid Student ID")
        return
    
    else:

        await ctx.send(f"Checking '{arg}' for '{str(user.display_name)}'!")

        # validateID(arg)

        valid = True

        if valid:            
            # Hash user and student ID
            hash_user = hashlib.sha256(str(user).encode())
            hash_id = hashlib.sha256(str(arg).encode())
            hash_user = str(hash_user.hexdigest())
            hash_id = str(hash_id.hexdigest())

            # Check members.txt for existing data
            f = open("members.txt", "r")
            lines = f.readlines()
            f.close()
            for l in lines:
                if re.search(f"^{hash_user} - *", l):
                    await ctx.send(f"{user.display_name} is already a paid member.")
                    return
                
                if re.search(f"- {hash_id}$", l):
                    await ctx.send(f"{arg} has already been used!")
                    return
                


            # Open members.txt and append new hashes
            f = open("members.txt", "a")
            f.write(hash_user + " - " + hash_id + "\n")
            f.close()

            await discord.Member.add_roles(user, role)
            await discord.Member.remove_roles(user, role_pend)

            await ctx.send(f"{user.display_name} has paid!")


@client.command()
async def uncheckme(ctx, *args):

    user = ctx.message.author
    hash_user = hashlib.sha256(str(user).encode())
    hash_user = str(hash_user.hexdigest())

    role = discord.utils.get(user.guild.roles, name="Paid Member")
    role_pend = discord.utils.get(user.guild.roles, name="Pending")

    f = open("members.txt", "r")
    lines = f.readlines()
    f.close()

    f = open("members.txt", "w")
    m_found = False
    for l in lines:
        if re.search(f"^{hash_user} - *", l):
            await ctx.send(f"{user.display_name} removed from list of paid members")
            await discord.Member.add_roles(user, role_pend)
            await discord.Member.remove_roles(user, role)
        else:
            f.write(l)

                






client.run(token)