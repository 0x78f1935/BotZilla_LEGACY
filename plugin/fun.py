from discord.ext import commands
import json
import discord
import aiohttp
import random
import async_timeout
import re
import xml.etree.ElementTree
from bs4 import BeautifulSoup
import asyncio

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


    @commands.command(pass_context=True, hidden=True, name='hl')
    async def HighLow(self, ctx):
        game = True
        while game:
            number = random.randrange(0,1000)
            embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                  description='Higher or Lower then: **`{}`**\n**`10`** Seconds to vote..'.format(number),
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
                embed = discord.Embed(title='HighLow:',
                                      description='GameOver! Nobody voted'.format(new_number),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, '\U0001f480')
                game = False

            elif total_less == total_more:
                embed = discord.Embed(title='HighLow:',
                                      description='Draw!\nContinue? **`10`** Seconds remaining'.format(new_number),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, '\U0001f3f3')
                await self.bot.add_reaction(a, '\U0001f3f3')
                total_continue = message.reactions[0].count - 1
                if total_continue > 0:
                    game = True
                else:
                    game = False
                await asyncio.sleep(10)
                await self.bot.delete_message(a)

            elif winner == total_more and new_number >= number:
                embed = discord.Embed(title='HighLow:',
                                      description='Victorious! You hit number **`{}`**\nTotals\n-------\n:arrow_up_small: : **`{}`**    :arrow_down_small: : **`{}`**\nTotal Votes: **`{}`**\n\nNext round in **`10`** Seconds'.format(new_number, total_more, total_less, total_votes),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                game = True
                await asyncio.sleep(10)
                await self.bot.delete_message(a)

            elif winner == total_less and new_number <= number:
                embed = discord.Embed(title='HighLow:',
                                      description='Victorious! You hit number **`{}`**\nTotals\n-------\n:arrow_up_small:  : **`{}`**    :arrow_down_small: : **`{}`**\nTotal Votes: **`{}`**\n\nNext round in **`10`** Seconds'.format(new_number, total_more, total_less, total_votes),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                game = True
                await asyncio.sleep(10)
                await self.bot.delete_message(a)

            else:
                embed = discord.Embed(title='HighLow:',
                                      description='GameOver! You hit number **`{}`**\nTotals\n-------\n:arrow_up_small:  : **`{}`**    :arrow_down_small: : **`{}`**\nTotal Votes: **`{}`**'.format(new_number, total_more, total_less, total_votes),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, '\U0001f480')
                game = False






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


def setup(bot):
    if ImgurClient is False:
        raise RuntimeError("You need the imgurpython module to use this.\n"
                           "pip3 install imgurpython")

    bot.add_cog(Images(bot))