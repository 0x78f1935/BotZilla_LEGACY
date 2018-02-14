from discord.ext import commands
import datetime
import json
import random
import discord
import asyncio


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
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!8ball in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
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


    @commands.command(pass_context=True, name='highlow')
    async def HighLow(self, ctx):
        """
        Higher or Lower? Gamble your way out! 0 ~ 1.000
        Is the next number higher or lower then your current number?
        Vote with the whole server!
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!highlow in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        while True:
            number = random.randrange(0,1000)
            embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                  description='Higher or Lower than: **`{}`**\n**`10`** Seconds to vote..'.format(number),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\U0001f53c')
            await self.bot.add_reaction(a, '\U0001f53d')
            await asyncio.sleep(10)
            new_number = random.randrange(0,1000)

            message = await self.bot.get_message(ctx.message.channel, a.id)
            more = message.reactions[0]
            less = message.reactions[1]
            total_more = more.count - 1
            total_less = less.count - 1
            total_votes = total_more + total_less
            vote_list = [total_more, total_less]
            winner = max(vote_list)
            await self.bot.delete_message(a)

            if total_votes == 0:
                embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                      description='GameOver! Nobody voted...\nUse **`{}highlow`** to start a new game'.format(self.config['prefix']),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, '\U0001f480')
                break

            elif total_less == total_more:
                embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                      description='Vote Draw!\nContinue? **`10`** Seconds remaining'.format(new_number),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                await self.bot.add_reaction(a, '\U0001f3f3')
                await asyncio.sleep(10)
                message = await self.bot.get_message(ctx.message.channel, a.id)
                emoji_continue = message.reactions[0]
                total_continue = emoji_continue.count - 1
                await self.bot.delete_message(a)
                if total_continue == 0:
                    embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                          description='Gameover! Nobody to play with...\nStart a new game with **`{}highlow`**'.format(self.config['prefix']),
                                          colour=0xf20006)
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, '\U0001f60f')
                    break


            elif winner == total_more and new_number >= number:
                embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                      description='Victorious! You hit number **`{}`**\nYour previous number was **`{}`**\n\nTotals\n-------\n:arrow_up_small: : **`{}`**    :arrow_down_small: : **`{}`**\nTotal Votes: **`{}`**\n\nNext round in **`10`** Seconds'.format(new_number, number, total_more, total_less, total_votes),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                await asyncio.sleep(10)
                await self.bot.delete_message(a)

            elif winner == total_less and new_number <= number:
                embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                      description='Victorious! You hit number **`{}`**\nYour previous number was **`{}`**\n\nTotals\n-------\n:arrow_up_small:  : **`{}`**    :arrow_down_small: : **`{}`**\nTotal Votes: **`{}`**\n\nNext round in **`10`** Seconds'.format(new_number, number, total_more, total_less, total_votes),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                await asyncio.sleep(10)
                await self.bot.delete_message(a)

            else:
                embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                      description='GameOver! You hit number **`{}`**\nYour previous number was **`{}`**\n\nTotals\n-------\n:arrow_up_small:  : **`{}`**    :arrow_down_small: : **`{}`**\nTotal Votes: **`{}`**\n\nUse **`{}highlow`** for a new game!'.format(new_number, number, total_more, total_less, total_votes, self.config['prefix']),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, '\U0001f480')
                break


def setup(bot):
    m = Games(bot)
    bot.add_cog(m)
