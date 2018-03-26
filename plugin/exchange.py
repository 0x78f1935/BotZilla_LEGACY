import json
import discord
from discord.ext import commands
import aiohttp
import decimal
import datetime


try:
    from plugin.database import Database
except:
    pass

class Exchange:
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

    @commands.command(pass_context=True, aliases=["btc"])
    async def bitcoin(self, ctx):
        """
        Shows current bitcoin value
        Show bitcoin value from exchange
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!bitcoin in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        url = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
        cent = decimal.Decimal('0.01')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.json()

        source = json.dumps(source)
        data = json.loads(str(source))

        embed = discord.Embed(title="{}".format("Bitcoin :currency_exchange:"),
                              description="Bitcoin price is currently at $**{}**".format(decimal.Decimal(float(data[0]['price_usd'])).quantize(cent, decimal.ROUND_UP)),
                              color=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, aliases=["eth"])
    async def ethereum(self, ctx):
        """
        Shows current Ethereum value
        Show Ethereum value from exchange
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!ethereum in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        url = 'https://api.coinmarketcap.com/v1/ticker/Ethereum/'
        cent = decimal.Decimal('0.01')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.json()

        source = json.dumps(source)
        data = json.loads(str(source))

        embed = discord.Embed(title="{}".format("Ethereum :currency_exchange:"),
                              description="Ethereum price is currently at $**{}**".format(decimal.Decimal(float(data[0]['price_usd'])).quantize(cent, decimal.ROUND_UP)),
                              color=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

    @commands.command(pass_context=True)
    async def ripple(self, ctx):
        """
        Shows current Ripple value
        Show Ripple value from exchange
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!ripple in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        url = 'https://api.coinmarketcap.com/v1/ticker/Ripple/'
        cent = decimal.Decimal('0.01')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.json()

        source = json.dumps(source)
        data = json.loads(str(source))

        embed = discord.Embed(title="{}".format("Ripple :currency_exchange:"),
                              description="Ripple price is currently at $**{}**".format(decimal.Decimal(float(data[0]['price_usd'])).quantize(cent, decimal.ROUND_UP)),
                              color=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, aliases=["lte"])
    async def litecoin(self, ctx):
        """
        Shows current Litecoin value
        Show Litecoin value from exchange
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!litecoin in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        url = 'https://api.coinmarketcap.com/v1/ticker/Litecoin/'
        cent = decimal.Decimal('0.01')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.json()

        source = json.dumps(source)
        data = json.loads(str(source))

        embed = discord.Embed(title="{}".format("Litecoin :currency_exchange:"),
                              description="Litecoin price is currently at $**{}**".format(decimal.Decimal(float(data[0]['price_usd'])).quantize(cent, decimal.ROUND_UP)),
                              color=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, aliases=["doge"])
    async def dogecoin(self, ctx):
        """
        Shows current Dogecoin value
        Show Dogecoin value from exchange
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!dogecoin in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        url = 'https://api.coinmarketcap.com/v1/ticker/Dogecoin/'
        cent = decimal.Decimal('0.01')
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.json()

        source = json.dumps(source)
        data = json.loads(str(source))

        embed = discord.Embed(title="{}".format("Dogecoin :currency_exchange:"),
                              description="Dogecoin price is currently at $**{}**".format(decimal.Decimal(float(data[0]['price_usd'])).quantize(cent, decimal.ROUND_UP)),
                              color=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Exchange(bot))
