import discord
from discord.ext import commands
import json
import datetime
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
try:
    from plugin.database import Database
except Exception as e:
    pass


tmp_config = json.loads(str(open('./options/config.js').read()))
config = tmp_config['config']
owner_list = config['owner-id']


class Help:
    def __init__(self, bot):
        self.bot = bot
        bot_version = 'V0.8'
        self.version = bot_version
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']

        self.emoji_start = '\u23ee'
        self.emoji_five_back = '\u23ea'
        self.emoji_oneback = '\u25c0'
        self.emoji_oneahead = '\u25b6'
        self.emoji_five_ahead = '\u23e9'
        self.emoji_end = '\u23ed'
        self.emoji_start_txt = '⏮'
        self.emoji_five_back_txt = '⏪'
        self.emoji_oneback_txt = '◀'
        self.emoji_oneahead_txt = '▶'
        self.emoji_five_ahead_txt = '⏩'
        self.emoji_end_txt = '⏭'

        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except Exception as e:
            print('Help: Database files not found - {}'.format(e.args))
            pass

    @commands.command(pass_context=True)
    async def help(self, ctx, command: str = None):
        """
        Show this message
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!help <{command}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        self.message = ctx.message

        def get_command_by_name():
            self.database.cur.execute("select * from botzilla.help;")
            command_object = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            command_names = [i[0] for i in command_object]
            return command_names

        def get_commands_by_cog(cog_name):
            self.database.cur.execute("select * from botzilla.help where cog = '{}';".format(cog_name))
            command_object = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            return command_object

        def get_short_desc(command_object):
            command_desc = command_object[2]
            split_lines = command_desc.splitlines(keepends=True)
            list_desc = [i.strip() for i in split_lines if i != '\n']
            try:
                short_desc = f'{list_desc[0]}\n{list_desc[1]}'
            except Exception as e:
                short_desc = list_desc[0]
            return short_desc

        async def wait_for_reaction(message):
            while True:
                reaction = await self.bot.wait_for_reaction([self.emoji_start, self.emoji_five_back, self.emoji_oneback, self.emoji_oneahead, self.emoji_five_ahead, self.emoji_end], message=message, timeout=120)
                if ctx.message.author.id == reaction.user.id:
                    try:
                        await self.bot.remove_reaction(emoji=reaction.reaction.emoji, member=ctx.message.author, message=message)
                    except Exception as e:
                        print(e.args)
                    break
                else:
                    try:
                        await self.bot.remove_reaction(emoji=reaction.reaction.emoji, member=reaction.user, message=message)
                    except Exception as e:
                        print(e.args)
            return reaction

        def create_new_page(cog:str):
            # print('New_page Function')
            data = get_commands_by_cog(cog)
            data = sorted(data)
            pages = []
            new_page = discord.Embed(title=f'Help for {ctx.message.author.display_name}',
                                     description=f'**Category:** ***`{cog}`***',
                                     colour=0xf20006)
            for item in data:
                new_page.add_field(name=f"-- {self.config['prefix']}{item[0]}\n\n",
                                value=f'***`{get_short_desc(item)}`***\n**Name:** ***`{item[0]}`***',
                                inline=False)
                pages.append(new_page)
            # print('DONE New_page Function')
            return pages

        def generate_pages():
            # print('generate_pages Function')
            all = []
            # print('all')
            all.append(create_new_page('Games'))
            # print('Games DONE')
            all.append(create_new_page('GameStats'))
            # print('GameStats DONE')
            all.append(create_new_page('Fun'))
            # print('Fun DONE')
            all.append(create_new_page('Music'))
             #print('Music DONE')
            all.append(create_new_page('Utils'))
            # print('Utils DONE')
            all.append(create_new_page('Images'))
            # print('Images DONE')
            all.append(create_new_page('Exchange'))
            # print('Exchange DONE')

            paginator = {}
            page_number = 0
            for item in all:
                page_number += 1
                paginator[str(page_number)] = item
            # print('DONE generate_pages Function')
            return paginator

        #test

        if command is None:
            # print('Function loaded in')

            # Pages
            page0 = discord.Embed(title=f'Help for: {ctx.message.author.display_name}',
                                  description='If you are stuck this console is for you.\nNavigate around with the **`emoji\'s`** underneath.\n\n`{0}`: First page\n`{1}`: Five pages back\n`{2}`: One page back\n`{3}`: Next page\n`{4}`: Skip next five pages\n`{5}`: Last page\n\nIf you like to retrieve more information about a command.\nSimply add any command name behind **`{6}help`**\nFor example: Their is a command called **`battleship`**.\nIt\'s a game what you can play in discord.\nFor more information on how to play battleship use **`{6}help battleship`**\n\nIf this console is **`2`** minutes inactive it will shutdown'.format(
                                      self.emoji_start_txt, self.emoji_five_back_txt, self.emoji_oneback_txt, self.emoji_oneahead_txt, self.emoji_five_ahead_txt, self.emoji_end_txt, self.config['prefix']),
                                  colour=0xf20006)
            start = await self.bot.say(embed=page0)

            generate_pages_result = generate_pages()

            await self.bot.add_reaction(start, self.emoji_start)
            await self.bot.add_reaction(start, self.emoji_five_back) #Maybe if there are more commands
            await self.bot.add_reaction(start, self.emoji_oneback)
            await self.bot.add_reaction(start, self.emoji_oneahead)
            await self.bot.add_reaction(start, self.emoji_five_ahead) #Maybe if there are more commands
            await self.bot.add_reaction(start, self.emoji_end)

            await asyncio.sleep(0.6)

            page0.set_footer(text=f'Version: {self.version}\t|\tDev help: !!rtfm\t|\tReady...')
            await self.bot.edit_message(start, embed=page0)

            # print('Reactions added')

            # remove duplicates
            page = 0
            paginator = {}
            paginator['0'] = page0
            for key, value in generate_pages_result.items():
                paginator[key] = value[0]
                page += 1

            page_number = 1
            lenght_help = int(len(paginator.keys()) - 1)

            # print(f'QUery lenght: {lenght_help}')

            for i in range(100):
                reaction = await wait_for_reaction(start)
                if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_start):
                    if page_number >= 1 and page_number <= lenght_help:
                        page_number = 0
                        # print(page_number)

                if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_five_back):
                    if page_number >= 5 and page_number <= lenght_help:
                        page_number = page_number - 5
                        # print(page)

                if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_oneback):
                    if page_number >= 1 and page_number <= lenght_help:
                        page_number = page_number - 1
                        # print(page)

                if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_oneahead):
                    if page_number >= 0 and page_number <= lenght_help - 1:
                        page_number = page_number + 1
                        # print(page_number)

                if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_five_ahead):
                    if page_number >= 0 and page_number <= lenght_help - 5:
                        page_number = page_number + 5
                        # print(page)

                if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_end):
                    if page_number <= lenght_help:
                        page_number = lenght_help
                        # print(page_number)

                embed = paginator[str(page_number)]
                embed.set_footer(text=f'Version: {self.version}\t|\tDev help: !!rtfm\t|\tPage: {int(page_number + 1)}/{int(len(paginator.keys()))}')
                await self.bot.edit_message(start, embed=embed)

        if command != None:
            commanden = get_command_by_name()
            print(commanden)
            if str(command).lower() in commanden:
                self.database.cur.execute("select * from botzilla.help where name = '{}';".format(str(command).lower()))
                command_object = self.database.cur.fetchone()
                self.database.cur.execute("ROLLBACK;")
                desc = str(command_object[2]).replace('<insert semicolon here>', ';')
                embed = discord.Embed(title=f'Help for: {ctx.message.author.display_name}',
                                      description=f'**\nCommand:** - **`{self.config["prefix"]}{command_object[0]}`**\n**Category:** - **`{command_object[1]}`**\n\n**Description:**\n**```\n{desc}\n```**',
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            else:
                embed = discord.Embed(title=f'Help for: {ctx.message.author.display_name}',
                                      description=f'Unfortunately the command **`{self.config["prefix"]}{command}`** doesnt exist.\nAll commands can be found in **`{self.config["prefix"]}help`**',
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])

    @commands.command(pass_context=True)
    async def rtfm(self, ctx, search:str=None):
        """
        Discord.py documentation.
        Usefull for developers.

        Usage:
          - !!rtfm <Event | Object | Function>
        Example:
          - !!rtfm message
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!rtfm <{search}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        hrefs = []
        url = 'http://discordpy.readthedocs.io/en/latest/api.html'
        link_limit_rtfm = 20
        logging_help = "[logging](https://discordpy.readthedocs.io/en/latest/logging.html)"
        whats_new = "[whats_new](https://discordpy.readthedocs.io/en/latest/whats_new.html)"
        migrating = "[migrating](https://discordpy.readthedocs.io/en/latest/migrating.html)"
        api_ref = "[here](http://discordpy.readthedocs.io/en/latest/api.html#api-reference)"

        # # make bot do stuff
        await self.bot.send_typing(ctx.message.channel)
        embed = discord.Embed(title=f'Manual for {ctx.message.author.name}, RTFM!!',
                              description=f'If you miss something, please use the suggest command.\n**`{self.config["prefix"]}help report`** for more info about this command.\nUse a object to search more accurate, More info **`{self.config["prefix"]}help rtfm`**',
                              colour=0xf20006)
        if search is None:
            embed.add_field(name='Useful related links',
                            value=f'- [API Reference](http://discordpy.readthedocs.io/en/latest/api.html#api-reference)')
            embed.add_field(name=f'Additional links:',
                            value=f'{logging_help}\n{migrating}\n{whats_new}')
            none_object = await self.bot.say(embed=embed)
            await self.bot.add_reaction(none_object, self.emojiUnicode['succes'])
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.read()

        bs = BeautifulSoup(html, 'lxml')

        for link in bs.find_all('a'):
            if link.has_attr('href'):
                hrefs.append(link.attrs['href'])

        # Filter results, remove all != doc pages
        filtered_hrefs = []
        for i in hrefs:
            if str(i).startswith('#'):
                if str(i) == '#':
                    pass  ### remove index page
                else:
                    filtered_hrefs.append(i)

        # Make a dictionary out of the hrefs, add also a link to each href
        dict_hrefs = {}
        filtered_dict = {}
        for item in filtered_hrefs:
            dict_hrefs[str(item)[1:]] = str(item)[1:].split('.')  # remove '#' from tag

            # Filter the dictionary on user input

            for key, value in dict_hrefs.items():
                if search in key or search in value:
                    filtered_dict[key] = 'https://discordpy.readthedocs.io/en/latest/api.html#{}'.format(key)

        src_format = []
        # if search in filtered_dict.keys():
        # format matches
        search_matches = str(json.dumps(filtered_dict, indent=2))
        src_match_load = json.loads(search_matches)

        for key, value in src_match_load.items():
            src_format.append(f"- [{key}]({value})")

        print(search in src_match_load.keys())
        # Pretyfy
        for n in range(link_limit_rtfm):
            prety_format = '\n'.join(sorted(src_format, key=len))

        print(prety_format)

        if bool(prety_format) == False:
            print('no results found')
            embed.add_field(name=f'Useful Links:',
                            value=f'- No results found on **`{search}`**..')
            embed.add_field(name=f'Additional links:',
                            value=f'{logging_help}\n{migrating}\n{whats_new}')
            msg = await self.bot.say(embed=embed)
            embed.set_footer(text=f'discord.py')
            await self.bot.add_reaction(msg, self.emojiUnicode['succes'])
        else:
            embed.add_field(name=f'Useful Links:',
                            value=f'**{prety_format}**..\n\nMore information can be found **{api_ref}** or **[here](https://www.google.nl/search?q=discordpy%20{search})**')
            embed.add_field(name=f'Additional useful links:',
                            value=f'{logging_help}\n{migrating}\n{whats_new}')
            msg = await self.bot.say(embed=embed)
            embed.set_footer(text=f'discord.py')
            await self.bot.add_reaction(msg, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Help(bot))