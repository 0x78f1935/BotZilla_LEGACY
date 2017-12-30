from discord.ext import commands
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


    @commands.command(pass_context=True)
    async def cmd_8ball(self, ctx , *, question: str = None):
        question = question.lower()
        ball = random.randint(1, 20)

        # uncomment the following line to let the user now what number is picked by 8ball
        # ball_anaunce = await self.safe_send_message(channel, "8Ball chose number %s" % (ball))

        if question is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You did not fully address your question!\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['Warning'])
            return

        if ball == 1:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='It is certain\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f605') # Done
            return

        if ball == 2:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='It is decidedly so\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f913') # Done
            return

        if ball == 3:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Without a doubt\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f611') # Done
            return

        if ball == 4:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Yes, definitely!\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f98b') # Done
            return

        if ball == 5:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may rely on it\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f60c') # Done
            return

        if ball == 6:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='As I see it, yes\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f48d') # Done
            return

        if ball == 7:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Most likely\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f609') # Done
            return

        if ball == 8:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Outlook good\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f44c') # done
            return

        if ball == 9:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Yes\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f525') # Done
            return

        if ball == 10:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Signs point to yes\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f607') # Done
            return

        if ball == 11:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Reply hazy try again\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f47b') # Done
            return

        if ball == 12:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Ask again later\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f550') # Done
            return

        if ball == 13:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Better not tell you now\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\u2620') # Done
            return

        if ball == 14:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Cannot predict now\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f914') # Done
            return

        if ball == 15:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Concentrate and ask again\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f616') # Done
            return

        if ball == 16:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Don\'t count on it\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f625') # Done
            return

        if ball == 17:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='My reply is no\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f4a9') # Done
            return

        if ball == 18:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='My sources say no\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f614') # Done
            return

        if ball == 19:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Outlook not so good\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f60f') # Done
            return

        if ball == 20:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Very doubtful\n:8ball:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(last_message, '\U0001f61f') # Done
            return


def setup(bot):
    m = Games(bot)
    bot.add_cog(m)
