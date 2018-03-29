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
import textwrap
from lxml import etree
from functools import partial
import datetime
import pytz

try:
    from plugin.database import Database
except:
    pass


def to_emoji(c):
    base = 0x1f1e6
    return chr(base + c)


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

    @commands.command(pass_context=True, aliases=["g"])
    async def google(self, ctx, *, search_term: str = None):
        """
        Make a google search.
        Retrieve the top 3 search results.

        Alias : !!g

        Usage:
          - !!google <search>
          - !!g <search>
        Example:
          - !!google what time is it now?
          - !!g what time is it now?
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!g <{search_term}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if search_term is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='try to "search" for **`{}help g`**'.format(self.config['prefix']),
                                  colour=0xf20006)
            embed.set_footer(text='Data © google contributors, google.com')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        search = search_term
        if ' ' in search:
            search = str(search).replace(' ', '%20')

        url = f'https://www.google.nl/search?q={search}'
        params = {'safe': 'on', 'lr': 'lang_en', 'hl': 'en'}
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) Gecko/20100101 Firefox/53.0'}

        # list of URLs and title tuples
        entries = []

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params, headers=headers) as response:
                if response.status != 200:
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='Google has failed to respond. :cry:',
                                          colour=0xf20006)
                    embed.set_footer(text='Data © google contributors, google.com')
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                    return
                else:
                    source = await response.read()
                    source = source.decode('utf-8')

                    root = etree.fromstring(source, etree.HTMLParser())

                    search_results = root.findall(".//div[@class='rc']")
                    for node in search_results:
                        link = node.find("./h3[@class='r']/a")
                        if link is not None:
                            entries.append((link.get('href'), link.text))

                    try:
                        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                              description=f'Search result **`1`**\n[{entries[0][1]}]({entries[0][0]})\n\nSearch result **`2`**\n[{entries[1][1]}]({entries[1][0]})\n\nSearch result **`3`**\n[{entries[2][1]}]({entries[2][0]})',
                                              colour=0xf20006)
                        embed.set_footer(text='Data © google contributors, google.com')
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                    except Exception as e:
                        try:
                            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                                  description=f'Search result **`1`**\n[{entries[0][1]}]({entries[0][0]})\n\nSearch result **`2`**\n[{entries[1][1]}]({entries[1][0]})',
                                                  colour=0xf20006)
                            embed.set_footer(text='Data © google contributors, google.com')
                            a = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                        except Exception as e:
                            try:
                                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                                      description=f'Search result **`1`**\n[{entries[0][1]}]({entries[0][0]})',
                                                      colour=0xf20006)
                                embed.set_footer(text='Data © google contributors, google.com')
                                a = await self.bot.say(embed=embed)
                                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                            except Exception as e:
                                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                                      description=f'No results found for **`{search_term}`**',
                                                      colour=0xf20006)
                                a = await self.bot.say(embed=embed)
                                await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def pokedex(self, ctx, *, pokemon=None):
        """
        Discord Pokedex.
        Show information about a specific pokemon.

        Usage:
          - !!pokedex <pokemon name>
          - !!pokedex <pokemon number>
        Example:
          - !!pokedex pikachu
          - !!pokedex 007
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!pokedex <{pokemon}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if pokemon is None:
            embed = discord.Embed(title="{}:".format(ctx.message.author.name),
                                  description="Try **`{}help pokedex`** instead".format(self.config['prefix']),
                                  color=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return
        else:
            await self.bot.send_typing(ctx.message.channel)
            try:
                url = "https://cheeze.club/api/pokedex/{}".format(pokemon)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        source = await response.json(encoding='utf8')

                source = json.dumps(source)
                data = json.loads(str(source))

                if data['name'] == 0:
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='Pokemon **`{}`** not found'.format(pokemon),
                                          colour=0xf20006)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                    return

                types = " - ".join(data["types"])

                tmp = []
                for i in data["abilities"]:
                    k = f'- {i}'
                    tmp.append(k)
                abilities = "\n".join(tmp)

                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'**Name: ** *`{data["name"]}`*\n**Number: ** *`{data["number"]}`*\n**Type(s): ** *`{types}`*\n**Species: ** *`{data["species"]}`*\n**Height: ** *`{data["height"]}`*\n**Weight: ** *`{data["weight"]}`*\n**Description:**\n*```\n{data["description"]}\n```*\n**Abilities:**\n*`{abilities}`*',
                                      colour=0xf20006)
                embed.set_thumbnail(url=data["image"])
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Pokemon **`{}`** not found'.format(pokemon),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])


    @commands.command(pass_context=True)
    async def fact(self, ctx, *, search_term: str = None):
        """
        Search for a fact!
        Use this command in combination with a subject you like
        to get a fact for that subject

        Usage:
          - !!fact <search term>
        Example:
          - !!fact cats
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!fact <{search_term}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if search_term is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You really should reconsider reading **`{}help fact`**'.format(self.config['prefix']),
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
            message2user = "**Type:**\n*`{}`*\n**Text:**\n*`{}`*\n**Source:**\n*{}*".format(related_type, related_text, related_related)
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


    @commands.command(pass_context=True, aliases=["oauth"])
    async def invite(self, ctx):
        """
        Invite BotZilla to your server!
        Gives BotZilla OAuth url. Use this to add him to your server!

        Usage:
          - !!invite
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!invite in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Use the following url to add BotZilla V2 to your guild!\n**{}**\nDon\'t forget to upvote! :)'.format(
                                  'https://discordbots.org/bot/397149515192205324'),
                              colour=0xf20006)
        embed.set_footer(text='PuffDip#5369 ©')
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """
        Sends a package to the discord server.
        Calculates response time

        Usage:
          - !!ping
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!ping in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
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
        Count the community, servers and more!

        Usage:
          - !!count
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!count in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if self.database_file_found:
            self.database.cur.execute("select count(*) from botzilla.users;")
            rows = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            a = str(rows).replace('(', '').replace('[', '')
            self.total_users = a.replace(']', '').replace(',', '').replace(')', '')
            self.database.cur.execute("select extract(epoch from current_timestamp - pg_postmaster_start_time()) as uptime;")
            uptime = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            uptime = str(uptime).replace('(', '').replace(',', '').replace('[', '').replace(')', '').replace(']', '')
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
                                  color=0xf20006)
            embed.set_thumbnail(url='https://images.discordapp.net/avatars/397149515192205324/ced0f56a29af0b9bfecdb336d04544a3.png?size=512')
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            self.total_online_users = 0
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        else:
            embed = discord.Embed(title="{}".format("Server Count"),
                                  description="We are in **{}** servers\nWe have **{}** members\nThere are **{}** users online".format(
                                      str(len(self.bot.servers)), str(len(set(self.bot.get_all_members()))), sum(1 for m in set(ctx.bot.get_all_members()) if m.status != discord.Status.offline)),
                                  color=0xf20006)
            embed.set_thumbnail(url='https://images.discordapp.net/avatars/397149515192205324/ced0f56a29af0b9bfecdb336d04544a3.png?size=512')
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            self.total_online_users = 0
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def swcount(self, ctx):
        """
        Count total swearwords used in servers where BotZilla is in.
        Counts each word individual.

        Usage:
          - !!swcount
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!swcount in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
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
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'questionmark';")
            questionmark = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'crap';")
            crap = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'pussy';")
            pussy = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute("select total from botzilla.swearwords where swearword = 'wtf';")
            wtf = self.database.cur.fetchall()
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
            uptime = str(uptime).replace('[', '').replace('(', '').replace(',', '').replace(')', '').replace(']', '')
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
            embed.add_field(name='Character [?]', value=str(questionmark).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Crap', value=str(crap).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Pussy', value=str(pussy).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='WTF', value=str(wtf).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Fag', value=str(fag).replace('[(', '**').replace(',)]', '**'))
            embed.add_field(name='Gay', value=str(gay).replace('[(', '**').replace(',)]', '**'))
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, hidden=True)
    async def say(self, ctx, *, message=None):
        """
        Say something as BotZilla.
        This only works in the direct channel the command is used in.

        Usage:
          - !!say <message>
        Example:
          - !!say Hello World!
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!say <{message}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if message is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Maybe you should considering using **`{}help say`** instead'.format(self.config['prefix']),
                                  colour=0xf20006)
            await self.bot.say(embed=embed)
        else:
            try:
                await self.bot.delete_message(ctx.message)
            except Exception as e:
                pass
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format(str(message)),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def location(self, ctx, *, keywords:str = None):
        """
        Get more information about a location.
        Supported: Zipcode, City, Country, street, latitude, longitude

        Usage:
          - !!location <supported>
        Example:
          - !!location england
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!location <{keywords}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if keywords is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Maybe you should look in **`{}help location`**. Its a secret spot :wink:'.format(self.config['prefix']),
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        if 'area51' in str(keywords).lower():
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':alien:\n:shirt::shield:\n:jeans:',
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\U0001f47d')
        else:
            old_keywords = str(keywords)
            try:
                keywords = str(keywords).replace(' ', '%20')
                url = 'http://nominatim.openstreetmap.org/?format=json&addressdetails=1&q={}&format=json&limit=1'.format(keywords)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        source = await response.json(encoding='utf8')

                source = json.dumps(source, indent=2)
                result = json.loads(source)

                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Your search tag was:\n***{}***\n\n**Tags**\n```\n{}\n```'.format(old_keywords, result[0]['display_name']),
                                      colour=0xf20006)
                embed.add_field(name='Location:', value='City: **`{}`**\nState: **`{}`**\nCountry: **`{}`**\nCountry Code: **`{}`**\nNeighbourhood: **`{}`**\nRoad: **`{}`**\nPostcode: **`{}`**'.format(
                    result[0]['address']['city'], result[0]['address']['state'], result[0]['address']['country'], result[0]['address']['country_code'], result[0]['address']['neighbourhood'],
                    result[0]['address']['road'], result[0]['address']['postcode']))
                embed.add_field(name='Latitude:', value=result[0]['lat'], inline=False)
                embed.add_field(name='Longitude:', value=result[0]['lon'], inline=False)
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
                                              old_keywords, result[0]['display_name']),
                                          colour=0xf20006)
                    embed.add_field(name='Location:',
                                    value='City: **`{}`**\nState: **`{}`**\nCountry: **`{}`**\nCountry Code: **`{}`**'.format(
                                        result[0]['address']['city'], result[0]['address']['state'],
                                        result[0]['address']['country'], result[0]['address']['country_code']))
                    embed.add_field(name='Latitude:', value=result[0]['lat'], inline=False)
                    embed.add_field(name='Longitude:', value=result[0]['lon'], inline=False)
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
                                                  old_keywords, result[0]['display_name']),
                                              colour=0xf20006)
                        embed.add_field(name='Location:',
                                        value='State: **`{}`**\nCountry: **`{}`**\nCountry Code: **`{}`**'.format(
                                            result[0]['address']['state'], result[0]['address']['country'],
                                            result[0]['address']['country_code']))
                        embed.add_field(name='Latitude:', value=result[0]['lat'], inline=False)
                        embed.add_field(name='Longitude:', value=result[0]['lon'], inline=False)
                        embed.set_footer(text=result[0]['licence'])
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                    except Exception as e:
                        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                              description='Your search tag was:\n***{}***\nNothing found :map:'.format(
                                                  old_keywords, self.config['prefix']),
                                              colour=0xf20006)
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, self.emojiUnicode['warning'])


    @commands.command(pass_context=True, aliases=["phobia"])
    async def fear(self, ctx, *, phobia:str = None):
        """
        Search for any fear, phobia
        No search for a phobia will result in a random pick

        Alias : !!phobia

        Usage:
          - !!fear
          - !!fear <fear>
          - !!phobia <fear>
        Example:
          - !!fear hippopotomonstrosesquipedaliophobia
          - !!phobia hippopotomonstrosesquipedaliophobia

        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!fear <{phobia}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        url = 'http://ikbengeslaagd.com/API/phobia.json'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.json(encoding='utf8')

        if phobia is None:
            random_key = []
            for key in dict(source).keys():
                random_key.append(key)
            phobia_key =  random.choice(random_key)
            embed = discord.Embed(title=f'{str(phobia_key).title()}',
                                  description=f'**`{source[phobia_key]}`**',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            return

        phobia = phobia.lower()

        try:
            embed = discord.Embed(title=f'{str(phobia).title()}',
                                  description=f'**`{source[phobia]}`**',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        except Exception as e:
            embed = discord.Embed(title=f'{ctx.message.author.name}',
                                  description=f'I\'m sorry, but i could not find a phobia called:\n**`{phobia}`**',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return


    @commands.command(pass_context=True)
    async def number(self, ctx, *, number : str = None):
        """
        Shows information about a specific number.
        Some numbers may mean multiple things.

        Usage:
          - !!number <number>
        Example:
          - !!number 42
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!number <{number}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if number is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Please specify a number. Use **`{}help number`** for more info'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        else:
            try:
                try:
                    base_number = partial(int, base=0)
                    url = f'http://numbersapi.com/{base_number(number)}?json'
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            source = await response.json(encoding='utf8')

                        source = json.dumps(source)
                        data = json.loads(str(source))
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='Your number was: **`{}`**\nFound: **`{}`**\nType: **`{}`**\n```\n{}\n```'.format(
                                              data['number'], data['found'], data['type'], data['text']
                                          ),
                                          colour=0xf20006)
                    embed.set_footer(text='Data © Numbers contributors, numbersapi.com')
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['succes'])

                except Exception as e:
                    base_number = partial(int, base=0)
                    if number.startswith("0"):
                        number = number[1:]
                    url = f'http://numbersapi.com/{base_number(number)}?json'
                    async with aiohttp.ClientSession() as session:
                        async with session.get(url) as response:
                            source = await response.json(encoding='utf8')

                        source = json.dumps(source)
                        data = json.loads(str(source))
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='Your number was: **`{}`**\nFound: **`{}`**\nType: **`{}`**\n```\n{}\n```'.format(
                                              data['number'], data['found'], data['type'], data['text']
                                          ),
                                          colour=0xf20006)
                    embed.set_footer(text='Data © Numbers contributors, numbersapi.com')
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['succes'])

            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Your search number was : **`{}`**\nFound: **`False`**'.format(number),
                                      colour=0xf20006)
                embed.set_footer(text='Data © Numbers contributors, numbersapi.com')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])


class Utils:
    """
    Util commands for BotZilla.
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

    @commands.command(pass_context=True, aliases=["clock"])
    async def worldclock(self, ctx):
        """
        Get a list of the global times.
        This is a list based on GMT time.

        Alias: !!clock

        Usage:
          - !!worldclock
          - !!clock
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!worldclock in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        await self.bot.send_typing(ctx.message.channel)
        zones = pytz.all_timezones
        timezone_list = {}
        for zone in zones:
            zone = zone.split('/')
            if len(zone) >= 3:
                pass
            else:
                if 'etc' in str(zone).lower():
                    country = pytz.timezone(f'{zone[0]}/{zone[1]}')
                    current_time = datetime.datetime.now(country)
                    strf_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
                    timezone_list[zone[1]] = strf_time

        GMT_Plus = {}
        GMT_Min = {}
        GMT_Rest = {}
        for key, value in timezone_list.items():
            if '+' in key:
                GMT_Plus[key] = value
            elif '-' in key:
                GMT_Min[key] = value
            else:
                GMT_Rest[key] = value

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description=f'Overall Timezone:\n\n{GMT_Rest["Greenwich"]} - **`Greenwich`**\n{GMT_Rest["Universal"]} - **`Universal`**\n{GMT_Rest["Zulu"]} - **`Zulu`**\n\n**`Overview of all timezones:`**',
                              color=0xf20006)
        embed.add_field(name='**`UTC +`**',
                        value=f'`{GMT_Min["GMT-0"]}` - **GMT** **`+0`**\n`{GMT_Min["GMT-1"]}` - **GMT** **`+1`**\n`{GMT_Min["GMT-2"]}` - **GMT** **`+2`**\n`{GMT_Min["GMT-3"]}` - **GMT** **`+3`**\n`{GMT_Min["GMT-4"]}` - **GMT** **`+4`**\n`{GMT_Min["GMT-5"]}` - **GMT** **`+5`**\n`{GMT_Min["GMT-6"]}` - **GMT** **`+6`**\n`{GMT_Min["GMT-7"]}` - **GMT** **`+7`**\n`{GMT_Min["GMT-8"]}` - **GMT** **`+8`**\n`{GMT_Min["GMT-9"]}` - **GMT** **`+9`**\n`{GMT_Min["GMT-10"]}` - **GMT** **`+10`**\n`{GMT_Min["GMT-11"]}` - **GMT** **`+11`**\n`{GMT_Min["GMT-12"]}` - **GMT** **`+12`**\n`{GMT_Min["GMT-13"]}` - **GMT** **`+13`**\n`{GMT_Min["GMT-14"]}` - **GMT** **`+14`**',
                        inline=True)
        embed.add_field(name='**`UTC -`**',
                        value=f'`{GMT_Plus["GMT+0"]}` - **GMT** **`-0`**\n`{GMT_Plus["GMT+1"]}` - **GMT** **`-1`**\n`{GMT_Plus["GMT+2"]}` - **GMT** **`-2`**\n`{GMT_Plus["GMT+3"]}` - **GMT** **`-3`**\n`{GMT_Plus["GMT+4"]}` - **GMT** **`-4`**\n`{GMT_Plus["GMT+5"]}` - **GMT** **`-5`**\n`{GMT_Plus["GMT+6"]}` - **GMT** **`-6`**\n`{GMT_Plus["GMT+7"]}` - **GMT** **`-7`**\n`{GMT_Plus["GMT+8"]}` - **GMT** **`-8`**\n`{GMT_Plus["GMT+9"]}` - **GMT** **`-9`**\n`{GMT_Plus["GMT+10"]}` - **GMT** **`-10`**\n`{GMT_Plus["GMT+11"]}` - **GMT** **`-11`**\n`{GMT_Plus["GMT+12"]}` - **GMT** **`-12`**',
                        inline=True)

        embed.set_thumbnail(url='https://media.discordapp.net/attachments/407238426417430539/417703639658921994/clock-png-clock-png-image-1478.png')
        embed.set_image(url='https://media.discordapp.net/attachments/407238426417430539/417703230680727552/Standard_World_Time_Zones.png?width=1276&height=677')
        embed.set_footer(text=f'Server time : {datetime.date.today()} {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def profile(self, ctx):
        """
        Generate random user information.
        The information provided is all fake.
        This could be used to make a user profiles for role play goals.

        Usage:
          - !!profile
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!profile in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        try:
            url = 'https://randomuser.me/api/'
            await self.bot.send_typing(ctx.message.channel)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    data = await response.json(encoding='utf8')

            embed = discord.Embed(title='{}:'.format(ctx.message.author.name), description='The following information is **fake**', colour=0xf20006)
            embed.add_field(name='Name:', value='Name: {} {} {}\nGender: {}'.format(str(data['results'][0]['name']['title']).upper(), str(data['results'][0]['name']['first']).title(), str(data['results'][0]['name']['last']).title(), str(data['results'][0]['gender']).title()), inline=False)
            embed.add_field(name='Location:', value='{}\n{}\n{}\n{}'.format(str(data['results'][0]['location']['street']).title(), str(data['results'][0]['location']['city']).title(), str(data['results'][0]['location']['state']).title(), data['results'][0]['location']['postcode']), inline=False)
            embed.add_field(name='Online:', value='Email: {}\nUsername: {}\nPassword: {}'.format(data['results'][0]['email'], data['results'][0]['login']['username'], data['results'][0]['login']['password']), inline=False)
            embed.add_field(name='Misc:',   value='Phone: {}\nCellPhone: {}'.format(data['results'][0]['phone'], data['results'][0]['cell']), inline=False)
            embed.set_thumbnail(url=data['results'][0]['picture']['large'])
            embed.set_footer(text='Data © randomuser contributors, randomuser.me')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name), description='Could not generate a user profile', colour=0xf20006)
            embed.set_footer(text='Data © randomuser contributors, randomuser.me')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


    @commands.command(pass_context=True)
    async def perm(self, ctx, *, username=None):
        """
        Check permissions of any user in the server
        Leave blank to check your own permissions

        Usage:
          - !!perm
          - !!perm <member.mention>
        Example:
          - !!perm @puffdip
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!perm <{username}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if username is None:
            member = discord.utils.find(lambda m: m.name == ctx.message.author.name, ctx.message.server.members)
            per = member.server_permissions
            permissions = []
            for i in per:
                if 'True' in str(i):
                    i = str(i).replace(', True', '')
                    i = ':white_check_mark: : {}'.format(i)
                if 'False' in str(i):
                    i = str(i).replace(', False', '')
                    i = ':x: : {}'.format(i)
                permissions.append(str(i))
            perml = "\n".join(permissions)
            perm_pretty = perml.replace('(', '').replace(')', '').replace("'", "**")
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='The following permissions are valid for\n\n`{}`\n\n{}'.format(
                                      ctx.message.author.name, perm_pretty),
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        else:
            try:
                username = username.replace('<@', '')
                username = username.replace('>', '')
                username = username.replace('!', '')
                user = await self.bot.get_user_info(username)
                member = discord.utils.find(lambda m: m.name == user.name, ctx.message.server.members)
                per = member.server_permissions
                permissions = []
                for i in per:
                    if 'True' in str(i):
                        i = str(i).replace(', True', '')
                        i = ':white_check_mark: : {}'.format(i)
                    if 'False' in str(i):
                        i = str(i).replace(', False', '')
                        i = ':x: : {}'.format(i)
                    permissions.append(str(i))
                perml = "\n".join(permissions)
                perm_pretty = perml.replace('(', '').replace(')', '').replace("'", "**")

                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='The following permissions are valid for\n\n`{}`\n\n{}'.format(
                                          user.name, perm_pretty),
                                      colour=0xf20006)
                embed.set_footer(text='PuffDip#5369 ©')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            except:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Invalid username',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])


    @commands.command(pass_context=True)
    async def poll(self, ctx, timer = None, *questions_and_choices: str):
        """
        Makes a poll for your server.
        Choose your time, your question and your answers.

        Usage:
          - !!poll <seconds> <question> ? <Answer A> ; <Answer B> ..

        Example:
          - !!poll 300 are you male or female? Male ; Female ; other

        You can only have up to 20 choices and one question.
        Use ; and ? as a delimiter.
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!poll <{questions_and_choices}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if timer is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='It\'s not a bad idea to read **`{}help poll`** first'.format(self.config['prefix']),
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        else:
            try:
                timer = int(timer)
                if timer >= 31556926:
                    moment = 'year[s]'
                    timer_layout = (timer // 31556926)
                elif timer >= 2629743 and timer <= 31556925:
                    moment = 'month[s]'
                    timer_layout = (timer // 2629743)
                elif timer >= 86400 and timer <= 2629742:
                    moment = 'day[s]'
                    timer_layout = (timer // 86400)
                elif timer >= 3600 and timer <= 86399:
                    moment = 'hour[s]'
                    timer_layout = (timer // 3600)
                elif timer >= 60 and timer <= 3599:
                    moment = 'minute[s]'
                    timer_layout = (timer//60)
                else:
                    moment = 'seconds[s]'
                    timer_layout = timer
                print(timer_layout, moment)
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='It\'s not a bad idea to read **`{}help poll`** first'.format(
                                          self.config['prefix']),
                                      colour=0xf20006)
                embed.set_footer(text='PuffDip#5369 ©')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return

        if str(questions_and_choices) == '()':
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='It\'s not a bad idea to read **`{}help poll`** first'.format(self.config['prefix']),
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
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
                                      description='You need at least two answers',
                                      colour=0xf20006)
                embed.set_footer(text='PuffDip#5369 ©')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return
            elif len(answers) > 21:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='You have more than 20 answers',
                                      colour=0xf20006)
                embed.set_footer(text='PuffDip#5369 ©')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                return

            choices = [(to_emoji(e), v) for e, v in enumerate(answers)]

            try:
                await ctx.message.delete()
            except:
                pass
            embed = discord.Embed(title='{}\'s question'.format(ctx.message.author.name),
                                  description='This poll will end in *`{} {}`*\n\n**{}** asks:\n*```\n{}\n```*'.format(
                                      timer_layout, moment, ctx.message.author.name, question),
                                  colour=0xf20006)
            answerpoll = {}
            for key, c in choices:
                embed.add_field(name='{} Answer:'.format(':gear:'), value='{} : {}\n'.format(key, c), inline=False)
                answerpoll[key] = c
            embed.set_footer(text='PuffDip#5369 ©')
            POLL = await self.bot.say(embed=embed)

            for emoji, _ in choices:
                await self.bot.add_reaction(POLL, emoji)

            # Try to pin the message
            try:
                await self.bot.pin_message(POLL)
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='To get rid of this warning, please provide Bot2illa `Manage Messages Permissions`, Error:\n```py\n{}\n```\nPoll continues..'.format(
                                          e.args),
                                      colour=0xf20006)
                embed.set_footer(text='PuffDip#5369 ©')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])

            #Sleep for 30 min
            await asyncio.sleep(int(timer)) # 1800 30 min

            try:
                message = await self.bot.get_message(ctx.message.channel, POLL.id)
                requester = await self.bot.get_user_info(ctx.message.author.id)
                answers_user = {}
                answer_count = []
                for reaction in message.reactions:
                    answers_user[reaction.count] = reaction.emoji
                    answer_count.append(reaction.count)

                winner = max(answers_user.keys())
                await self.bot.delete_message(message)
                embed = discord.Embed(title='Results of poll:', description=f"Poll started by : **`{ctx.message.author.name}`**\nID number : **`{ctx.message.author.id}`**\nQuestion was :\n**```\n{question}\n```**",
                                      colour=0xf20006)
                await self.bot.send_message(requester, embed=embed)
                embed.set_footer(text='Next page in 10 seconds')
                b = await self.bot.say(embed=embed)
                await self.bot.add_reaction(b, self.emojiUnicode['succes'])

                # send poll results to requester
                embed = discord.Embed(title='Results of poll:', description='\t', colour=0xf20006)
                votes_from_users = 0
                for key, value in answerpoll.items():
                    embed.add_field(name=':gear: Answer:', value='{} : **`{}`**\nVotes: **`{}`**'.format(str(key).upper(), str(value), str(answer_count[votes_from_users])), inline=False)
                    votes_from_users += 1
                embed.add_field(name='----', value='The server choose answer : **{}**'.format(str(answers_user[winner]).upper()))
                embed.set_footer(text='End date {} {}'.format(datetime.datetime.today(), datetime.datetime.now()))
                result_message = await self.bot.send_message(requester, embed=embed)
                await self.bot.add_reaction(result_message, self.emojiUnicode['succes'])
                # check for loop #round
                round = 0
                b = await self.bot.get_message(ctx.message.channel, b.id)
                for i in range(10-1):
                    await asyncio.sleep(10)
                    # so the loop ends at the right position
                    round += 1
                    if round == 8:
                        embed = discord.Embed(title='Results of poll:',
                                              description='\t',
                                              colour=0xf20006)
                        votes_from_users = 0
                        for key, value in answerpoll.items():
                            embed.add_field(name=':gear: Answer:', value='{} : **`{}`**\nVotes: **{}**'.format(str(key).upper(), str(value), str(answer_count[votes_from_users])), inline=False)
                            votes_from_users += 1
                        embed.add_field(name='----', value='The server choose answer : **{}**'.format(str(answers_user[winner]).upper()))
                        embed.set_footer(text='End date {} {}'.format(datetime.datetime.today(), datetime.datetime.now()))
                        await self.bot.edit_message(b, embed=embed)
                        await self.bot.add_reaction(b, self.emojiUnicode['succes'])
                        break
                    else:
                        embed = discord.Embed(title='Results of poll:',
                                              description='\t',
                                              colour=0xf20006)
                        votes_from_users = 0
                        for key, value in answerpoll.items():
                            embed.add_field(name=':gear: Answer:', value='{} : **`{}`**\nVotes: **{}**'.format(str(key).upper(), str(value), str(answer_count[votes_from_users])), inline=False)
                            votes_from_users += 1
                        embed.add_field(name='----', value='The server choose answer : **{}**'.format(str(answers_user[winner]).upper()))
                        embed.set_footer(text='Next page in 10 seconds')
                        await self.bot.edit_message(b, embed=embed)
                        await self.bot.add_reaction(b, self.emojiUnicode['succes'])

                    await asyncio.sleep(10)
                    embed = discord.Embed(title='Results of poll:',
                                          description=f"Poll started by : **`{ctx.message.author.name}`**\nID number : **`{ctx.message.author.id}`**\nQuestion was :\n**```\n{question}\n```**",
                                          colour=0xf20006)
                    embed.set_footer(text='Next page in 10 seconds')
                    await self.bot.edit_message(b, embed=embed)
                    await self.bot.add_reaction(b, self.emojiUnicode['succes'])

            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Could not calculate total votes, Error:\n```py\n{}\n```'.format(
                                          e.args),
                                      colour=0xf20006)
                embed.set_footer(text='PuffDip#5369 ©')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])

        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Don\'t forget the question..\nQuestion: did you read the **`{}help poll`**?'.format(self.config['prefix']),
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


    @commands.command(pass_context=True)
    async def blacklist(self, ctx, username:discord.Member=None, *, reason: str = None):
        """
        Starts a blacklist vote.
        Ban people from making use of BotZilla.
        5 votes are needed.

        Usage:
          - !!blacklist <member.mention | username | ID> <reason>
        Example:
          - !!blacklist PuffDip Spamming server
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!blacklist <{username}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if username is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Read **`{}help blacklist`** that would help..'.format(
                                      self.config['prefix']),
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        elif reason is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You have to give up a reason..\nI recommend reading **`{}help blacklist`**'.format(
                                      self.config['prefix']),
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        else:
            try:
                name = await self.bot.get_user_info(username.id)
                if name.id in self.database.blacklist:
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='*`{}` already on the blacklist*'.format(name),
                                          colour=0xf20006)
                    embed.set_footer(text='PuffDip#5369 ©')
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, '\U0001f605')
                    return
            except:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Invalid username'.format(str(username)),
                                      colour=0xf20006)
                embed.set_footer(text='PuffDip#5369 ©')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return


            embed = discord.Embed(title='Blacklist vote started by {}:'.format(ctx.message.author.name),
                                  description='**`2`** Minutes remaining..\n\nWould you like to blacklist:\n\n**`{}`**\n\nReason:\n\n**`{}`**\n\nPeople who got blacklisted can\'t use BotZilla anymore.\nEven in other servers'.format(
                                      name, str(reason)),
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\u2705')
            await self.bot.add_reaction(a, '\U0001f1fd')
            await asyncio.sleep(120)

            message = await self.bot.get_message(ctx.message.channel, a.id)
            total_yes = message.reactions[0].count - 1
            total_no = message.reactions[1].count - 1
            total = total_yes + total_no
            yes_needed = 5

            if float(total) >= yes_needed:
                if float(total_yes) >= yes_needed:
                    try:
                        reason = str(reason).replace(';', '')
                        self.database.cur.execute("INSERT INTO botzilla.blacklist (ID, server_name, reason, total_votes) VALUES ({}, '{}', '{}', {});".format(username.id, username.name, str(reason), total))
                        self.database.cur.execute("ROLLBACK;")
                        print(f'Vote blacklist approved for {username}')
                        await self.bot.delete_message(message)
                    except:
                        await self.bot.delete_message(message)
                        pass
                    finally:
                        embed = discord.Embed(title='Blacklist vote approved:',
                                              description='Blacklist vote has been approved for **`{}`**'.format(username.name),
                                              colour=0xf20006)
                        embed.set_footer(text='PuffDip#5369 ©')
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, '\U0001f44b')
                        await self.bot.delete_message(message)
            else:
                embed = discord.Embed(title='Blacklist vote started by {}:'.format(ctx.message.author.name),
                                      description='Blacklist vote has been declined for **`{}`**'.format(username.name),
                                      colour=0xf20006)
                embed.set_footer(text='PuffDip#5369 ©')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, '\u2705')
                await self.bot.delete_message(message)


    @commands.command(pass_context=True, aliases=["suggestion", "sug"])
    async def report(self, ctx, *, Message: str = None):
        """
        Report any issue to the bot owner
        Suggestions and bug reports are more then welcome
        Report it with this command please.
        This way needed changes could be made.
        You risk a place on the global blacklist if you use this command
        for spam or other exploits.

        Alias : !!suggestion, !!sug

        Usage:
          - !!report <message>
          - !!suggestion <message>
          - !!sug <message>
        Example:
          - !!report bug report on command !!test
          - !!suggestion Make ... new command
          - !!sug Can you limit command X
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!report <{Message}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if Message is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='please read **`{}help report`** first..'.format(self.config['prefix']),
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Report send.. Misbehavior may be punished!',
                              colour=0xf20006)
        embed.set_footer(text='PuffDip#5369 ©')
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
    async def copy(self, ctx, number = None):
        """
        Copy messages in channel.
        Retrieve a hastebin link.

        Usage:
          - !!copy <number>
        Example:
          - !!copy 50
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!copy <{number}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if number is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Try **`{}help copy`**'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        #try:
        number = int(number)
        logs = []
        async for message in self.bot.logs_from(ctx.message.channel, limit=number):
            logs.append(message)

        data = []
        for msg in logs:
            pre = f"{msg.timestamp:%c} - {msg.author!s}{'[BOT]'*msg.author.bot}: "
            indented = textwrap.indent(msg.clean_content, ' '*len(pre)).strip()
            data.append(f"{pre}{indented}")
        data.reverse()

        await self.bot.send_typing(ctx.message.channel)

        async with aiohttp.ClientSession() as session:
            await self.bot.send_typing(ctx.message.channel)
            async with session.post("https://hastebin.com/documents", data="\n".join(data)) as response:
                if '503 Service Unavailable' in str(response):
                    embed = discord.Embed(title='{} copy request:'.format(ctx.message.author.name),
                                          description="Service unavailable, Try again later",
                                          colour=0xf20006)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                    return
                key = (await response.json(encoding='utf8'))["key"]

        embed = discord.Embed(title='{} log request:'.format(ctx.message.author.name),
                              description=f"https://hastebin.com/{key}.md",
                              colour=0xf20006)
        user = await self.bot.get_user_info(ctx.message.author.id)
        last_message = await self.bot.send_message(user, embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

        embed = discord.Embed(title='{} log request:'.format(ctx.message.author.name),
                              description='Check your private message',
                              colour=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

        for owner in self.config['owner-id']:
            embed = discord.Embed(title='{} log request:'.format(ctx.message.author.name),
                                  description=f"https://hastebin.com/{key}.md",
                                  colour=0xf20006)
            owner = await self.bot.get_user_info(owner)
            last_message = await self.bot.send_message(owner, embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

        # except Exception as e:
        #     embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
        #                           description='Try **`{}help copy`**\nError:\n```py\n{}\n```'.format(self.config['prefix'], e.args),
        #                           colour=0xf20006)
        #     a = await self.bot.say(embed=embed)
        #     await self.bot.add_reaction(a, self.emojiUnicode['error'])


    @commands.command(pass_context=True)
    async def id(self, ctx, *, username:discord.Member=None):
        """
        Shows your ID or the id of any other user.
        This can be usefull for development.

        Usage:
          - !!id
          - !!id <member.mention | ID | username>
        Example:
          - !!id @puffdip
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!id <{username}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if username is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Your ID is:\n**`{}`**'.format(str(ctx.message.author.id)),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        else:
            try:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='The ID you looking for is:\n**`{}`**'.format(username.id),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            except:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Invalid username',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])


    @commands.command(pass_context=True)
    async def emoji(self, ctx, *, emoji : str = None):
        """
        Shows ASCII information about the emoji.
        This can be usefull for development.

        Usage:
          - !!emoji <emoji>
        Example:
          - !!emoji :smiley:
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!emoji <{emoji}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if emoji is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Try **`{}help emoji`**, That would help..'.format(self.config['prefix']),
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
                                  description=f'**{type(e).__name__}:**\n```py\n{e}```',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])

    @commands.command(pass_context=True)
    async def server(self, ctx):
        """
        Shows information about this server.
        Most info is displayed here.

        Usage:
          - !!server
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!server in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        server = self.bot.get_server(f'{ctx.message.server.id}')

        embed = discord.Embed(title='{}\'s server info:'.format(ctx.message.server.name),
                              colour=0xf20006)

        embed.add_field(name=f'Information',
                        value=f'ID: **`{server.id}`**\nRegion: **`{server.region}`**\nCreated: **`{server.created_at.strftime("%Y-%m-%d %H:%M:%S")}`**\nMember Count: **`{server.member_count}`**\nCustom Emoji\'s: **`{len(server.emojis)}`**\nRoles: **`{len(server.roles)}`**\nChannels: **`{len(server.channels)}`**')

        if server.mfa_level == 0:
            mfa_level = 'False'
        else:
            mfa_level = 'True'
        if not server.unavailable:
            av = 'True'
        else:
            av = 'False'

        embed.add_field(name=f'Security',
                        value=f'Owner: **`{server.owner}`**\nVerification Level: **`{server.verification_level}`**\nMFA Level: **`{mfa_level}`**\nDefault Channel: **`{server.default_channel}`**\nAvailability: **`{av}`**\n\n**Voice**\nAFK Channel: **`{server.afk_channel}`**\nAFK Timeout: **`{server.afk_timeout//60} Minutes`**')

        invite_obj = await self.bot.invites_from(server)
        if invite_obj:
            if invite_obj[0].uses == 0:
                max_uses = 'unlimited'
            else:
                max_uses = invite_obj[0].max_uses

            embed.add_field(name=f'Invite information:',
                            value=f'Invite Link: **{invite_obj[0]}**\nUses: **`{invite_obj[0].uses}`**\nTotal Uses: **`{max_uses}`**\nTemporary: **`{invite_obj[0].temporary}`**\nInvite Creator: **`{invite_obj[0].inviter}`**\nRevoked: **`{invite_obj[0].revoked}`**')

        embed.set_thumbnail(url=server.icon_url)

        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Information(bot))
    bot.add_cog(Utils(bot))
