import json
import discord
from discord.ext import commands
import aiohttp
from bs4 import BeautifulSoup
import random
import datetime


try:
    from plugin.database import Database
except:
    pass

class TestScripts:
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
        except Exception as e:
            print('Test: Database files not found - {}'.format(e.args))
            pass

    @commands.command(pass_context=True)
    async def test(self, ctx, member:discord.Member = None, emoji : str = None):
        """
        Now is your chance to infect someone with reactions!
        Each infect has a duration of one hour.
        Usage:
          - !!infect <username | ping | id> <emoji>
        Example:
          - !!infect puffdip :smirk:
          - !!infect @puffdip :smiley:
          - !!infect 275280442884751360 :wink:
        """

        self.database.cur.execute("SELECT ID from botzilla.infect;")
        members_who_already_infected = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")

        if member is None or emoji is None:
            embed = discord.Embed(title=f'{ctx.message.author.name}',
                                  description=f'To get help on how to infect someone.\nUse ***`{self.config["prefix"]}help infect`***',
                                  color=0xf20006)
            await self.bot.say(embed=embed)
            return

        if str(member.id) in str(members_who_already_infected):
            await self.bot.say(f'{member.name} is already infected')
        else:
            now = datetime.datetime.now()
            until = now + datetime.timedelta(hours=1)
            self.database.cur.execute("INSERT INTO botzilla.infect(ID, until, emoji) VALUES({}, '{}', '{}');".format(member.id, until, emoji))
            self.database.conn.commit()
            self.database.cur.execute("ROLLBACK;")
            await self.bot.say(f'**`{member.name}`** has been infected with **{emoji}** for **`one`** hour')

def setup(bot):
    bot.add_cog(TestScripts(bot))