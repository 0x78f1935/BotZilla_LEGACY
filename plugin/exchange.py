from discord.ext import commands
import json
import aiohttp
import discord

tmp_config = json.loads(str(open('./options/config.js').read()))
config = tmp_config['config']
owner_list = config['owner-id']

class MoneyMaker:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']


    @commands.command(pass_context=True)
    async def bitcoin(self, ctx):
        """Shows current bitcoin value
        Show bitcoin valua from exchange"""
        url = tmp_config['exchange']['api-url']
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.text(encoding='utf8')

        source = json.dumps(source)
        data = json.loads(str(source))

        embed = discord.Embed(title="{}".format("Bitcoin :currency_exchange:"),
                              description="Bitcoin price is currently at $**{}**".format(str(data['bpi']['USD']['rate'])),
                              color=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(MoneyMaker(bot))