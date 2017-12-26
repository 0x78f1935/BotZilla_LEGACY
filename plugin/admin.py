from discord.ext import commands
import json
import discord
import traceback
import psycopg2


class AdminCommands:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']

        debounce = False
        while True:
            if not debounce:
                debounce = True
                try:
                    conn = psycopg2.connect("dbname='bz' user='postgres' host='1.1.1.2' port='5432' password=''")
                    self.cur = conn.cursor()
                    print('Established Database connection')
                    break
                except:
                    print('I am unable to connect to the Database')
                debounce = False


    @commands.command(pass_context=True)
    async def kick(self, ctx, member:discord.Member):
        """Kicks a `Member` from the server they belong to.
        This function kicks the `Member` based on the server it belongs to,
        So you must have the proper permissions in that server."""
        if ctx.message.author.id not in self.owner_list:
            return
        await self.bot.kick(member)


    @commands.command(pass_context=True)
    async def game(self, ctx, game: str = None, *, url: str = None):
        """
        Change the bots game.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            self.bot.say(embed=embed)
            return
        if game is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You stupid! use `{}help game` instead'.format(self.config['prefix']),
                                  colour=0xf20006)
            self.bot.say(embed=embed)
            return

        if not url:
            game = discord.Game(name=game, type=0)
        else:
            game = discord.Game(name=game, url=url, type=1)
        await self.bot.change_presence(game=game)

    # ===========================
    #   Module related commands
    # ===========================

    @commands.command(pass_context=True)
    async def load(self, ctx,  *, extension: str):
        """
        Load an extension.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            self.bot.say(embed=embed)
        extension = extension.lower()
        try:
            self.bot.load_extension("plugin.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            await self.bot.say("Could not load `{}` -> `{}`".format(extension, e))
        else:
            await self.bot.say("Loaded cog `plugin.{}`.".format(extension))

    @commands.command(pass_context=True)
    async def unload(self, ctx, *, extension: str):
        """
        Unload an extension.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            self.bot.say(embed=embed)
        extension = extension.lower()
        try:
            self.bot.unload_extension("plugin.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            await self.bot.say("Could not unload `{}` -> `{}`".format(extension, e))
        else:
            await self.bot.say("Unloaded `{}`.".format(extension))

    @commands.command(pass_context=True)
    async def reload(self, ctx, *, extension: str):
        """
        Reload an extension.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            self.bot.say(embed=embed)
        extension = extension.lower()
        try:
            self.bot.unload_extension("plugin.{}".format(extension))
            self.bot.load_extension("plugin.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            await self.bot.say("Could not reload `{}` -> `{}`".format(extension, e))
        else:
            await self.bot.say("Reloaded `{}`.".format(extension))

    @commands.command(pass_context=True)
    async def reloadall(self, ctx):
        """
        Reload all extensions.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            self.bot.say(embed=embed)
        for extension in self.bot.extensions:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            except Exception as e:
                await self.bot.say("Could not reload `{}` -> `{}`".format(extension, e))

        await self.bot.say("Reloaded all.")


def setup(bot):
    bot.add_cog(AdminCommands(bot))