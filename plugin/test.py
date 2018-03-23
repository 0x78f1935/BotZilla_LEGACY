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
        pass




   @commands.command()
    @commands.cooldown(1, 30, type=commands.BucketType.user)
    async def infect(self, ctx, member:discord.Member, emoji):
        if member.id == self.bot.user.id and ctx.author.id != owner_id:
            await ctx.send(f'You rolled a Critical Fail...\nInfection bounces off and rebounds on the attacker.')
            member = ctx.author
        if member in self.bot.infected:
            await ctx.send(f'{member.display_name} is already infected. Please wait until they are healed before infecting them again...')
        else:
            emoji = self.bot.get_emoji(int(emoji.split(':')[2].strip('>'))) if '<:' in emoji or '<a:' in emoji else emoji
            self.bot.infected[member] = [emoji,datetime.now().timestamp()]
            await ctx.send(f"{member.display_name} has been infected with {emoji}")


def setup(bot):
    bot.add_cog(TestScripts(bot))