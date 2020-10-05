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
        
        # validate
        f = open("IDs.txt", "r")
        IDlist = f.readlines()
        f.close()

        valid = False
        for uid in IDlist:
            if re.search(f"^{hash_id}$", uid):
                valid = True
                
        if valid:
            # Open members.txt and append new hashes
            f = open("members.txt", "a")
            f.write(hash_user + " - " + hash_id + "\n")
            f.close()

            # Remove ID from list of available
            f = open("IDs.txt", "r")
            lines = f.readlines()
            f.close()

            f = open("IDs.txt", "w")
            for l in lines:
                if not re.search(f"^{hash_id}$", l):
                    f.write(l)
            f.close()

            # Add role to user and remove pending
            await discord.Member.add_roles(user, role)
            await discord.Member.remove_roles(user, role_pend)

            await ctx.send(f"{user.display_name} has paid!")
        else:
            await ctx.send(f"{arg} is invalid.")


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
    f.close()


@client.command()
async def uncheck(ctx, *args):

    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="Committee")
    if not (role in user.roles):
        await ctx.send(f"Only Committee members can add ID's")
        return

    user = bot.get_user(args[0])
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
    f.close()

@client.command()
async def addID(ctx, *args):
    
    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="Committee")
    if not (role in user.roles):
        await ctx.send(f"Only Committee members can add ID's")
        return

    f = open("members.txt", "r")
    membersList = f.readlines()
    f.close()

    f = open("IDs.txt", "r")
    IDlist = f.readlines()
    f.close()
    
    for arg in args:
        hash_id = hashlib.sha256(str(arg).encode())
        hash_id = str(hash_id.hexdigest())

        idClaimed = 0
        idExists = 0
        idAdded = 0

        inUse = False
        for m in membersList:
            if re.search(f"- {hash_id}$", m):
                inUse = True
                idClaimed += 1
                break

        exists = False
        for uid in IDlist:
            if re.search(f"^{hash_id}$", uid):
                exists = True
                idExists += 1
                break
        
        if (not inUse) and (not exists):
            f = open("IDs.txt", "a")
            f.write(hash_id + "\n")
            f.close()
            idAdded += 1
        
    await ctx.send(f"{str(idAdded)} ID's added ({idClaimed} already claimed, {idExists} already exist)")


@client.command()
async def dumpLogs(ctx):

    user = ctx.message.author
    role = discord.utils.get(user.guild.roles, name="Committee")
    if not (role in user.roles):
        await ctx.send(f"Only Committee members can dump log files")
        return
    
    f = open("members.txt", "r")
    m_lines = f.readlines()
    f.close()

    f = open("IDs.txt", "r")
    i_lines = f.readlines()
    f.close()

    print("Members List:")
    for l in m_lines:
        print(l)
    print("")
    print("")
    print("ID List:")
    for l in i_lines:
        print(l)
    
    await ctx.send(f"Logs successfully dumped to console")



client.run(token)