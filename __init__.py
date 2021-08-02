#!/usr/bin/env python3

import time
import discord
from discord import member
from discord import message
from discord import guild
from discord import role
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Bot is ready')

# Rollen Feature, der Kirkland Meeseeks kann mit den Folgenden Funktionen Rollen hinzufügen und entfernen.

@client.command()

# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def addrole(ctx, rolename):
    member = ctx.message.author
    role = get(member.guild.roles, name=rolename)
    await ctx.send(':sparkles:' + '*poof*' + ':sparkles:')
    await ctx.send('Was willst du?')
    time.sleep(1)
    await ctx.send('Die Rolle ' + str(rolename) + '? oh ja, das kann ich für dich tun!')
    time.sleep(1)
    await member.add_roles(role)
    await ctx.send(':sparkles:' + '*poof*' + ':sparkles:')

@client.command()

# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def rmrole(ctx, rolename):
    member = ctx.message.author
    role = get(member.guild.roles, name=rolename)
    await ctx.send(':sparkles:' + '*poof*' + ':sparkles:')
    await ctx.send('Was willst du?')
    time.sleep(1)
    await ctx.send('Du willst die Rolle ' + str(rolename) + ' nicht mehr? oh ja, das kann ich für dich tun!')
    time.sleep(1)
    await member.remove_roles(role)
    await ctx.send(':sparkles:' + '*poof*' + ':sparkles:')

client.run('ODY0MDYyODA3OTk2MzY2ODYw.YOv_Mg.Ta49h5QniPBqGFhL5c3XFB12OEs')

