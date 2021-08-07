import time
from discord.ext import commands
from discord.utils import get


class MemberCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Die folgenden Zeilen sind das Rollen Feature des Kirkland Meeseeks.

    @commands.command()

    # Der !lsrole Befehl Listet die bereits verfügbaren Rollen auf.

    async def lsrole(self, context):

        """Dieser Befehl Listet dir die für dich bereits verfügbaren Rollen auf"""

        lowest = get(context.guild.roles, name='@everyone')
        highestrole = get(context.guild.roles, name='Groovy')
        member = context.message.author
        #logging.info(str(member) + ' called lsrole')

        for role in context.guild.roles:
            
            if role.position < highestrole.position and role.position > lowest.position:
                await context.send(role)
                time.sleep(0.75)

    @commands.command()

    # Der !addrole Befehl fügt einem Nutzer eine bestimmte Rolle an.
    # Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
    # @commands.has_role("Der Architekt")

    async def addrole(self, context, rolename):

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
        #logging.info(str(member) + ' called addrole')
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
                    await context.send('Rolle ' + str(role) + ' wurde hinzugefügt')
                    #logging.info(str(member) + ' hat sich die Rolle ' + str(role) + ' zugewiesen')
                    time.sleep(0.5)
                else:
                    await context.send('kann die Rolle ' + str(role) + ' nicht hinzufügen')
                    #logging.info(str(member) + ' hat versucht sich eine Rolle hinzuzufügen die höher als die erlaubt ist')    
        else:
            role = get(member.guild.roles, name=para)
            # prüfe ob die gewünschte Rolle in der hirarchie höher liegt als die erlaubte
            if role.position < highestrole.position:
                await member.add_roles(role)
                await context.send('Rolle ' + str(role) + ' wurde hinzugefügt')
                #logging.info(str(member) + ' hat sich die Rolle ' + str(role) + ' zugewiesen')
                time.sleep(0.5)
            else:
                await context.send('kann die Rolle ' + str(role) + ' nicht hinzufügen')
                #logging.info(str(member) + ' hat versucht sich eine Rolle hinzuzufügen die höher als die erlaubt ist')    

        await context.send(':sparkles:' + '*poof*' + ':sparkles:')           

    @commands.command()

    # Der !addall Befehl fügt einem Nutzer alle Verfügbaren Rollen an.
    # Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
    # @commands.has_role("Der Architekt")

    async def addall(self, context):

        """Du glaubst jedes Spiel zu haben? 
        Dann gib dir doch fix einfach alle Gamingrollen um überall mit zu mischen"""

        author = context.message.author
        lowest = get(context.guild.roles, name='@everyone')
        highestrole = get(context.guild.roles, name='Groovy')
        
        await context.send(':sparkles:' + '*poof*' + ':sparkles:')
        await context.send('Was willst du? Alle Rollen? Oh ja, das kann ich für dich tun!')
        for role in self.guild.roles:
            
            if role.position < highestrole.position and role.position > lowest.position:
                await author.add_roles(role)

        await self.send(':sparkles:' + '*poof*' + ':sparkles:')

    @commands.command()

    # Der !rmrole Befehl entfernt eine bestimmte Rolle von einem Nutzer.
    # Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
    # @commands.has_role("Der Architekt")

    async def rmrole(self, context, rolename):

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

    @commands.command()

    # Der !rm3role Befehl entfernt drei bestimmte Rolle von einem Nutzer.
    # Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
    # @commands.has_role("Der Architekt")

    async def rm3roles(self, context, rolename1, rolename2, rolename3):

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

    @commands.command()

    # Der !rmall Befehl enfernt alle Rollen von einem Nutzer.
    # Sicherheitsfunktion zu Testzwecken, kann nach Konfiguration deaktiviert werden.
    # @commands.has_role("Der Architekt")

    async def rmall(self, context):

        """Keine Lust mehr auf Gaming? Dann nimm dir doch einfach alle Rollen"""

        author = context.message.author
        lowest = get(context.guild.roles, name='@everyone')
        highestrole = get(context.guild.roles, name='Groovy')
        
        await context.send(':sparkles:' + '*poof*' + ':sparkles:')
        await context.send('Was willst du? Alle Rollen abgeben? Oh ja, das kann ich für dich tun!')
        for role in self.guild.roles:
            
            if role.position < highestrole.position and role.position > lowest.position:
                await author.remove_roles(role)

        await context.send(':sparkles:' + '*poof*' + ':sparkles:')


def setup(bot):
    bot.add_cog(MemberCommands(bot))