import time
from typing import List
import discord
from discord import member
from discord.ext import commands
from discord.utils import get
import logging

logger = logging.getLogger('SkyNet-Core')

class MemberCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Die folgenden Zeilen sind das Rollen Feature des Kirkland Meeseeks.

    @commands.command()

    # Der !lsrole Befehl Listet die bereits verfügbaren Rollen auf.

    async def lsrole(self, context):

        """Dieser Befehl Listet dir die für dich bereits verfügbaren Rollen auf"""

        lowest = get(context.guild.roles, name='@everyone')
        highestrole = get(context.guild.roles, name='Nutzer')
        member = context.message.author
        logger.info(str(member) + ' called lsrole')
        ListRolesField = ''

        for role in context.guild.roles:
            if role.position < highestrole.position and role.position > lowest.position:
                ListRolesField += str(role) + '\n'
            else:
                pass

        embed = discord.Embed(
            title='List of Gamingroles',
            description=ListRolesField,
            color=discord.Color.blue()
        )
        await context.send(embed=embed)
        await context.message.delete()

    @commands.command()

    # Der !addrole Befehl fügt einem Nutzer eine bestimmte Rolle an.
    # Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
    # @commands.has_role("Der Architekt")

    async def addrole(self, context, rolename):

        """fügt dir eine, oder mehrere Gamingrollen hinzu (mit Komma getrennt), 
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
        logger.info(str(member) + ' called addrole')
        highestrole = get(context.guild.roles, name='Nutzer')

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
                    await context.send('Die Rolle ' + str(role) + ' ? oh ja, das kann ich für dich tun!')
                    logger.info(str(member) + ' hat sich die Rolle ' + str(role) + ' zugewiesen')
                    time.sleep(0.5)
                else:
                    await context.send('kann die Rolle ' + str(role) + ' nicht hinzufügen')
                    logger.info(str(member) + ' hat versucht sich eine Rolle hinzuzufügen die höher als die erlaubt ist')    
        else:
            role = get(member.guild.roles, name=para)
            # prüfe ob die gewünschte Rolle in der hirarchie höher liegt als die erlaubte
            if role.position < highestrole.position:
                await member.add_roles(role)
                await context.send('Die Rolle ' + str(role) + ' ? oh ja, das kann ich für dich tun!')
                logger.info(str(member) + ' hat sich die Rolle ' + str(role) + ' zugewiesen')
                time.sleep(0.5)
            else:
                await context.send('kann die Rolle ' + str(role) + ' nicht hinzufügen')
                logger.info(str(member) + ' hat versucht sich eine Rolle hinzuzufügen die höher als die erlaubt ist')    

        await context.send(':sparkles:' + '*poof*' + ':sparkles:')
        await context.message.delete()           

    @commands.command()

    # Der !addall Befehl fügt einem Nutzer alle Verfügbaren Rollen an.
    # Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
    # @commands.has_role("Der Architekt")

    async def addall(self, context):

        """Du glaubst jedes Spiel zu haben? 
        Dann gib dir doch fix einfach alle Gamingrollen um überall mit zu mischen"""

        author = context.message.author
        nick = author.display_name
        lowest = get(context.guild.roles, name='@everyone')
        highestrole = get(context.guild.roles, name='Nutzer')
        smbed = discord.Embed(
            title=':sparkles:' + '*poof*' + ':sparkles:',
            description='Ich bin Mr Meeseeks, schaut mich an.\nAlle Rollen? Oh ja, das kann ich für dich tun!',
            color=discord.Color.green()
            )
        addedroles = ''

        for role in context.guild.roles:
            if role.position < highestrole.position and role.position > lowest.position:
                await author.add_roles(role)
                addedroles += str(role) + '\n'
        
        addedroles += ' \n'
        smbed.add_field(
            name=f'@{nick}´s neue Rollen',
            value=addedroles+':sparkles:' + '*poof*' + ':sparkles:',
            inline=False
            )
        await context.send(embed=smbed)
        await context.message.delete()

    @commands.command()

    # Der !rmrole Befehl entfernt eine bestimmte Rolle von einem Nutzer.
    # Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
    # @commands.has_role("Der Architekt")

    async def rmrole(self, context, rolename):

        """nimmt dir eine oder mehrere Rollen ab (mit Komma getrennt), um dein Interface sauber zu halten."""

        # prüfe ob ein Komma in rolename vorhanden ist , wenn ja werden mehrere Rollen entfernt

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
        logger.info(str(member) + ' called addrole')
        highestrole = get(context.guild.roles, name='Nutzer')

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
                    await member.remove_roles(role)
                    await context.send('Du willst die Rolle ' + str(role) + ' nicht mehr? oh ja, das kann ich für dich tun!')
                    logger.info(str(member) + ' hat sich die Rolle ' + str(role) + ' zugewiesen')
                    time.sleep(0.5)
                else:
                    await context.send('kann die Rolle ' + str(role) + ' nicht entfernen')
                    logger.info(str(member) + ' hat versucht sich eine Rolle hinzuzufügen die höher als die erlaubt ist')    
        else:
            role = get(member.guild.roles, name=para)
            # prüfe ob die gewünschte Rolle in der hirarchie höher liegt als die erlaubte
            if role.position < highestrole.position:
                await member.remove_roles(role)
                await context.send('Du willst die Rolle ' + str(role) + ' nicht mehr? oh ja, das kann ich für dich tun!')
                logger.info(str(member) + ' hat sich die Rolle ' + str(role) + ' zugewiesen')
                time.sleep(0.5)
            else:
                await context.send('kann die Rolle ' + str(role) + ' nicht entfernen')
                logger.info(str(member) + ' hat versucht sich eine Rolle hinzuzufügen die höher als die erlaubt ist')    

        await context.send(':sparkles:' + '*poof*' + ':sparkles:')
        await context.message.delete()  

    @commands.command()

    # Der !rmall Befehl enfernt alle Rollen von einem Nutzer.
    # Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
    # @commands.has_role("Der Architekt")

    async def rmall(self, context):

        """Keine Lust mehr auf Gaming? Dann nimm dir doch einfach alle Rollen"""

        author = context.message.author
        nick = author.display_name
        lowest = get(context.guild.roles, name='@everyone')
        highestrole = get(context.guild.roles, name='Nutzer')
        smbed = discord.Embed(
            title=':sparkles:' + '*poof*' + ':sparkles:',
            description='Ich bin Mr Meeseeks, schaut mich an.\nAlle Rollen abgeben?\nOh ja, das kann ich für dich tun!',
            color=discord.Color.dark_orange()
            )
        addedroles = ''

        for role in context.guild.roles:
            if role.position < highestrole.position and role.position > lowest.position:
                await author.remove_roles(role)
                addedroles += str(role) + '\n'
        
        addedroles += ' \n'
        smbed.add_field(
            name=f'@{nick}´s entfernte Rollen',
            value=addedroles+':sparkles:' + '*poof*' + ':sparkles:',
            inline=False
            )
        await context.send(embed=smbed)
        await context.message.delete()


def setup(bot):
    bot.add_cog(MemberCommands(bot))