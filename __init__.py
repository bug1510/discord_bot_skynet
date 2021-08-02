#!/usr/bin/env python3

import time
import discord
import json
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Bot is ready')

# Die folgenden Zeilen sind das Rollen Feature des Kirkland Meeseeks.

@client.command()

# Der !lsrole Befehl Listet die bereits verfügbaren Rollen auf.

async def lsrole(self):
    lowest = get(self.guild.roles, name='@everyone')
    botrole = get(self.guild.roles, name='Mr Meeseeks')
    
    for role in self.guild.roles:
        
        if role.position < botrole.position and role.position > lowest.position:
            await self.send(role)
            time.sleep(0.66)

@client.command()

# Der !addrole Befehl fügt einem Nutzer eine bestimmte Rolle an.
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

# Der !addall Befehl fügt einem Nutzer alle Verfügbaren Rollen an.
# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def addall(self):
    author = self.message.author
    lowest = get(self.guild.roles, name='@everyone')
    botrole = get(self.guild.roles, name='Mr Meeseeks')
    
    await self.send(':sparkles:' + '*poof*' + ':sparkles:')
    await self.send('Was willst du? Alle Rollen? Oh ja, das kann ich für dich tun!')
    for role in self.guild.roles:
        
        if role.position < botrole.position and role.position > lowest.position:
            await author.add_roles(role)

    await self.send(':sparkles:' + '*poof*' + ':sparkles:')

@client.command()

# Der !rmrole Befehl entfernt eine bestimmte Rolle von einem Nutzer.
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

# Der !rmall Befehl enfernt alle Rollen von einem Nutzer.
# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def rmall(self):
    author = self.message.author
    lowest = get(self.guild.roles, name='@everyone')
    botrole = get(self.guild.roles, name='Mr Meeseeks')
    
    await self.send(':sparkles:' + '*poof*' + ':sparkles:')
    await self.send('Was willst du? Alle Rollen abgeben? Oh ja, das kann ich für dich tun!')
    for role in self.guild.roles:
        
        if role.position < botrole.position and role.position > lowest.position:
            await author.remove_roles(role)

    await self.send(':sparkles:' + '*poof*' + ':sparkles:')

client.run('ODY0MDYyODA3OTk2MzY2ODYw.YOv_Mg.h2_0lQr26VeAdyvis4D0EcIX3UE')

