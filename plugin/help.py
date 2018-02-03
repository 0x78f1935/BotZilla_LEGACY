import discord
from discord.ext import commands
import json
try:
    from plugin.database import Database
except:
    pass


tmp_config = json.loads(str(open('./options/config.js').read()))
config = tmp_config['config']
owner_list = config['owner-id']


class Help:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']
        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except:
            print('Help: Database files not found')
            pass

    @commands.command(pass_context=True, hidden=True)
    async def t(self, ctx, command: str = None):
        """
        Show this message
        """
        all_cogs = ['Exchange', 'Fun', 'GameStats']
        command_list = []
        embed = discord.Embed(title="Help for {}:".format(ctx.message.author.name),
                              color=0xf20006)
        for cog in all_cogs:

            self.database.cur.execute("select name from botzilla.help where cog = '{}';".format(cog))
            cog = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            commands = []
            for i in cog:
                i = '`{}{}`'.format(self.config['prefix'], i[0])
                commands.append(i)
                command_list.append("\n".join(commands))

            for command in command_list:
                embed.add_field(name=cog, value=command, inline=True)


        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Help(bot))