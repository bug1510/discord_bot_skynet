import time
from typing import List
from unicodedata import name
import discord
from discord import member
from discord.ext import commands
from discord.utils import get
import logging

logger = logging.getLogger('SkyNet-Core.Member_Utils')

async def adding_roles(member, roles, embed):

    added_roles = ''
    not_added_roles = ''

    if roles.find(",") > 0:
        para = roles.split(",")
    else:
        para = [roles]

    for e in para:
        role = get(member.guild.roles, name=e)
        # prüfe ob die gewünschte Rolle in der hirarchie höher liegt als die erlaubte
        if role.position < highestrole.position:
            await member.add_roles(role)
            
            embed.add_field(
                name='!Success adding roles!',
                value=added_roles
                )
            
            logger.info(f'{member} hat die Rolle {role} zugewiesen bekommen')
        else:
            
            embed.add_field(
                name='!Error adding Roles!',
                value=not_added_roles
                )
            logger.info(f'{member} hat versucht eine Rolle hinzuzufügen die höher als die, welche erlaubt sind')
            

async def removing_roles(member, roles, embed):

        if role.find(",") > 0:
            # mehrere Rollen gefunden
            multi = True
            para = role.split(",")
        else:
            # nur eine Rolle
            multi = False
            para = role

        # definiere variablen
        member = ctx.message.author
        logger.info(str(member) + ' called addrole')
        highestrole = get(ctx.guild.roles, name='Nutzer')

        await ctx.send(':sparkles:' + '*poof*' + ':sparkles:')
        await ctx.send('Was willst du?')
        time.sleep(1)

        # prüfen ob mehrere Rollen hinzugefügt werden müssen
        if multi:
            # durchlaufe das array für jeden eintrag
            for e in para:
                role = get(member.guild.roles, name=e)
                # prüfe ob die gewünschte Rolle in der hirarchie höher liegt als die erlaubte
                if role.position < highestrole.position:
                    await member.remove_roles(role)
                    await ctx.send('Du willst die Rolle ' + str(role) + ' nicht mehr? oh ja, das kann ich für dich tun!')
                    logger.info(str(member) + ' hat sich die Rolle ' + str(role) + ' zugewiesen')
                    time.sleep(0.5)
                else:
                    await ctx.send('kann die Rolle ' + str(role) + ' nicht entfernen')
                    logger.info(str(member) + ' hat versucht sich eine Rolle hinzuzufügen die höher als die erlaubt ist')    
        else:
            role = get(member.guild.roles, name=para)
            # prüfe ob die gewünschte Rolle in der hirarchie höher liegt als die erlaubte
            if role.position < highestrole.position:
                await member.remove_roles(role)
                await ctx.send('Du willst die Rolle ' + str(role) + ' nicht mehr? oh ja, das kann ich für dich tun!')
                logger.info(str(member) + ' hat sich die Rolle ' + str(role) + ' zugewiesen')
                time.sleep(0.5)
            else:
                await ctx.send('kann die Rolle ' + str(role) + ' nicht entfernen')
                logger.info(str(member) + ' hat versucht sich eine Rolle hinzuzufügen die höher als die erlaubt ist')    

        await ctx.send(':sparkles:' + '*poof*' + ':sparkles:')
        await ctx.message.delete()  
