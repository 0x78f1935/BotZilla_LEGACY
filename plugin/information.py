"""
Informative commands for the bot.
"""
import time
import json
import discord
from discord.ext import commands
import asyncio
import re
import random
import ddg3 as duckduckgo3
import aiohttp


try:
    from plugin.database import Database
except:
    pass


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

        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except:
            print('Information: Database files not found')
            pass

    # ========================
    #   Bot related commands


    @commands.command(pass_context=True)
    async def poll(self, ctx, *questions_and_choices: str):
        """
        Makes a poll quickly for your server.
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


    @commands.command(pass_context=True)
    async def fact(self, ctx, *, search_term: str = None):
        """
        Search for a fact!
        Use this command in combination with a subject you like
        to get a fact for that subject
        """

        if search_term is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You really should reconsider reading the **`{}help fact`**'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        search_term = search_term.lower()

        if search_term == "botzilla":
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Best bot on the market right now! \nNo need for more information!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\U0001f44c')
            return


        try:
            search_number = random.randint(0, 1)
            r = duckduckgo3.query(search_term)
            related_type = r.type
            related_text = r.related[search_number].text
            'Python (programming language), a computer programming language'

            related_related = r.related[search_number].url
            print("Type: %s \nText: %s \nSource: %s" % (related_type, related_text, related_related))
            message2user = "Type: %s \nText: %s \nSource: %s" % (related_type, related_text, related_related)
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format(message2user),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            return

        except IndexError:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Nothing found...',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return


    @commands.command(pass_context=True, aliases=["oauth", "invite"])
    async def join(self, ctx):
        """
        Add BotZilla to your server!
        Gives BotZilla OAuth url. Use this to add him to your server!
        When the database restarts botzilla will automatically join voice channels
        with 'music' or 'Music' in the name.
        """

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Use the following url to add BotZilla V2 to your guild!\n**{}**'.format(
                                  discord.utils.oauth_url(self.bot.user.id)),
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """
        Check server response.
        Sends a package to the discord server.
        Calculates response time
        """
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
        """
        Give information about Botzilla.
        Count's the community, servers and more!
        """
        if self.database_file_found:
            self.database.cur.execute("select count(*) from botzilla.users;")
            rows = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            a = str(rows).replace('[(', '')
            self.total_users = a.replace(',)]', '')
            self.database.cur.execute("select extract(epoch from current_timestamp - pg_postmaster_start_time()) as uptime;")
            uptime = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            uptime = str(uptime).replace('[(', '').replace(',)]', '')
            uptime_in_minutes = str(float(uptime)/60).split('.')[0]
            uptime = '{} Minute(s)'.format(uptime_in_minutes)
            if int(uptime_in_minutes) >= 60:
                uptime_in_hours = str(float(uptime_in_minutes)/60).split('.')[0]
                uptime = '{} Hour(s)'.format(uptime_in_hours)
            if int(uptime_in_minutes) >= 1440:
                uptime_in_days = str(float(uptime_in_minutes)/1440).split('.')[0]
                uptime = '{} Day(s)'.format(uptime_in_days)
            embed = discord.Embed(title="{}".format("Server Count"),
                                  description="We are in **{}** servers\nWe have **{}** members\nWe had a total of **{}** users\nThere are **{}** users online\nUptime: `{}`".format(
                                      str(len(self.bot.servers)), str(len(set(self.bot.get_all_members()))), self.total_users, sum(1 for m in set(ctx.bot.get_all_members()) if m.status != discord.Status.offline), uptime),
                                  url='https://discordapp.com/oauth2/authorize?client_id=397149515192205324&permissions=1261448256&scope=bot',
                                  color=0xf20006)
            embed.set_thumbnail(url='https://raw.githubusercontent.com/Annihilator708/DiscordBot-BotZilla/master/icon.png')
            a = await self.bot.say(embed=embed)
            self.total_online_users = 0
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        else:
            embed = discord.Embed(title="{}".format("Server Count"),
                                  description="We are in **{}** servers\nWe have **{}** members\nThere are **{}** users online".format(
                                      str(len(self.bot.servers)), str(len(set(self.bot.get_all_members()))), sum(1 for m in set(ctx.bot.get_all_members()) if m.status != discord.Status.offline)),
                                  url='https://discordapp.com/oauth2/authorize?client_id=397149515192205324&permissions=1261448256&scope=bot',
                                  color=0xf20006)
            embed.set_thumbnail(url='https://raw.githubusercontent.com/Annihilator708/DiscordBot-BotZilla/master/icon.png')
            a = await self.bot.say(embed=embed)
            self.total_online_users = 0
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def swcount(self, ctx):
        """
        Count total swearwords used in servers where BotZilla is in
        """
        if self.database_file_found:
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'shit';")
            shit = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'fuck';")
            fuck = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'damn';")
            damn = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'bitch';")
            bitch = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'crap';")
            crap = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'pussy';")
            pussy = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'asshole';")
            asshole = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'fag';")
            fag = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'gay';")
            gay = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select extract(epoch from current_timestamp - pg_postmaster_start_time()) as uptime;")
            uptime = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            uptime = str(uptime).replace('[(', '').replace(',)]', '')
            uptime_in_minutes = str(float(uptime)/60).split('.')[0]
            uptime = '{} Minute(s)'.format(uptime_in_minutes)
            if int(uptime_in_minutes) >= 60:
                uptime_in_hours = str(float(uptime_in_minutes)/60).split('.')[0]
                uptime = '{} Hour(s)'.format(uptime_in_hours)
            if int(uptime_in_minutes) >= 1440:
                uptime_in_days = str(float(uptime_in_minutes)/1440).split('.')[0]
                uptime = '{} Day(s)'.format(uptime_in_days)

            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='The following swearwords are registered.\nBotZilla shows the total uses of a swearword since database is up.\nDatabase is up for:\n```{}```'.format(uptime),
                                  colour=0xf20006)
            embed.add_field(name='Shit', value=str(shit).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Fuck', value=str(fuck).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Damn', value=str(damn).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Bitch', value=str(bitch).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Crap', value=str(crap).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Pussy', value=str(pussy).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Asshole', value=str(asshole).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Fag', value=str(fag).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Gay', value=str(gay).replace('[(', '**').replace(',)]', '**'))

            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def id(self, ctx, *, username=None):
        """Shows your ID or the id of the user."""
        if username is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Your ID is:\n**{}**'.format(str(ctx.message.author.id)),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        else:
            try:
                username = username.replace('<@', '')
                username = username.replace('>', '')
                username = username.replace('!', '')
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='The ID you looking for is:\n**{}**'.format(str(username)),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            except:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Invalid username'.format(str(username)),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])


    @commands.command(pass_context=True, hidden=True)
    async def say(self, ctx, *, message=None):
        """Say something as BotZilla.
        This only works in the direct channel the command is used in.
        Secret egg ;)
        """

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


    @commands.command(pass_context=True)
    async def emoji(self, ctx, *, emoji : str =None):
        """
        Shows ASCII information about the emoji.
        Usefull for developers.
        """
        if emoji is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Try `{}help emoji`, That would help..'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        try:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='```asci\n{}\n```'.format(ascii(str(emoji))),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='```Python\n{}\n```'.format(e.args),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


    @commands.command(pass_context=True)
    async def blacklist(self, ctx, username=None, *, reason: str = None):
        """
        Starts a blacklist vote. Ban people from making use of BotZilla.
        5 % of your server has to agree.
        """
        if username is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Read **`{}help blacklist`** that would help..'.format(
                                      self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        elif reason is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You have to give up a reason..\nI recommend reading **`{}help blacklist`**'.format(
                                      self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        else:
            vote_policy = len(ctx.message.server.members) / 100 * 5
            username = username.replace('<@', '')
            username = username.replace('>', '')
            username = username.replace('!', '')

            try:
                name = await self.bot.get_user_info(username)
                if name.id in self.database.blacklist:
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='*`{}` already on the blacklist*'.format(name),
                                          colour=0xf20006)
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, '\U0001f605')
                    return
            except:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Invalid username'.format(str(username)),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return


            embed = discord.Embed(title='Blacklist vote started by {}:'.format(ctx.message.author.name),
                                  description='Total votes are needed: **{}**\n**2** Minutes remaining..\n\nWould you like to blacklist:\n\n**`{}`**\n\nReason:\n\n**`{}`**\n\nPeople who got blacklisted can\'t use BotZilla anymore.\nEven in other servers'.format(
                                      vote_policy, name, str(reason)),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\u2705')
            await self.bot.add_reaction(a, '\U0001f1fd')
            await asyncio.sleep(120)

            message = await self.bot.get_message(ctx.message.channel, a.id)
            total_yes = message.reactions[0].count - 1
            total_no = message.reactions[1].count - 1
            total = total_yes + total_no
            yes_needed = vote_policy // 2

            if float(total) >= vote_policy:
                if float(total_yes) >= yes_needed:
                    try:
                        reason = str(reason).replace(';', '')
                        self.database.cur.execute("INSERT INTO botzilla.blacklist (ID, server_name, reason, total_votes) VALUES ({}, '{}', '{}', {});".format(name.id, str(name), str(reason), total))
                        self.database.cur.execute("ROLLBACK;")
                        print(f'Vote blacklist approved for {username}')
                        await self.bot.delete_message(message)
                    except:
                        await self.bot.delete_message(message)
                        pass
                    finally:
                        embed = discord.Embed(title='Blacklist vote approved:',
                                              description='Blacklist vote has been approved for **`{}`**'.format(name),
                                              colour=0xf20006)
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, '\U0001f44b')
                        await self.bot.delete_message(message)
            else:
                embed = discord.Embed(title='Blacklist vote started by {}:'.format(ctx.message.author.name),
                                      description='Blacklist vote has been declined for **`{}`**'.format(name),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, '\u2705')
                await self.bot.delete_message(message)


    @commands.command(pass_context=True)
    async def report(self, ctx, *, Message: str = None):
        """
        Report any issue to the bot owner
        Did you find any bugs. Something that annoys you.
        Report it with this command please.
        This way needed changes could be made.
        You risk a place on the global blacklist if you use this command
        for spam or other exploits.
        """
        if Message is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='please read **`{}help report`** first..'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Report send.. Misbehavior may be punished!',
                              colour=0xf20006)
        report_send = await self.bot.say(embed=embed)
        await self.bot.add_reaction(report_send, self.emojiUnicode['succes'])

        embed = discord.Embed(title='USER REPORT {} | {}:'.format(ctx.message.author.name, ctx.message.author.id),
                              description='Server:\n**{}**\n*{}*\n\nChannel:\n**{}**\n*{}*\n\nMessage:\n```{}```'.format(
                                  ctx.message.server, ctx.message.server.id, ctx.message.channel, ctx.message.channel.id, Message),
                              colour=0xf20006)
        for owner in self.config['owner-id']:
            owner = await self.bot.get_user_info(owner)
            message = await self.bot.send_message(owner, embed=embed)
            await self.bot.add_reaction(message, self.emojiUnicode['succes'])
            await self.bot.add_reaction(message, '\u2620')
            await asyncio.sleep(5)
            emoji = await self.bot.wait_for_reaction([self.emojiUnicode['succes'], '\u2620'], message=message)

            if emoji.reaction.emoji == self.emojiUnicode['succes']:
                user_who_send_report = await self.bot.get_user_info(ctx.message.author.id)
                embed = discord.Embed(
                    title='Your report, {}:'.format(ctx.message.author.name),
                    description='You have been noticed, Your report has been seen\n\n**Report:**\n```{}```'.format(Message),
                    colour=0xf20006)
                a = await self.bot.send_message(user_who_send_report, embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                await self.bot.delete_message(message)
                await self.bot.send_message(owner, 'Report removed')
                return


            if emoji.reaction.emoji == '\u2620':
                self.database.cur.execute(
                    "INSERT INTO botzilla.blacklist (ID, server_name, reason, total_votes) VALUES ({}, '{}', '{}', {});".format(
                        ctx.message.author.id, str(ctx.message.author.name), 'Misbehaviour Report Command', 10000))
                self.database.cur.execute("ROLLBACK;")
                await self.bot.delete_message(message)
                user_who_got_blacklisted = await self.bot.get_user_info(ctx.message.author.id)
                embed = discord.Embed(
                    title='Warning {}:'.format(ctx.message.author.name),
                    description='You are on the global blacklist, Reason:\n```Misbehavior Report Command```',
                    colour=0xf20006)
                a = await self.bot.send_message(user_who_got_blacklisted, embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                await self.bot.send_message(owner, 'User {} | {} added to blacklist'.format(ctx.message.author.name, ctx.message.author.id))


    @commands.command(pass_context=True)
    async def location(self, ctx, *, keywords:str = None):
        """
        Get more information about a location.
        Supported: Zipcode, City, Country, street, latitude, longitude
        """

        if keywords is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Maybe you should look in `{}help location`. Its a secret spot :wink:'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])

        if keywords.lower() == 'area51':
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':alien:\n:shirt::shield:\n:jeans:',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\U0001f47d')
        else:
            old_keyword = "".join(keywords)
            try:
                keywords = str(keywords).replace(' ', '%20')
                url = 'http://nominatim.openstreetmap.org/?format=json&addressdetails=1&q={}&format=json&limit=1'.format(keywords)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        source = await response.json(encoding='utf8')

                source = json.dumps(source, indent=2)
                result = json.loads(source)

                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Your search tag was:\n***{}***\n\n**Tags**\n```\n{}\n```'.format(old_keyword, result[0]['display_name']),
                                      colour=0xf20006)
                embed.add_field(name='Location:', value='City: **`{}`**\nState: **`{}`**\nCountry: **`{}`**\nCountry Code: **`{}`**\nNeighbourhood: **`{}`**\nRoad: **`{}`**\nPostcode: **`{}`**\n```\n```'.format(
                    result[0]['address']['city'], result[0]['address']['state'], result[0]['address']['country'], result[0]['address']['country_code'], result[0]['address']['neighbourhood'],
                    result[0]['address']['road'], result[0]['address']['postcode']))
                embed.add_field(name='Latitude:', value=result[0]['lat'], inline=True)
                embed.add_field(name='Longitude:', value=result[0]['lon'], inline=True)
                embed.set_footer(text=result[0]['licence'])
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])

            except Exception as e:
                try:
                    keywords = str(keywords).replace(' ', '%20')
                    url = 'http://nominatim.openstreetmap.org/?format=json&addressdetails=1&q={}&format=json&limit=1'.format(keywords)
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            source = await response.json(encoding='utf8')

                    source = json.dumps(source, indent=2)
                    result = json.loads(source)

                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='Your search tag was:\n***{}***\n\n**Tags**\n```\n{}\n```'.format(
                                              old_keyword, result[0]['display_name']),
                                          colour=0xf20006)
                    embed.add_field(name='Location:',
                                    value='City: **`{}`**\nState: **`{}`**\nCountry: **`{}`**\nCountry Code: **`{}`**'.format(
                                        result[0]['address']['city'], result[0]['address']['state'],
                                        result[0]['address']['country'], result[0]['address']['country_code']))
                    embed.add_field(name='Latitude:', value=result[0]['lat'], inline=True)
                    embed.add_field(name='Longitude:', value=result[0]['lon'], inline=True)
                    embed.set_footer(text=result[0]['licence'])
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['succes'])

                except Exception as e:
                    try:
                        keywords = str(keywords).replace(' ', '%20')
                        url = 'http://nominatim.openstreetmap.org/?format=json&addressdetails=1&q={}&format=json&limit=1'.format(
                            keywords)
                        async with aiohttp.ClientSession() as session:
                            async with session.get(url) as response:
                                source = await response.json(encoding='utf8')

                        source = json.dumps(source, indent=2)
                        result = json.loads(source)

                        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                              description='Your search tag was:\n***{}***\n\n**Tags**\n```\n{}\n```'.format(
                                                  old_keyword, result[0]['display_name']),
                                              colour=0xf20006)
                        embed.add_field(name='Location:',
                                        value='State: **`{}`**\nCountry: **`{}`**\nCountry Code: **`{}`**'.format(
                                            result[0]['address']['state'], result[0]['address']['country'],
                                            result[0]['address']['country_code']))
                        embed.add_field(name='Latitude:', value=result[0]['lat'], inline=True)
                        embed.add_field(name='Longitude:', value=result[0]['lon'], inline=True)
                        embed.set_footer(text=result[0]['licence'])
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                    except Exception as e:
                        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                              description='Your search tag was:\n***{}***\nNothing found :map:'.format(
                                                  old_keyword, self.config['prefix']),
                                              colour=0xf20006)
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, self.emojiUnicode['warning'])


def setup(bot):
    bot.add_cog(Information(bot))
