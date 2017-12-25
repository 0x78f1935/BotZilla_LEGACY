from discord.ext import commands
import json
import urllib.request
import xml.etree.ElementTree
import random
import discord

tmp_config = json.loads(str(open('./options/config.js').read()))
channels = tmp_config['channels']
nsfw_channels = channels['nsfw']

class NSFW:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']


    @commands.command(pass_context=True)
    async def rule34(self, ctx, *, content=None):

        if ctx.message.channel.id not in nsfw_channels:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You do not have the permission to use this command outside a NSFW channel.',
                                  colour=0xf20006)
            await self.bot.say(embed=embed)
            return

        if content == None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Maybe you should considering using `{}help rule34` instead'.format(tmp_config['config']['prefix']),
                                  colour=0xf20006)
            await self.bot.say(embed=embed)
        else:
            link = 'http://rule34.xxx/index.php?page=dapi&s=post&q=index&limit=100&tags=' + content
            rget = urllib.request.urlopen(link.replace(' ', '_').replace('+', ' '))
            rget = rget.read()
            root = xml.etree.ElementTree.fromstring(rget)
            print("[NSFW] [RULE34] %s" % (link))

            try:
                image = root[random.randint(0, len(root) - 1)].attrib['file_url']

                if image.endswith(".webm"):
                    await self.bot.say("Naughty boy grrrr tiger :tiger:")
                    return

                if image.endswith(".png"):
                    print("[NSFW] [RULE34] Sending {} 'PNG' image".format(ctx.message.author.name))
                    pass

                if image.endswith(".jpg"):
                    print("[NSFW] [RULE34] Sending {} 'JPG' image".format(ctx.message.author.name))
                    pass

                if image.endswith(".jpeg"):
                    print("[NSFW] [RULE34] Sending {} 'JPEG' image".format(ctx.message.author.name))
                    pass

                if image.endswith(".gif"):
                    print("[NSFW] [RULE34] Sending {} 'GIF' image".format(ctx.message.author.name))
                    pass

                image = "https:{}".format(image)
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='{}'.format(''),
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

def setup(bot):
    bot.add_cog(NSFW(bot))