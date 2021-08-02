#!/usr/bin/env python3

import time
import json
import requests
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix='!')

@client.event

async def on_ready():
    print('Im ready')

@client.command()
@commands.has_role('El-Special')

async def game_channel_create(self, gamename):
    guild = self.message.guild

    gamerole = await guild.create_role(name=gamename)
    junior_admin = get(self.guild.roles, name='Junior Admin')
    admin = get(self.guild.roles, name='Admin')
    senior_admin = get(self.guild.roles, name='Senior Admin')
    
    place = await guild.create_category_channel(name='<##>' + str(gamename))

    await place.set_permissions(
        guild.default_role,

        view_channel=False,
        manage_channels=False,
        manage_permissions=False,
        manage_webhooks=False,
        create_instant_invite=False,
        send_messages=False,
        embed_links=False,
        attach_files=False,
        add_reactions=False,
        use_external_emojis=False,
        mention_everyone=False,
        manage_messages=False,
        read_message_history=False,
        send_tts_messages=False,
        use_slash_commands=False,
        connect=False,
        speak=False,
        stream=False,
        use_voice_activation=False,
        priority_speaker=False,
        mute_members=False,
        deafen_members=False,
        move_members=False,
        request_to_speak=False
        )
    
    await place.set_permissions(
        gamerole,

        view_channel=True,
        manage_channels=False,
        manage_permissions=False,
        manage_webhooks=False,
        create_instant_invite=False,
        send_messages=True,
        embed_links=False,
        attach_files=False,
        add_reactions=True,
        use_external_emojis=True,
        mention_everyone=False,
        manage_messages=False,
        read_message_history=True,
        send_tts_messages=True,
        use_slash_commands=False,
        connect=True,
        speak=True,
        stream=True,
        use_voice_activation=True,
        priority_speaker=False,
        mute_members=False,
        deafen_members=False,
        move_members=False,
        request_to_speak=True
        )
    
    await place.set_permissions(
        junior_admin,

        view_channel=True,
        manage_channels=False,
        manage_permissions=False,
        manage_webhooks=False,
        create_instant_invite=False,
        send_messages=True,
        embed_links=False,
        attach_files=False,
        add_reactions=True,
        use_external_emojis=True,
        mention_everyone=True,
        manage_messages=True,
        read_message_history=True,
        send_tts_messages=True,
        use_slash_commands=False,
        connect=True,
        speak=True,
        stream=True,
        use_voice_activation=True,
        priority_speaker=False,
        mute_members=True,
        deafen_members=True,
        move_members=True,
        request_to_speak=True
        )
    
    await place.set_permissions(
        admin,

        view_channel=True,
        manage_channels=False,
        manage_permissions=False,
        manage_webhooks=False,
        create_instant_invite=False,
        send_messages=True,
        embed_links=True,
        attach_files=False,
        add_reactions=True,
        use_external_emojis=True,
        mention_everyone=True,
        manage_messages=True,
        read_message_history=True,
        send_tts_messages=True,
        use_slash_commands=True,
        connect=True,
        speak=True,
        stream=True,
        use_voice_activation=True,
        priority_speaker=True,
        mute_members=True,
        deafen_members=True,
        move_members=True,
        request_to_speak=True
        )
    
    await place.set_permissions(
        senior_admin,

        view_channel=True,
        manage_channels=True,
        manage_permissions=False,
        manage_webhooks=False,
        create_instant_invite=False,
        send_messages=True,
        embed_links=True,
        attach_files=True,
        add_reactions=True,
        use_external_emojis=True,
        mention_everyone=True,
        manage_messages=True,
        read_message_history=True,
        send_tts_messages=True,
        use_slash_commands=True,
        connect=True,
        speak=True,
        stream=True,
        use_voice_activation=True,
        priority_speaker=True,
        mute_members=True,
        deafen_members=True,
        move_members=True,
        request_to_speak=True
        )
    
    await guild.create_text_channel(name=str(gamename) + '-talk', category=place)
    await guild.create_voice_channel(name='Fraktion-I', category=place, user_limit=8)
    await guild.create_voice_channel(name='Fraktion-II', category=place, user_limit=8)
    await guild.create_voice_channel(name='Fraktion-III', category=place, user_limit=8)
    await guild.create_voice_channel(name='Fraktion-IV', category=place, user_limit=8)
    await guild.create_voice_channel(name='Group-Talk', category=place)

# Die folgenden Zeilen sind das Rollen Feature des Kirkland Meeseeks.

@client.command()

# Der !lsrole Befehl Listet die bereits verfügbaren Rollen auf.

async def lsrole(context):
    lowest = get(context.guild.roles, name='@everyone')
    highestrole = get(context.guild.roles, name='Groovy')
    
    for role in context.guild.roles:
        
        if role.position < highestrole.position and role.position > lowest.position:
            await context.send(role)
            time.sleep(0.75)

@client.command()

# tell a joke
# written by Pope

async def joke(context):
    jokejson = requests.get("https://v2.jokeapi.dev/joke/Any?lang=de")
    joke_payload = jokejson.json()
    if jokejson.status_code == 200:
        if joke_payload['type'] == 'twopart':
            question = joke_payload['setup']
            answer = joke_payload['delivery']
            await context.send(question)
            time.sleep(1)
            await context.send(answer)
        if joke_payload['type'] == 'single':
            joke =  joke_payload['joke']
            await context.send(joke)

@client.command()

# Der !addrole Befehl fügt einem Nutzer eine bestimmte Rolle an.
# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def addrole(context, rolename):
    member = context.message.author
    role = get(member.guild.roles, name=rolename)
    highestrole = get(context.guild.roles, name='Groovy')
    
    if role.position < highestrole.position:
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

# Der !add3roles Befehl fügt einem Nutzer drei bestimmte Rollen an.
# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def add3roles(context, rolename1, rolename2, rolename3):
    member = context.message.author
    role1 = get(member.guild.roles, name=rolename1)
    role2 = get(member.guild.roles, name=rolename2)
    role3 = get(member.guild.roles, name=rolename3)
    highestrole = get(context.guild.roles, name='Groovy')

    if(role1.position < highestrole.position and role2.position < highestrole.position and role3.position < highestrole.position):
        await context.send(':sparkles:' + '*poof*' + ':sparkles:')
        await context.send('Was willst du?')
        time.sleep(1)
        await context.send('Die Rollen ' + ', ' + str(rolename1) + ', ' + str(rolename2) + ' und ' + str(rolename3) + '? Oh ja, das kann ich für dich tun!')
        time.sleep(1)
        await member.add_roles(role1)
        await member.add_roles(role2)
        await member.add_roles(role3)
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
    highestrole = get(self.guild.roles, name='Groovy')
    
    await self.send(':sparkles:' + '*poof*' + ':sparkles:')
    await self.send('Was willst du? Alle Rollen? Oh ja, das kann ich für dich tun!')
    for role in self.guild.roles:
        
        if role.position < highestrole.position and role.position > lowest.position:
            await author.add_roles(role)

    await self.send(':sparkles:' + '*poof*' + ':sparkles:')

@client.command()

# Der !rmrole Befehl entfernt eine bestimmte Rolle von einem Nutzer.
# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def rmrole(context, rolename):
    member = context.message.author
    role = get(member.guild.roles, name=rolename)
    highestrole = get(context.guild.roles, name='Groovy')
    
    if role.position < highestrole.position:
        await context.send(':sparkles:' + '*poof*' + ':sparkles:')
        await context.send('Was willst du?')
        time.sleep(1)
        await context.send('Du willst die Rolle ' + str(rolename) + ' nicht mehr? oh ja, das kann ich für dich tun!')
        time.sleep(1)
        await member.remove_roles(role)
        await context.send(':sparkles:' + '*poof*' + ':sparkles:')

@client.command()

# Der !rm3role Befehl entfernt drei bestimmte Rolle von einem Nutzer.
# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def rm3roles(context, rolename1, rolename2, rolename3):
    member = context.message.author
    role1 = get(member.guild.roles, name=rolename1)
    role2 = get(member.guild.roles, name=rolename2)
    role3 = get(member.guild.roles, name=rolename3)
    highestrole = get(context.guild.roles, name='Groovy')
    
    if(role1.position < highestrole.position and role2.position < highestrole.position and role3.position < highestrole.position):
        await context.send(':sparkles:' + '*poof*' + ':sparkles:')
        await context.send('Was willst du?')
        time.sleep(1)
        await context.send('Du willst die Rollen ' + str(rolename1) + ', ' + str(rolename2) + ', ' + str(rolename3) + ' nicht mehr? oh ja, das kann ich für dich tun!')
        time.sleep(1)
        await member.remove_roles(role1)
        await member.remove_roles(role2)
        await member.remove_roles(role3)
        await context.send(':sparkles:' + '*poof*' + ':sparkles:')

    else:
        await context.send('Irgendwas ist schief gegangen, überprüfe deine Angaben nochmal.')

@client.command()

# Der !rmall Befehl enfernt alle Rollen von einem Nutzer.
# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def rmall(self):
    author = self.message.author
    lowest = get(self.guild.roles, name='@everyone')
    highestrole = get(self.guild.roles, name='Groovy')
    
    await self.send(':sparkles:' + '*poof*' + ':sparkles:')
    await self.send('Was willst du? Alle Rollen abgeben? Oh ja, das kann ich für dich tun!')
    for role in self.guild.roles:
        
        if role.position < highestrole.position and role.position > lowest.position:
            await author.remove_roles(role)

    await self.send(':sparkles:' + '*poof*' + ':sparkles:')

maintenance = open('token.json',)
secret = json.load(maintenance)

client.run(secret['token'])

maintenance.close()