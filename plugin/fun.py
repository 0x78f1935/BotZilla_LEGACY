from discord.ext import commands
import json
import discord
import aiohttp
import random
import async_timeout
import re
import xml.etree.ElementTree
from bs4 import BeautifulSoup

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


    @commands.command(pass_context=True, no_pm=True)
    async def gif(self, ctx, *keywords):
        """Retrieves a random gif from a giphy search"""
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
    async def credits(self, ctx):
        """Give credit to a user"""
        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='\n:ok_hand:  :laughing:\n  :telephone_receiver::shirt::call_me:\n         :jeans:        :fire:',
                              colour=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def rule34(self, ctx, *, content=None):
        """
        Shows graphical content NSFW.
        Rule#34 : If it exists there is porn of it. If not, start uploading.
        Works only in channels with nsfw in the name.
        """

        if 'nsfw' not in str(ctx.message.channel.name).lower():
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You do not have the permission to use this command outside a NSFW channel.',
                                  colour=0xf20006)
            await self.bot.say(embed=embed)
            return

        if content == None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Maybe you should considering using `{}help rule34` instead'.format(self.config['prefix']),
                                  colour=0xf20006)
            await self.bot.say(embed=embed)
            return
        else:
            link = 'http://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=100&tags=' + content
            url = link.replace(' ', '_').replace('+', ' ')
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    source = await response.read()

            root = xml.etree.ElementTree.fromstring(source)
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

                if image.endswith(".png"):
                    pass

                if image.endswith(".jpg"):
                    pass

                if image.endswith(".jpeg"):
                    pass

                if image.endswith(".gif"):
                    pass


                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      colour=0xf20006)
                embed.set_image(url=image)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
                return
            except ValueError:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='{}'.format('No results found.'),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                return
            except Exception as e:
                a = await self.bot.say(image)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def dict(self, ctx, *keywords):
        """
        Look something up in the UrbanDictionary.
        Use this command with a search keyword.
        """

        if not keywords:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Did you tried `{}help dict` yet?'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return
        if keywords:
            old_keyword = " ".join(keywords)
            try:
                keywords = "%20".join(keywords)
                url = 'http://api.urbandictionary.com/v0/define?term={}'.format(keywords)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        source = await response.json(encoding='utf8')

                source = json.dumps(source, indent=2)
                result = json.loads(str(source))
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Your search tag was:\n***`{}`***'.format(old_keyword),
                                      colour=0xf20006)
                embed.add_field(name='Word:', value='`{}`'.format(result['list'][0]['word']), inline=False)
                embed.add_field(name='Definition:', value='```{}```'.format(result['list'][0]['definition']), inline=False)
                embed.add_field(name='example:', value='```{}```'.format(result['list'][0]['example']), inline=True)
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


    @commands.command(pass_context=True, hidden=True)
    async def meow(self, ctx):
        """
        Easter egg!
        Spawn a kitty cat!
        """
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


    @commands.command(pass_context=True, name='dr', hidden=True)
    async def DeathRow(self, ctx):
        """
        Deathrow! Checkout someones last words spoken on a death row!
        The person is real en registered at Texas Department of Criminal Justice.
        All data is open for public.
        """
        url = 'http://www.tdcj.state.tx.us/death_row/dr_executed_offenders.html'

        async def fetch(session, url):
            with async_timeout.timeout(10):
                async with session.get(url) as response:
                    return await response.text()

        offenders = []
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, url)
            soup = BeautifulSoup(html, 'lxml')

            for link in soup.find_all('a'):
                link2 = link.get('href')
                if re.match(r'dr_info\/(.*)', str(link2), flags=0):
                    link = re.match(r'dr_info\/(.*)', str(link2)).group()
                    good_final = link.replace('dr_info/', 'http://www.tdcj.state.tx.us/death_row/dr_info/')
                    offenders.append(str(good_final))

        while True:
            url = random.choice(offenders)
            if str(url).endswith('.html'):
                break
            else:
                pass

        url = random.choice(offenders)
        async with aiohttp.ClientSession() as session:
            html = await fetch(session, str(url))
        print(html)
        await self.bot.say(url)


class Fun:
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


    @commands.command(pass_context=True, hidden=True)
    async def hacked(self, ctx, *, account : str = None):
        """
        Check if your username or email is hacked.
        Sometimes companys get hacked. Sometime the hackers decide
        to put the information they stole online.
        Use this command to check of your account has been leaked.
        Works on e-mail and username.
        """

        if account == None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You should use `{}help hacked` first.'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        url = 'https://haveibeenpwned.com/api/v2/breachedaccount/{}?truncateResponse=true'.format(account)

        if '@' in url:
            # make email request
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    source = await response.json(encoding='utf8')

            source = json.dumps(source, indent=2)
            result = json.loads(str(source))
            if result == None:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Your email: `{}` seems safe'.format(account),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                return

            print("MAIL")
            print(result)
            print("--------------------------------------------------------")
            pass
        else:
            # make username
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    source = await response.json(encoding='utf8')

            source = json.dumps(source, indent=2)
            result = json.loads(str(source))

            if result == None:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Your username: `{}` seems safe'.format(account),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                return

            siteslist = []
            for site in result:
                siteslist.append(site['Name'])


            sites = "\n".join(siteslist)
            print(sites)


            print("USERNAME")
            print(result)
            print("--------------------------------------------------------")
            pass





def setup(bot):
    if ImgurClient is False:
        raise RuntimeError("You need the imgurpython module to use this.\n"
                           "pip3 install imgurpython")

    bot.add_cog(Images(bot))
    bot.add_cog(Fun(bot))