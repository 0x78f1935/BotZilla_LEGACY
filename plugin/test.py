import discord
from discord.ext import commands
import json
import re


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
        """This is a group with commands"""
        if ctx.invoked_subcommand is None:
            message = 'Hello {}'.format(ctx.message.author.name)
            embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                  description="```**{}**```".format(message),
                                  color=0xf20006)
            embed.set_author(name="Example", url="http://www.example.com",
                          icon_url="https://cdn.discordapp.com/icons/265828729970753537/0c4fc42c61804747b54300282d0d7629.jpg")
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(TestScripts(bot))