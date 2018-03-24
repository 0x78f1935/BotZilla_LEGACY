from discord.ext import commands
import json
import discord
import aiohttp
import random
import re
import xml.etree.ElementTree
import datetime
import pyfiglet
import sys
import os
try:
    from plugin.database import Database
except:
    pass

try:
    from imgurpython import ImgurClient
except:
    ImgurClient = False


class Images:
    """Image related commands."""

    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.imgur = ImgurClient(self.config['giphy-id'], self.config['giphy-secret'])
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.channels = self.tmp_config['channels']
        self.emojiUnicode = self.tmp_config['unicode']
        self.owner_list = self.config['owner-id']


    @commands.command(pass_context=True)
    async def ascii(self, ctx, font : str = None, *, text : str = None):
        '''
        Transform any text to ascii art.
        All available fonts can you find here:
        Full list: https://www.flamingtext.com/tools/figlet/fontlist.html
        Usage:
          - !!ascii <font> <text>
          - !!ascii <any random letter> <text> #gets a random font
        Example:
          - !!ascii big hello
          - !!ascii . hello
        '''
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!ascii <{font}> <{text}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        fonts = ["3-d", "3x5", "5lineoblique", "acrobatic", "alligator2", "alligator", "alphabet", "avatar", "banner3",
                 "banner4", "banner", "barbwire", "basic", "bell", "bigchief", "big", "binary", "block", "broadway",
                 "bubble", "bulbhead", "calgphy2", "caligraphy", "catwalk", "chunky", "coinstak", "colossal",
                 "computer", "contessa", "contrast", "cosmic", "cosmike", "crawford", "cricket", "cyberlarge",
                 "cybermedium", "cybersmall", "decimal", "diamond", "digital", "doh", "doom", "dotmatrix", "double",
                 "drpepper", "eftichess", "eftifont", "eftipiti", "eftirobot", "eftitalic", "eftiwall", "eftiwater",
                 "epic", "fender", "fourtops", "fuzzy", "goofy", "gothic", "graffiti", "hex", "hollywood", "invita",
                 "isometric1", "isometric2", "isometric3", "isometric4", "italic", "ivrit", "jazmine", "katakana",
                 "kban", "larry3d", "lcd", "lean", "letters", "linux", "lockergnome", "madrid", "marquee", "maxfour",
                 "mike", "mini", "mirror", "mnemonic", "nancyj-fancy", "nancyj", "nancyj-underlined", "nipples", "o8",
                 "octal", "ogre", "os2", "pawp", "peaks", "pebbles", "pepper", "poison", "puffy", "pyramid",
                 "rectangles", "relief2", "relief", "rev", "roman", "rot13", "rounded", "rowancap", "rozzo", "sblood",
                 "script", "serifcap", "shadow", "short", "slant", "slide", "slscript", "small", "smisome1",
                 "smkeyboard", "smscript", "smshadow", "smslant", "speed", "stacey", "stampatello", "standard",
                 "starwars", "stellar", "stop", "straight", "tanja", "term", "thick", "thin", "threepoint", "ticks",
                 "ticksslant", "tinker-toy", "tombstone", "trek", "twopoint", "univers", "usaflag", "weird", "whimsy"]
        if text == None:
            embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                  description="You should check out **`{}help ascii`**".format(self.config['prefix']),
                                  color=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return
        elif font == None:
            embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                  description="You should check out **`{}help ascii`**".format(self.config['prefix']),
                                  color=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return
        else:
            if font.lower() == 'random' or font.lower() not in fonts:
                font = random.sample(fonts, 1)
                figlet = pyfiglet.Figlet(font=font[0])
                art = figlet.renderText(text)

                if len(art) >= 2000:
                    embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                          description="Unfortunate discords handles a character limitation of 2000 characters.\nDue to this fact try to shorten your text",
                                          color=0xf20006)
                    embed.set_footer(text="Font: {}".format(font[0]))
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['error'])
                    return

                embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                      description="```py\n{}\n```".format(art),
                                      color=0xf20006)
                embed.set_footer(text="Font: {}".format(font[0]))
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
                return

            if font.lower() in fonts:
                figlet = pyfiglet.Figlet(font=font)
                art = figlet.renderText(text)

                if len(art) >= 2000:
                    embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                          description="Unfortunate discords handles a character limitation of 2000 characters.\nDue to this fact try to shorten your text",
                                          color=0xf20006)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['error'])
                    return

                embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                      description="```py\n{}\n```".format(art),
                                      color=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            else:
                embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                      description="The font you gave doesnt exist, check **`{}help ascii`** for more information".format(self.config['prefix']),
                                      color=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['error'])



    @commands.command(pass_context=True)
    async def big(self, ctx, *, emoji : str = None):
        """
        Make custom emojis 10x time bigger!
        Usage:
          - !!big <custom emoji>
        Example:
          - !!big :cactus_sap0:
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!big <{emoji}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if emoji is None:
            embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                  description="You should big time check out **`{}help big`** instead".format(self.config['prefix']),
                                  color=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return
        else:
            emote = str(emoji).split(':')
            try:
                emote = ''.join(re.findall(r"[a-zA-Z_0-9]", emote[1]))
                emoteO = discord.utils.get(ctx.message.server.emojis, name=emote)
                async with aiohttp.ClientSession() as session:
                    async with session.get(emoteO.url, allow_redirects=True) as r:
                        await self.bot.send_typing(ctx.message.channel)
                        embed = discord.Embed(title='{}:'.format(ctx.message.author.name), description='\t', colour=0xf20006)
                        embed.set_image(url=emoteO.url)
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            except Exception as e:
                embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                      description="The emoji **`{}`** was not found\nPerhaps this is not a custom server emoji.".format(emote),
                                      color=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])


    @commands.command(pass_context=True, no_pm=True)
    async def gif(self, ctx, *keywords):
        """
        Retrieves a random gif from a giphy search
        Usage:
          - !!gif
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!gif <{keywords}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if keywords:
            keywords = "+".join(keywords)
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='sigh.. **`{}help gif`**'.format(self.config['prefix']),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['error'])
            return
        await self.bot.send_typing(ctx.message.channel)
        url = ("http://api.giphy.com/v1/gifs/random?&api_key={}&tag={}"
               "".format(self.config['giphy-api-key'], keywords))

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.json(encoding='utf8')

        source = json.dumps(source)
        result = json.loads(str(source))

        if response.status == 200:
            if result["data"]:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='{}'.format(''),
                                      colour=0xf20006)
                embed.set_image(url=result["data"]["image_original_url"])
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            else:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='{}'.format('No results found.'),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format('Error contacting the API'),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['error'])


    @commands.command(pass_context=True)
    async def rule34(self, ctx, *, content=None):
        """
        Shows graphical content NSFW.
        Rule#34 : If it exists there is porn of it. If not, start uploading.
        Works only in channels with nsfw in the name.
        Usage:
          - !!rule34 <search term>
        Example:
          - !!rule34 pizza
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!rule34 <{content}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if 'nsfw' not in str(ctx.message.channel.name).lower():
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You do not have the permission to use this command outside a NSFW channel.',
                                  colour=0xf20006)
            await self.bot.say(embed=embed)
            return

        if content == None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Maybe you should considering using **`{}help rule34`** instead'.format(self.config['prefix']),
                                  colour=0xf20006)
            await self.bot.say(embed=embed)
            return
        else:
            link = 'http://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=100&tags={}'.format(content)
            url = link.replace(' ', '_').replace('+', ' ')
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    source = await response.read()

            root = xml.etree.ElementTree.fromstring(source)

            try:
                image = root[random.randint(0, len(root) - 1)].attrib['file_url']

                try:
                    if image.endswith(".webm"):
                        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                              description='Naughty boy grrrr tiger :tiger:',
                                              colour=0xf20006)
                        last_message = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                        await self.bot.say(embed=embed)
                        return

                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          colour=0xf20006)
                    embed.set_image(url=image)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

                except ValueError:
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='No results found for **`{}`**'.format(content),
                                          colour=0xf20006)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])

                except Exception as e:
                    a = await self.bot.say(image)
                    await self.bot.add_reaction(a, self.emojiUnicode['succes'])

            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='No results found for **`{}`**'.format(content),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])

    @commands.command(pass_context=True ,aliases=["av"])
    async def avatar(self, ctx, *, member:discord.Member=None):
        """
        Shows a big avatar from a discord user
        Usage:
          - !!avatar <username | ping | id>
        Example:
          - !!avatar puffdip
          - !!avatar @puffdip
          - !!avatar 275280442884751360
        Alias:
          - !!av
        Example:
          - !!av @puffdip
        """
        user = member or ctx.message.author
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!avatar <{user.name}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        embed = discord.Embed(title='{}\'s avatar:'.format(user.name),
                              description='\t',
                              colour=0xf20006)
        embed.set_image(url=user.avatar_url)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


class Fun:
    """
    Fun related commands.
    """

    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.imgur = ImgurClient(self.config['giphy-id'], self.config['giphy-secret'])
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.channels = self.tmp_config['channels']
        self.emojiUnicode = self.tmp_config['unicode']
        self.owner_list = self.config['owner-id']
        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except Exception as e:
            print('Test: Database files not found - {}'.format(e.args))
            pass

    @commands.command(pass_context=True)
    async def hack(self, ctx, *, account : str = None):
        """
        Check if your username or email is hacked.
        Sometimes companys get hacked. Sometime the hackers decide
        to put the information they stole online.
        Use this command to check of your account has been leaked.
        Works on e-mail and username.
        Usage:
          - !!hack <account name | email>
        Example:
          - !!hack hermin10
          - !!hack hermin10@hermin10.com
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!hack <{account}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if account == None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You should use **`{}help hacked`** first.'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        search = account.replace(' ', '%20')
        url = 'https://haveibeenpwned.com/api/v2/breachedaccount/{}?truncateResponse=true'.format(search)


        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    source = await response.json(encoding='utf8')

            source = json.dumps(source, indent=2)
            result = json.loads(str(source))

            if result == None:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Your account **`{}`** seems safe'.format(account),
                                      colour=0xf20006)
                embed.set_footer(text="Data © haveibeenpwned contributors, https://haveibeenpwned.com/About")
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                return

            siteslist = []
            for site in result:
                siteslist.append(site['Name'])

            sites = "\n".join(siteslist)

            if len(sites) >= 1000:
                target = await self.bot.get_user_info(ctx.message.author.id)
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='The internet is full of hackers\nThe following services have been hacked by them...\nTheir information is leaked online. That means that also your information is leaked!\nThe following online services leaked the information of account\n\n`{}`\n\nAdvice: **`Change your password`**\n**```{}```**'.format(account, sites),
                                      colour=0xf20006)
                embed.set_footer(text="Data © haveibeenpwned contributors, https://haveibeenpwned.com/About")
                last_message = await self.bot.send_message(target, embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Advice: **`Change your password`**\nDetails send through DM\nCheck your inbox!',
                                      colour=0xf20006)
                embed.set_footer(text="Data © haveibeenpwned contributors, https://haveibeenpwned.com/About")
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            else:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='The internet is full of hackers. The following services have been hacked by them...\nTheir information is leaked online. That means that also your information is leaked!\nThe following online services leaked the information of account\n\n`{}`\n\nAdvice: **`Change your password`**\n**```{}```**'.format(account, sites),
                                      colour=0xf20006)
                embed.set_footer(text="Data © haveibeenpwned contributors, https://haveibeenpwned.com/About")
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])

        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Something went wrong:\n**{}:**\n```py\n{}```'.format(type(e).__name__, e),
                                  colour=0xf20006)
            embed.set_footer(text="Data © haveibeenpwned contributors, https://haveibeenpwned.com/About")
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


    @commands.command(pass_context=True)
    async def dict(self, ctx, *, keywords : str = None):
        """
        Look something up in the UrbanDictionary.
        Use this command with a search keyword.
        Usage:
          - !!dict <keyword>
        Example:
          - !!dict Hippopotomonstrosesquipedaliophobia
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!dict <{keywords}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if keywords is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Did you tried **`{}help dict`** yet?'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return
        if keywords:
            old_keyword = keywords
            try:
                keywords = "%20".join(keywords)
                url = 'http://api.urbandictionary.com/v0/define?term={}'.format(keywords)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        source = await response.json(encoding='utf8')

                source = json.dumps(source, indent=2)
                result = json.loads(str(source))
                example = str(result['list'][0]['example'])
                example = example[:500]
                definition = str(result['list'][0]['definition'])
                definition = definition[:500]
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Your search tag was:\n***`{}`***'.format(old_keyword),
                                      colour=0xf20006)
                embed.add_field(name='Word:', value='`{}`'.format(result['list'][0]['word']), inline=False)
                embed.add_field(name='Definition:', value='```{}```'.format(definition), inline=False)
                embed.add_field(name='example:', value='```{}```'.format(example), inline=True)
                embed.add_field(name='Author:', value='`{}`'.format(result['list'][0]['author']), inline=False)
                embed.add_field(name='Link:', value='{}'.format(result['list'][0]['permalink']), inline=False)
                embed.add_field(name='Likes:', value='\U0001f44d `{}`'.format(result['list'][0]['thumbs_up']),
                                inline=True)
                embed.add_field(name='Dislikes:', value='\U0001f44e `{}`'.format(result['list'][0]['thumbs_down']),
                                inline=True)


                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Your search tag was:\n***`{}`***\n\nNothing found :sailboat:'.format(old_keyword, self.config['prefix']),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])


    @commands.command(pass_context=True)
    async def sb(self, ctx, *, text : str = None):
        """
        SpOnGeBoByFy, Transform your text!
        Use this command with any sentence you like to transform.
        Usage:
          - !!sb <text>
        Example:
          - !!sb hello world
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!sb <{text}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if text == None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Maybe you should try **`{}help sb`** instead.'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return


        try:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=''.join(random.choice([k.upper(), k]) for k in text.lower()),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='FoR SoMe ReAsOn I CoUlD NoT TrAnSfOrM YoUr TeXt, ChAnGe YoUr SeNtEnCe A bIt AnD tRy AgAiN',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])


    @commands.command(pass_context=True)
    async def joke(self, ctx):
        """
        Ever heard a Chuck Norris joke?
        Usage:
          - !!joke
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!joke in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        url = 'http://api.icndb.com/jokes/random%22'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.json(encoding='utf8')

        source = json.dumps(source)
        data = json.loads(str(source))
        joke = str(data['value']['joke'])

        if '&quot;' in joke:
            joke = joke.replace("&quot;", "")

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description="{}".format(joke),
                              colour=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
        return

    @commands.command(pass_context=True, hidden=True)
    async def meow(self, ctx):
        """
        Spawn a kitty cat!
        Usage:
          - !!meow
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!meow in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        url = 'http://placekitten.com/'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.read()
        art = str(source[559:1000], 'utf8')
        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='```{}```'.format(art),
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])

    @commands.command(pass_context=True)
    async def infect(self, ctx, member:discord.Member = None, emoji : str = None):
        """
        Now is your chance to infect someone with reactions!
        Each infect has a duration of one hour.
        To get healed again check out heal for more info.
          - !!help heal
        Usage:
          - !!infect <username | ping | id> <emoji>
        Example:
          - !!infect puffdip :smirk:
          - !!infect @puffdip :smiley:
          - !!infect 275280442884751360 :wink:
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!infect <{member}> <{emoji}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        self.database.cur.execute("SELECT ID from botzilla.infect;")
        members_who_already_infected = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")

        if member is None or emoji is None:
            embed = discord.Embed(title=f'{ctx.message.author.name}',
                                  description=f'If you are stuck, Use **`{self.config["prefix"]}help infect`**\nThis will provide you with more information.',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        if str(member.id) in str(members_who_already_infected):
            embed = discord.Embed(title=f'{ctx.message.author.name}',
                                  description=f'**`{member.name}`** is already infected',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\U0001f480')
        else:
            now = datetime.datetime.now()
            until = now + datetime.timedelta(hours=1)
            emoji_stripped = emoji.strip('<>').split(':')[-1]
            try:
                int(emoji_stripped)
                emoji = discord.utils.get(self.bot.get_all_emojis(), id=emoji_stripped)
            except Exception as e:
                pass
            self.database.cur.execute("INSERT INTO botzilla.infect(ID, until, emoji) VALUES({}, '{}', '{}');".format(member.id, until, emoji_stripped))
            self.database.conn.commit()
            self.database.cur.execute("ROLLBACK;")
            embed = discord.Embed(title=f'{ctx.message.author.name}',
                                  description=f'**`{member.name}`** has been infected with **{emoji}** for **`one`** hour',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def heal(self, ctx, member:discord.Member = None):
        """
        Heal someone who is infected.
        If someone is not infected, infect them!
        To get more information on how to infect someone, use
          - !!help infect
        Usage:
          - !!heal <username | ping | id> <emoji>
        Example:
          - !!heal puffdip :smirk:
          - !!heal @puffdip :smiley:
          - !!heal 275280442884751360 :wink:
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!heal <{member}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if member is None:
            embed = discord.Embed(title=f'{ctx.message.author.name}',
                                  description=f'If you are stuck, Use **`{self.config["prefix"]}help heal`**\nThis will provide you with more information.',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        self.database.cur.execute("SELECT * from botzilla.infect WHERE ID = {};".format(member.id))
        members_who_already_infected = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")

        if str(member.id) in str(members_who_already_infected):
            self.database.cur.execute("SELECT * from botzilla.infect WHERE ID = {};".format(member.id))
            infected_member = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if ctx.message.author.id == str(infected_member[0]):
                embed = discord.Embed(title=f'{ctx.message.author.name}',
                                      description=f'**`{member.name}`** you can\'t heal yourself',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                return

            self.database.cur.execute("DELETE FROM botzilla.infect WHERE ID = {};".format(member.id))
            self.database.conn.commit()
            self.database.cur.execute("ROLLBACK;")
            embed = discord.Embed(title=f'{ctx.message.author.name}',
                                  description=f'**`{member.name}`** is healed again',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        else:
            embed = discord.Embed(title=f'{ctx.message.author.name}',
                                  description=f'**`{member.name}`** has not yet been infected,\ninfect **`{member.name}`**! **`{self.config["prefix"]}help infect`** for more info',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])


    @commands.command(pass_context=True, aliases=["phobia"])
    async def fear(self, ctx, phobia:str = None):
        """
        Search for any fear, phobia
        Usage:
          - !!fear <fear>
          - !!phobia <fear>
        Example:
          - !!fear hippopotomonstrosesquipedaliophobia
          - !!phobia hippopotomonstrosesquipedaliophobia

        """
        url = 'http://ikbengeslaagd.com/JS/phobia.json'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                source = await response.json(encoding='utf8')

        embed = discord.Embed(title=f'{ctx.message.author.name}',
                              description=f'**`{source[0]}`**\n~~**=======================**~~\n**`{phobia}`**',
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


def setup(bot):
    if ImgurClient is False:
        raise RuntimeError("You need the imgurpython module to use this.\n"
                           "pip3 install imgurpython")

    bot.add_cog(Images(bot))
    bot.add_cog(Fun(bot))