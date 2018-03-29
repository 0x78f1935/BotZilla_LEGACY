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
        self.emoji_number = '\U0001f522'
        self.emoji_start_txt = '⏮'
        self.emoji_five_back_txt = '⏪'
        self.emoji_oneback_txt = '◀'
        self.emoji_oneahead_txt = '▶'
        self.emoji_five_ahead_txt = '⏩'
        self.emoji_end_txt = '⏭'
        self.emoji_number_txt = '🔢'

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
                reaction = await self.bot.wait_for_reaction([self.emoji_start, self.emoji_five_back, self.emoji_oneback, self.emoji_oneahead, self.emoji_five_ahead, self.emoji_end, self.emoji_number], message=message, timeout=120)
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
                                     colour=0xf20006)
            for item in data:
                new_page.add_field(name=f"-- {self.config['prefix']}{item[0]}\n\n",
                                value=f'***`{get_short_desc(item)}`***',
                                inline=False)
                pages.append(new_page)
            # print('DONE New_page Function')
            return pages

        def generate_pages():
            # print('generate_pages Function')
            all = []
            cogs = ['Games', 'GameStats', 'Information', 'Fun', 'Music', 'Utils', 'Images', 'Exchange']

            if ctx.message.author.id in self.owner_list:
                cogs.append('AdminCommands')

            for each in sorted(cogs):
                all.append(create_new_page(each))

            print(all)

            paginator = {}
            page_number = 0
            for item in all:

                page_number += 1
                paginator[str(page_number)] = item
            # print('DONE generate_pages Function')
            print(paginator)
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
            # await self.bot.add_reaction(start, self.emoji_five_back) #Maybe if there are more commands
            await self.bot.add_reaction(start, self.emoji_oneback)
            await self.bot.add_reaction(start, self.emoji_oneahead)
            # await self.bot.add_reaction(start, self.emoji_five_ahead) #Maybe if there are more commands
            await self.bot.add_reaction(start, self.emoji_end)
            await self.bot.add_reaction(start, self.emoji_number)

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
                # wait for reaction
                reaction = await wait_for_reaction(start)

                # First page
                if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_start):
                    if page_number >= 1 and page_number <= lenght_help:
                        page_number = 0
                        # print(page_number)

                # 5 pages back
                # if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_five_back):
                #     if page_number >= 5 and page_number <= lenght_help:
                #         page_number = page_number - 5
                #         # print(page)

                # previous page
                if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_oneback):
                    if page_number >= 1 and page_number <= lenght_help:
                        page_number = page_number - 1
                        # print(page)

                # next page
                if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_oneahead):
                    if page_number >= 0 and page_number <= lenght_help - 1:
                        page_number = page_number + 1
                        # print(page_number)

                # 5 pages ahead
                # if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_five_ahead):
                #     if page_number >= 0 and page_number <= lenght_help - 5:
                #         page_number = page_number + 5
                #         # print(page)

                #last page
                if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_end):
                    if page_number <= lenght_help:
                        page_number = lenght_help
                        # print(page_number)

                # let user choose page number
                if ascii(str(reaction.reaction.emoji)) == ascii(self.emoji_number):
                    embed = discord.Embed(title=f'Help for: {ctx.message.author.display_name}',
                                          description=f'Please {ctx.message.author.name} provide a number, Between **`0`** / **`{lenght_help}`**',
                                          colour=0xf20006)
                    number__input = await self.bot.say(embed=embed)
                    msg = await self.bot.wait_for_message(author=ctx.message.author, timeout=120)
                    try:
                        page_check = int(msg.content) + 1
                        if page_check >= 0 and page_check <= lenght_help:
                            pass # Make sure user input is equal to a existing page
                        else:
                            page_number = 0
                            embed = discord.Embed(title=f'Help for: {ctx.message.author.display_name}',
                                                  description=f'Please provide a number, Between **`0`** / **`{lenght_help}`**',
                                                  colour=0xf20006)
                            await self.bot.edit_message(number__input, embed=embed)
                    except ValueError:
                        page_number = 0
                        embed = discord.Embed(title=f'Help for: {ctx.message.author.display_name}',
                                              description=f'Please provide a number, Between **`0`** / **`{lenght_help}`**',
                                              colour=0xf20006)
                        await self.bot.edit_message(number__input, embed=embed)

                    # remove excess msg
                    try:
                        await asyncio.sleep(2)
                        await self.bot.delete_message(number__input)
                        await self.bot.delete_message(msg)
                    except:
                        pass

                # Send message and looks for category, edit category to footer
                embed = paginator[str(page_number)]
                embed.set_footer(text=f'| Category: - | Version: {self.version}\t|\tDev help: !!rtfm\t|\tPage: {int(page_number + 1)}/{int(len(paginator.keys()))} |')
                new = await self.bot.edit_message(start, embed=embed)
                try:
                    content_embed = new.embeds[0]['fields'][0]['name'].split('\n', 1)[0].replace('-- !!', '')
                    self.database.cur.execute(f"select * from botzilla.help where name = '{content_embed}';")
                    catagory = self.database.cur.fetchone()
                    self.database.cur.execute(f"ROLLBACK;")
                    embed.set_footer(text=f'| Category: {catagory[1]} | Version: {self.version}\t|\tDev help: !!rtfm\t|\tPage: {int(page_number + 1)}/{int(len(paginator.keys()))} |')
                    await self.bot.edit_message(start, embed=embed)
                except Exception as e:
                    print(e.args)

        # if command give info about that command
        if command:
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
    async def updatertfm(self, ctx, search:str=None):
        """
        Update Discord.py documentation.
        Only the bot owner can use this command
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!rtfm <{search}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if ctx.message.author.id not in self.owner_list:
            return

        hrefs = []
        url = 'http://discordpy.readthedocs.io/en/latest/api.html'

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

        # save file to export
        with open('./export/rtfm.txt', 'w') as f:
            f.write(json.dumps(filtered_hrefs))

        embed = discord.Embed(title=f'RTFM!!, updated..',
                              description=f':regional_indicator_r: :regional_indicator_t: :regional_indicator_f: :regional_indicator_m:\n\nDone :thumbsup: ',
                              colour=0xf20006)
        msg = await self.bot.say(embed=embed)
        await self.bot.add_reaction(msg, self.emojiUnicode['succes'])

    @commands.command(pass_context=True)
    async def rtfm(self, ctx, search: str = None):
        """
        Discord.py documentation.
        Usefull for developers.

        Usage:
          - !!rtfm <Event | Object | Function>
        Example:
          - !!rtfm message
        """
        link_limit_rtfm = 4+1
        logging_help = "[logging](https://discordpy.readthedocs.io/en/latest/logging.html)"
        whats_new = "[whats_new](https://discordpy.readthedocs.io/en/latest/whats_new.html)"
        migrating = "[migrating](https://discordpy.readthedocs.io/en/latest/migrating.html)"
        api_ref = "[here](http://discordpy.readthedocs.io/en/latest/api.html#api-reference)"

        # # make bot do stuff
        await self.bot.send_typing(ctx.message.channel)
        embed = discord.Embed(title=f'Manual for {ctx.message.author.name}, RTFM!!',
                              description=f'Use a object to search more accurate, More info **`{self.config["prefix"]}help rtfm`**',
                              colour=0xf20006)
        if search is None:
            embed.add_field(name='Useful related links',
                            value=f'- [API Reference](http://discordpy.readthedocs.io/en/latest/api.html#api-reference)')
            embed.add_field(name=f'Additional links:',
                            value=f'{logging_help}\n{migrating}\n{whats_new}')
            none_object = await self.bot.say(embed=embed)
            await self.bot.add_reaction(none_object, self.emojiUnicode['succes'])
            return

        with open('./options/rtfm.txt', 'r') as f:
            filtered_hrefs = json.loads(f.read())

        # Make a dictionary out of the hrefs, add also a link to each href
        dict_hrefs = {}
        filtered_dict = {}
        for item in filtered_hrefs:
            dict_hrefs[str(item)[1:]] = str(item)[1:].split('.')  # remove '#' from tag

        # Filter the dictionary on user input

        for key, value in dict_hrefs.items():
            if search.lower() in str(key).lower() or search.lower() in str(value).lower():
                filtered_dict[key] = 'https://discordpy.readthedocs.io/en/latest/api.html#{}'.format(key)

        src_format = []
        # if search in filtered_dict.keys():
        # format matches
        search_matches = json.dumps(filtered_dict, indent=2)
        src_match_load = json.loads(search_matches)

        # Remove links duplicates
        for key in src_match_load.keys():
            if key not in src_match_load.keys():
                del src_match_load[key]

        limiter = 0
        for key, value in src_match_load.items():
            if str(key).startswith('discord.'):
                key = str(key).replace('discord.', '')
                src_format.append(f"- [{key}]({value})")

            # limiter check
            limiter += 1
            if limiter >= link_limit_rtfm:
                break

        # Pretyfy
        src_format = list(set(src_format))
        prety_format = '\n'.join(sorted(src_format, key=len))

        # check if there are results
        if search not in prety_format:
            prety_format = f'No results\n`{search}`'

        # prep and send message
        embed.add_field(name=f'Useful Links:',
                        value=f'**{prety_format}**\n..\nMore information can be found **{api_ref}** or **[here](https://www.google.nl/search?q=discordpy%20{search})**')
        embed.add_field(name=f'Additional links:',
                        value=f'{logging_help}\n{migrating}\n{whats_new}')
        msg = await self.bot.say(embed=embed)
        embed.set_footer(text=f'discord.py')
        await self.bot.add_reaction(msg, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Help(bot))