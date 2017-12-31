import discord
from discord.ext import commands
import json
import re
import asyncio


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


    @commands.command(pass_context=True, hidden=True)
    async def blacklist(self, ctx, *, username=None):
        """Starts a blacklist vote"""
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return


        if username is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Read **`{}help blacklist`** thats a command!'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
        else:
            username = username.replace('<@', '')
            username = username.replace('>', '')
            username = username.replace('!', '')
            embed = discord.Embed(title='Blacklist vote started by {}:'.format(ctx.message.author.name),
                                  description='Your vote is needed\nWould you like to blacklist:\n\n**{}**\n\nPeople who got blacklisted can\'t use BotZilla anymore.\nEven in other servers'.format(str(username)),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\u2705')
            await self.bot.add_reaction(a, '\U0001f1fd')
            await asyncio.sleep(10)
            print(a.reactions)
            total = self.bot.reactions.count(a.emoji('\u2705'))
            print(total)
            # except:
            #     embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
            #                           description='Invalid username'.format(str(username)),
            #                           colour=0xf20006)
            #     a = await self.bot.say(embed=embed)
            #     await self.bot.add_reaction(a, self.emojiUnicode['warning'])

def setup(bot):
    bot.add_cog(TestScripts(bot))


