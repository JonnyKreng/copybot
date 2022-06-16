from email.message import Message
from io import TextIOWrapper
from typing import Sequence
import json

import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord_slash.model import SlashCommandOptionType

#https://discord.com/api/oauth2/authorize?client_id=949998207147065395&permissions=431644735552&scope=bot%20applications.commands

db_name = './data/settings.json'
token_file = './data/bottoken'

db = {}

client = commands.Bot(command_prefix="/", self_bot=True, intents=discord.Intents.default())
slash = SlashCommand(client, sync_commands=True)

def load_db():
    global db
    try:
        file = open(db_name,"r")
        db = json.load(file)
        file.close()
        print(json.dumps(db))
    except:
        pass

def save_db():
    global db
    try:
        file = open(db_name,"w")
        json.dump(db,file)
        file.close()
    except:
        pass

@client.event
async def on_ready():
    global db
    print("Hallo my name is " + str(client.user))
    
@client.event
async def on_message(message: discord.Message):
    global db

    if message.author == client.user:
        return

    if str(message.guild.id) in db:
        if str(message.channel.id) in db[str(message.guild.id)]:
            for x in db[str(message.guild.id)][str(message.channel.id)]:
                embed = discord.Embed(
                    title=f"Message in {message.channel.name}",
                    description=f'Author: {message.author.display_name}\nTimestamp: {message.created_at}\nMessage: {message.content}'
                )
                await client.get_channel(int(x)).send(embed=embed)
            await message.delete()

@slash.slash(name="CRTGMESSAGE", 
            description="Send Message to channel",
            options=[{'name': 'message', 'description': 'Message to send to channel', 'type': 3, 'required': True, 'choices': []}]
            )
async def register_channel(ctx: SlashContext, message: str):
    await ctx.send(f"Message from {ctx.author.display_name}: {message}")

@slash.slash(name="CRTGX",
            description="Marks channel as channel where Messsages should be removed"
            )
async def register_channel(ctx: SlashContext):
    if ctx.author == client.user:
        return
    embed = discord.Embed(title="CTRG+X Channel",description=f'Marked as CTRG+X Channel, "/CRTGV {ctx.channel.id}" to mark CTRG+V channel')
    await ctx.send(embed=embed)

@slash.slash(name="CRTGV", 
            description="Marks channel as pasta channel, messages will be pasted here", 
            options=[{'name': 'ctrgxid', 'description': 'CRTGX Channel id', 'type': 3, 'required': True, 'choices': []}]
            )
async def register_channel(ctx: SlashContext, ctrgxid: str):
    global db
    if ctx.author == client.user:
        return
    try:   
        if str(ctx.guild.id) not in db:
            db[str(ctx.guild.id)] = {}
        if str(ctrgxid) not in db[str(ctx.guild.id)]:
            db[str(ctx.guild.id)][str(ctrgxid)] = [str(ctx.channel.id)]
        else:
            if str(ctx.channel.id) in db[str(ctx.guild.id)][str(ctrgxid)]:
                embed = discord.Embed(title="Already marked to that channel")
                await ctx.send(embed=embed)
                return
            db[str(ctx.guild.id)][str(ctrgxid)].append(str(ctx.channel.id))

        embed = discord.Embed(title="CTRG+V Channel",description=f"Marked {ctx.channel.name} as CTRG+V channel, messages will be pasted here from {client.get_channel(int(ctrgxid)).name}")
        await ctx.send(embed=embed)
        save_db()
    except:
        print("Error on CRTGV")
        embed = discord.Embed(title="Error",description="Error marking channel")
        await ctx.send(embed=embed)

if __name__ == '__main__':    
    load_db()

    tokenFile = open(token_file)   
    token = tokenFile.read()
    tokenFile.close()
    client.run(token)