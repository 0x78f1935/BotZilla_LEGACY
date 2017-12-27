"""
Informative commands for the bot.
"""
import time
import json
import discord
from discord.ext import commands
import asyncio
import urllib.request
import urllib.parse
import traceback
import io
import re
from io import BytesIO
from discord.errors import HTTPException
from options.utils import chat_formatting, dataIO, downloader
from collections import defaultdict

def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)


class NoPrivateMessages(commands.CheckFailure):
    pass

def guild_only():
    async def predicate(ctx):
        if ctx.guild is None:
            raise NoPrivateMessages('Hey no DMs!')
        return True
    return commands.check(predicate)


class Polls:
    """Poll voting system."""

    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']


    @commands.command(pass_context=True)
    async def poll(self, ctx, *questions_and_choices: str):
        """Makes a poll quickly for your server.
        The first argument is the question and the rest are the choices.
        You can only have up to 20 choices and one question.
        Use `;` as a delimiter.
        Example: question? answerA; answer B; answerC
        """

        if str(questions_and_choices) == '()':
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='It\'s not a bad idea to read `{}help poll` first'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        try:
            question = re.search(r'(.*?)\?', str(questions_and_choices)).group(0)
            question = re.sub(r'[(|$|.|!|\'|,]', r'', str(question))
            left_over = re.search(r'\?(.*$)', str(questions_and_choices)).group(0)
            choices = re.sub(r'[(|$|.|!|\'|,|)]', r'', str(left_over))
            choices = re.sub(r'[?]', r'', str(choices))
            choices = choices.split(';')
            answers = []
            for choice in choices:
                answers.append(choice)

            if '' in answers:
                answers.remove('')

            if len(answers) < 2:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='You need atleast two answers',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return
            elif len(answers) > 21:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='You have more than 20 answers',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                return

            choices = [(to_emoji(e), v) for e, v in enumerate(answers)]

            try:
                await ctx.message.delete()
            except:
                pass
            embed = discord.Embed(title='{} asks:'.format(ctx.message.author.name),
                                  description='**{}**'.format(question),
                                  colour=0xf20006)
            for key, c in choices:
                embed.add_field(name='{} Answer:'.format(':gear:'), value='{} : {}\n'.format(key, c), inline=False)
            a = await self.bot.say(embed=embed)
            for emoji, _ in choices:
                await self.bot.add_reaction(a, emoji)

        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Don\'t forget the question..\nQuestion: did you read the `{}help poll`?'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            await asyncio.sleep(10)
            print(a.reaction.count-1)


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
        self.downloader = downloader.Downloader()

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


    @commands.command(pass_context=True)
    async def pldump(self, ctx, *, song_url):
        """
        Dumps the individual urls of a playlist
        Maybe usefull if you are a bot dev
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        try:
            info = await self.downloader.extract_info(self.loop, song_url.strip('<>'), download=False, process=False)
        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Could not extract info from input url\nI\'m confident you could use **`{}help pldump`** instead'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        if not info:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Could not extract info from input url, No data',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        if not info.get('entries', None):
            # TODO: Retarded playlist checking
            # set(url, webpageurl).difference(set(url))

            if info.get('url', None) != info.get('webpage_url', info.get('url', None)):
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='This does not seem to be a playlist.',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                return
            else:
                return await self.cmd_pldump(ctx.message.channel, info.get(''))

        linegens = defaultdict(lambda: None, **{
            "youtube":    lambda d: 'https://www.youtube.com/watch?v=%s' % d['id'],
            "soundcloud": lambda d: d['url'],
            "bandcamp":   lambda d: d['url']
        })

        exfunc = linegens[info['extractor'].split(':')[0]]

        if not exfunc:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Could not extract info from input url, unsupported playlist type.',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        with BytesIO() as fcontent:
            for item in info['entries']:
                fcontent.write(exfunc(item).encode('utf8') + b'\n')

            fcontent.seek(0)
            await self.bot.send_file(ctx.message.channel,
                                     fcontent,
                                     filename='playlist.txt',
                                     content="Here's the url dump for {}".format(song_url))

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description=':mailbox_with_mail:',
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Information(bot))
    bot.add_cog(Polls(bot))