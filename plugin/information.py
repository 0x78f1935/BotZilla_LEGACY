"""
Informative commands for the bot.
"""
import time
import json
import discord
from discord.ext import commands
import urllib.request
import urllib.parse
import traceback
import io
import re


class Information:
    """
    Informative commands for the bot.
    """

    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']

    # ========================
    #   Bot related commands

    @commands.command(pass_context=True, aliases=["oauth", "invite"])
    async def join(self, ctx):
        """Add BotZilla to your channel!
        Gives BotZilla OAuth url. Use this to add him to your channel!"""

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Use the following url to add BotZilla V2 to your guild!\n**{}**'.format(
                                  discord.utils.oauth_url(self.bot.user.id)),
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Check server response.
        Sends a package to the discord server.
        Calculates response time"""
        before = time.monotonic()
        await (await self.bot.ws.ping())
        after = time.monotonic()
        ping_result = (after - before) * 1000
        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Pong :ping_pong: **{0:.0f}ms**'.format(ping_result),
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def count(self, ctx):
        """Give information on how many servers Botzilla is active in.
        Also shows additional information"""
        embed = discord.Embed(title="{}".format("Server Count"),
                              description="We are in **{}** servers \nWe have **{}** members".format(
                                  str(len(self.bot.servers)), str(len(set(self.bot.get_all_members())))),
                              color=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def id(self, ctx):
        """Shows your ID.
        Get users ID."""
        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Your ID is **{}**'.format(str(ctx.message.author.id)),
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, hidden=True)
    async def say(self, ctx, *, message=None):
        """Say something as BotZilla.
        This only works in the direct
        channel the command is used in."""

        if message is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Maybe you should considering using `{}help say` instead'.format(self.config['prefix']),
                                  colour=0xf20006)
            await self.bot.say(embed=embed)
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format(str(message)),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, hidden=True)
    async def emoji(self, ctx, *, emoji : str =None):
        """
        Shows information about the emoji.
        """
        if emoji is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Try `{}help emoji`, That would help..'.format(self.config['prefix']),
                                  colour=0xf20006)
            self.bot.say(embed=embed)
            return

        url = 'https://canary.discordapp.com/api/v6/channels/{}/messages/{}/reactions/emoji/@me'.format(ctx.message.channel, emoji)

        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})) as response:
                source = response.read()
            data = json.loads(source)

            print(json.dumps(data, indent=2))

        except Exception as e:
            stdout = io.StringIO()
            value = stdout.getvalue()
            log_new = re.search(r'.+?(?= in position)', str(traceback.format_exc()), flags=0).group(0)
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='```py\n{}{}\n```'.format(value, log_new),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Information(bot))