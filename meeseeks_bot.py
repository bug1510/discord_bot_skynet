#!/usr/bin/env python3

import os
import time
from datetime import datetime
import json
import requests
import logging
from discord.ext import commands
from discord.utils import get

today = datetime.now()
today = today.strftime("%Y%m%d")
source = os.path.dirname(os.path.abspath(__file__))

client = commands.Bot(command_prefix='!')
logging.basicConfig(
    filename= source + '/../logs/' + str(today) + '_discord_bot.log',
    format='%(asctime)s %(message)s',
    level=logging.INFO
    ) # possible info/error/warning/critical/debug

@client.event

async def on_ready():
    logging.info('bot started')
    print('Im ready')

@client.command()
@commands.has_role('El-Special')

async def game_channel_create(self, gamename):

    """Dieser Befehl ist administrativ und legt eine ganze Rolle ihre Kategorie 
    und eigene Channel an"""

    guild = self.message.guild
    member = self.message.author
    logging.info(str(member) + ' tried to create ' + str(gamename))
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

    """Dieser Befehl Listet dir die für dich bereits verfügbaren Rollen auf"""

    lowest = get(context.guild.roles, name='@everyone')
    highestrole = get(context.guild.roles, name='Groovy')
    member = context.message.author
    logging.info(str(member) + ' called lsrole')

    for role in context.guild.roles:
        
        if role.position < highestrole.position and role.position > lowest.position:
            await context.send(role)
            time.sleep(0.75)

@client.command()

# Der !addrole Befehl fügt einem Nutzer eine bestimmte Rolle an.
# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def addrole(context, rolename):

    """addrole fügt dir einfach und schnell eine Gamingrolle oder mehrere Gamingrollen (mit Komma getrennt) hinzu, 
    damit du die richtigen Kategorien siehst"""

    # prüfe ob ein Komma in rolename vorhanden ist , wenn ja werden mehrere Rollen hinzugefügt

    if rolename.find(",") > 0:
        # mehrere Rollen gefunden
        multi = True
        para = rolename.split(",")
    else:
        # nur eine Rolle
        multi = False
        para = rolename

    # definiere variablen
    member = context.message.author
    logging.info(str(member) + ' called addrole')
    highestrole = get(context.guild.roles, name='Groovy')

    await context.send(':sparkles:' + '*poof*' + ':sparkles:')
    await context.send('Was willst du?')
    time.sleep(1)

    # prüfen ob mehrere Rollen hinzugefügt werden müssen
    if multi:
        # durchlaufe das array für jeden eintrag
        for e in para:
            role = get(member.guild.roles, name=e)
            # prüfe ob die gewünschte Rolle in der hirarchie höher liegt als die erlaubte
            if role.position < highestrole.position:
                await member.add_roles(role)
                logging.info(str(member) + ' hat sich die Rolle ' + str(role) + ' zugewiesen')
                time.sleep(0.5)
            else:
                await context.send('kann die Rolle ' + str(role) + ' nicht hinzufügen')
                logging.info(str(member) + ' hat versucht sich eine Rolle hinzuzufügen die höher als die erlaubt ist')    
    else:
        role = get(member.guild.roles, name=para)
        # prüfe ob die gewünschte Rolle in der hirarchie höher liegt als die erlaubte
        if role.position < highestrole.position:
            await member.add_roles(role)
            logging.info(str(member) + ' hat sich die Rolle ' + str(role) + ' zugewiesen')
            time.sleep(0.5)
        else:
            await context.send('kann die Rolle ' + str(role) + ' nicht hinzufügen')
            logging.info(str(member) + ' hat versucht sich eine Rolle hinzuzufügen die höher als die erlaubt ist')    

    await context.send(':sparkles:' + '*poof*' + ':sparkles:')           

@client.command()

# Der !addall Befehl fügt einem Nutzer alle Verfügbaren Rollen an.
# Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
# @commands.has_role("Der Architekt")

async def addall(self):

    """Du glaubst jedes Spiel zu haben? 
    Dann gib dir doch fix einfach alle Gamingrollen um überall mit zu mischen"""

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

    """rmrole nimmt dir eine Rolle und das Recht eine Kategorie zu sehen, 
    falls du ein Spiel nicht mehr magst ;)"""

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

    """Ist das Gegenstück zu add3roles und Funktioniert auch so, 
    nur das du am Ende weniger Rollen hast"""

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

    """Keine Lust mehr auf Gaming? Dann nimm dir doch einfach alle Rollen"""

    author = self.message.author
    lowest = get(self.guild.roles, name='@everyone')
    highestrole = get(self.guild.roles, name='Groovy')
    
    await self.send(':sparkles:' + '*poof*' + ':sparkles:')
    await self.send('Was willst du? Alle Rollen abgeben? Oh ja, das kann ich für dich tun!')
    for role in self.guild.roles:
        
        if role.position < highestrole.position and role.position > lowest.position:
            await author.remove_roles(role)

    await self.send(':sparkles:' + '*poof*' + ':sparkles:')

@client.command()

# tell a joke
# written by Pope

async def joke(context):

    """Langeweile? Mr Meeseeks erzählt dir gerne ein paar Witze"""

    member = context.message.author
    logging.info(str(member) + ' called joke')
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

maintenance = open(source + '/../token.json',)
secret = json.load(maintenance)

client.run(secret['token'])

maintenance.close()