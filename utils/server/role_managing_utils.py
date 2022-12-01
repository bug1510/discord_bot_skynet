import logging

class RoleManagingUtils():
    def __init__(self) -> None:
        self.logger = logging.getLogger('SkyNet-Core.Role_Managing_Utils')
    
    async def create_role(self, guild, name, member, embed):
        try:
            role = await guild.create_role(name=name)
            self.logger.info(f'{member} created role {name} successfully')
            embed.add_field(
                name= '!Success creating Role!',
                value= f'Die Rolle {role} wurde erstellt.',
                inline=False
            )
            return role, embed

        except Exception as e:
            self.logger.info(f'{member} tried to create role {name} but it failed due to an error: {e}')
            embed.add_field(
                name= '!Failure creating Category connected Role!',
                value= f'Die Rolle {name} wurde nicht erstellt,\n{e}.',
                inline=False
            )
            return embed

    async def delete_role(self, role, member, embed):
        try:
            await role.delete(reason=None)

            self.logger.info(f'{member} deleted the role {role} successfully')
            embed = embed.add_field(
                name= '!Success deleting Role!',
                value= f'Die Rolle {role} wurde gelöscht.',
                inline=False
            )
        except Exception as e:
            self.logger.warning(f'{member} tried to delete the role {role} but it failed due to an error: {e}')
            embed = embed.add_field(
                name= '!Failure deleting Role!',
                value= f'Beim löschen der Rolle {role} ist etwas schief gelaufen,\n{e}.',
                inline=False
            )
        finally:
            return embed