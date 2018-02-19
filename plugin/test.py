import discord
from discord.ext import commands
import json
import datetime
import random
import aiohttp

tmp_config = json.loads(str(open('./options/config.js').read()))
config = tmp_config['config']
owner_list = config['owner-id']


class TestScripts:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']

    @commands.group(pass_context=True, hidden=True)
    async def hello(self, ctx):
        """
        This is a group with commands
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!hello in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if ctx.invoked_subcommand is None:
            message = 'Hello {}'.format(ctx.message.author.name)
            embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                  description="```**{}**```".format(message),
                                  color=0xf20006)
            embed.set_author(name="Example", url="http://www.example.com",
                          icon_url="https://cdn.discordapp.com/icons/265828729970753537/0c4fc42c61804747b54300282d0d7629.jpg")
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def sebisauce(self, ctx):
        """
        Sebisauce
        """
        url = 'https://sebisauce.herokuapp.com/api/random'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.json(encoding='utf8')
        source = json.dumps(source)
        data = json.loads(source)
        im = data['file']
        embed = discord.Embed(title='\t', description='\t', color=0xf20006)
        embed.set_image(url=im)
        await self.bot.say(embed=embed)


    async def sebisauce_old(self, ctx):
        """
        Sebisauce
        """
        await self.bot.send_typing(ctx.message.channel)
        sebisauce_img = ['https://cdn.discordapp.com/attachments/407238426417430539/414844386212446210/sebisauce_3.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844423382368277/sebisauce_1.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844448367968276/sebisauce_2.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844479519064064/sebisauce_6.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844498779176961/sebisauce_8.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844517032787979/sebisauce_9.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844533898084352/sebisauce_10.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844552730640384/sebisauce_12.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844574385569794/sebisauce_13.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844592048046090/sebisauce_14.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844605885054976/sebisauce_15.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414860605976084490/unknown.png']

        url = random.choice(sebisauce_img)
        embed = discord.Embed(title="\t",
                              description="\t",
                              color=0xf20006)
        embed.set_image(url=url)
        await self.bot.say(embed=embed)

########################################################################################################################################


def setup(bot):
    bot.add_cog(TestScripts(bot))