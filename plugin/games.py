from discord.ext import commands
import urllib.request
import urllib.parse
import json
import random
import discord


class Games:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']


    @commands.command(pass_context=True, name='8ball')
    async def ball8(self, ctx , *, question: str = None):
        """
        8ball! Ask BotZilla Any question.
        """
        question = question.lower()
        ball = random.randint(1, 20)

        # uncomment the following line to let the user now what number is picked by 8ball
        # ball_anaunce = await self.safe_send_message(channel, "8Ball chose number %s" % (ball))

        if question is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: You did not fully address your question!',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['Warning'])
            return

        if ball == 1:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: It is certain',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f605') # Done
            return

        if ball == 2:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: It is decidedly so',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f913') # Done
            return

        if ball == 3:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Without a doubt',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f611') # Done
            return

        if ball == 4:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Yes, definitely!',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f98b') # Done
            return

        if ball == 5:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: You may rely on it',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f60c') # Done
            return

        if ball == 6:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: As I see it, yes',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f48d') # Done
            return

        if ball == 7:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Most likely',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f609') # Done
            return

        if ball == 8:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Outlook good',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f44c') # done
            return

        if ball == 9:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Yes',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f525') # Done
            return

        if ball == 10:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Signs point to yes',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f607') # Done
            return

        if ball == 11:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Reply hazy try again',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f47b') # Done
            return

        if ball == 12:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Ask again later',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f550') # Done
            return

        if ball == 13:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Better not tell you now',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\u2620') # Done
            return

        if ball == 14:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Cannot predict now',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f914') # Done
            return

        if ball == 15:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Concentrate and ask again',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f616') # Done
            return

        if ball == 16:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Don\'t count on it',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f625') # Done
            return

        if ball == 17:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: My reply is no',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f4a9') # Done
            return

        if ball == 18:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: My sources say no',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f614') # Done
            return

        if ball == 19:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Outlook not so good',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f60f') # Done
            return

        if ball == 20:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Very doubtful',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f61f') # Done
            return


    @commands.command(pass_context=True)
    async def joke(self, ctx):
        """
        Ever heard a Chuck Norris joke?
        """
        url = 'http://api.icndb.com/jokes/random%22'
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})) as response:
            source = response.read().decode('utf-8')
        data = json.loads(source)
        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description="{}".format(data['value']['joke']),
                              colour=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
        return


def setup(bot):
    m = Games(bot)
    bot.add_cog(m)
