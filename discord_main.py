# imports
import datetime
from dotenv import load_dotenv
import discord
from discord.ext import commands
import os

#  Loading env variables
load_dotenv('.env')


def get_prefix():
    with open('assets/text/prefix', 'r') as file:
        return file.readline()[0]


class CustomHelpCommand(commands.HelpCommand):
    def __init__(self):
        super().__init__()

    def get_ending_note(self):
        command_name = self.invoked_with
        return "Type {0}{1} <command/category> for more information | [Optional Arg], <Required Arg>".format(
            get_prefix(), command_name)

    async def send_bot_help(self, mapping):
        help_command = discord.Embed(
            title='Help is on the way',
            description=f'Heard you needed help! Here are all the commands you can access. {client.description}',
            colour=discord.Colour.blurple(),

        )
        for cog in mapping:
            if cog is not None:
                cog_name = cog.qualified_name
            else:
                cog_name = 'Normie Commands'
            filtered = await self.filter_commands([command for command in mapping[cog]])
            value = os.linesep.join([("> " + command.name.title()) for command in filtered])
            if len(value) > 1:
                help_command.add_field(name=cog_name, value=value)

        help_command.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=help_command)
        return await super(CustomHelpCommand, self).send_bot_help(mapping)

    async def send_cog_help(self, cog):
        cog_embed = discord.Embed(
            title=cog.qualified_name,
            colour=discord.Colour.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        filtered = await self.filter_commands([command for command in cog.get_commands()], sort=True)
        for command in filtered:
            cog_embed.add_field(name=command.name.title(), value=command.help, inline=False)
        cog_embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=cog_embed)
        return await super(CustomHelpCommand, self).send_cog_help(cog)

    async def send_group_help(self, group):  # Don't Need
        return await super(CustomHelpCommand, self).send_group_help(group)

    async def send_command_help(self, command):
        ctx = self.context
        if len("|".join(command.aliases)) > 0:
            base = f'{get_prefix()}[{command.name}|{"|".join(command.aliases)}]'
        else:
            base = f'{get_prefix()}[{command.name}]'
        syntax = f'```{base} {command.signature}```'
        command_embed = discord.Embed(
            title=command.name.title(),
            description=command.help + '\n' + syntax,
            colour=discord.Colour.blurple(),
            timestamp=datetime.datetime.utcnow()
        )
        command_embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=command_embed)
        return await super(CustomHelpCommand, self).send_command_help(command)

#  setting up indents
intents = discord.Intents.default()
intents.message_content = True
client = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True,
                      help_command=CustomHelpCommand())


async def on_ready():
    await client.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="the latest developments in tech"))
    print('Bot is ready')


client.run(str(os.getenv('DISCORD_TOKEN')))
