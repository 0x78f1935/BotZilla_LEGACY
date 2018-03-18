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
    async def test(self, ctx):

        hrefs = []
        sebisauce = []
        url = 'https://github.com/AnakiKaiver297/sebisauce'

        await self.bot.send_typing(ctx.message.channel)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.read()

        bs = BeautifulSoup(html)
        for link in bs.find_all('a'):
            if link.has_attr('href'):
                hrefs.append(link.attrs['href'])

        for i in hrefs:
            if 'sebisauce/blob/master' in str(i):
                sebisauce.append(i)

        im = 'https://github.com' + random.choice(sebisauce) + '?raw=true'
        print(im)
        embed = discord.Embed(title='\t', description='\t', color=0xf20006)
        embed.set_image(url=im)
        await self.bot.say(embed=embed)

def setup(bot):
    bot.add_cog(TestScripts(bot))