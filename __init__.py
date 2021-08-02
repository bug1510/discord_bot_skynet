#!/usr/bin/env python3

import time
import discord
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

async def addrole(context, rolename):
    member = context.message.author
    role = get(member.guild.roles, name=rolename)
    botrole = get(context.guild.roles, name='Mr Meeseeks')
    if role.position < botrole.position:
        await context.send(':sparkles:' + '*poof*' + ':sparkles:')
        await context.send('Was willst du?')
        time.sleep(1)
        await context.send('Die Rolle ' + str(rolename) + '? oh ja, das kann ich für dich tun!')
        time.sleep(1)
        await member.add_roles(role)
        await context.send(':sparkles:' + '*poof*' + ':sparkles:')
    else:
        await context.send('Versuch mal lsrole um dir alle für dich, verfügbaren Rollen anzeigen zulassen.')

@client.command()

# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def rmrole(context, rolename):
    member = context.message.author
    role = get(member.guild.roles, name=rolename)
    botrole = get(context.guild.roles, name='Mr Meeseeks')
    if role.position < botrole.position:
        await context.send(':sparkles:' + '*poof*' + ':sparkles:')
        await context.send('Was willst du?')
        time.sleep(1)
        await context.send('Du willst die Rolle ' + str(rolename) + ' nicht mehr? oh ja, das kann ich für dich tun!')
        time.sleep(1)
        await member.remove_roles(role)
        await context.send(':sparkles:' + '*poof*' + ':sparkles:')

@client.command()

# Listet die bereits verfügbaren Rollen auf.

async def lsrole(self):
    botrole = get(self.guild.roles, name='Mr Meeseeks')
    for role in self.guild.roles:
        if role.position < botrole.position:
            await self.send(role)
            time.sleep(0.5)


client.run('ODY0MDYyODA3OTk2MzY2ODYw.YOv_Mg.Ta49h5QniPBqGFhL5c3XFB12OEs')