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
        self.database.cur.execute("select name from botzilla.help where cog = 'Information';")
        Information_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Information_commands = []
        for i in Information_cog:
            i = '`{}{}`'.format(self.config['prefix'], i[0])
            Information_commands.append(i)
        Information_name = "\n".join(Information_commands)

        self.database.cur.execute("select name from botzilla.help where cog = 'Music';")
        Music_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Music_commands = []
        for i in Music_cog:
            i = '`{}{}`'.format(self.config['prefix'], i[0])
            Music_commands.append(i)
        Music_name = "\n".join(Music_commands)

        self.database.cur.execute("select name from botzilla.help where cog = 'Utils';")
        Utils_cog = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        Utils_commands = []
        for i in Utils_cog:
            i = '`{}{}`'.format(self.config['prefix'], i[0])
            Utils_commands.append(i)
        Utils_name = "\n".join(Utils_commands)

        embed = discord.Embed(title="Help for {}:".format(ctx.message.author.name),
                              color=0xf20006)

        embed.add_field(name='Information', value=Information_name, inline=True)
        embed.add_field(name='Music', value=Music_name, inline=True)
        embed.add_field(name='Utils', value=Utils_name, inline=True)

        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Help(bot))