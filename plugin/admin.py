from discord.ext import commands
from discord.ext.commands.errors import CommandInvokeError
import json
import discord
import traceback
try:
    from plugin.database import Database
except:
    pass


class AdminCommands:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']
        self.blue_A = '\U0001f1e6'
        self.red_B = '\U0001f171'
        self.blue_I = '\U0001f1ee'
        self.blue_L = '\U0001f1f1'
        self.blue_O = '\U0001f1f4'
        self.blue_T = '\U0001f1f9'
        self.blue_Z = '\U0001f1ff'
        self.arrow_up = '\u2b06'
        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except:
            print('AdminPanel: Database files not found')
            pass


    @commands.command(pass_context=True, hidden=True)
    async def kick(self, ctx, member:discord.Member):
        """
        Kicks a `Member` from the server they belong to.
        This function kicks the `Member` based on the server it belongs to,
        So you must have the proper permissions in that server.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        try:
            await self.bot.kick(member)
        except discord.ext.commands.CommandInvokeError as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command you do not have permission in server:"\n{}'.format(ctx.message.server.name),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])


    @commands.command(pass_context=True, hidden=True)
    async def game(self, ctx, game: str = None, *, url: str = None):
        """
        Change the bots game.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        if game is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You stupid! use `{}help game` instead'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        if not url:
            game = discord.Game(name=game, type=0)
        else:
            game = discord.Game(name=game, url=url, type=1)
        await self.bot.change_presence(game=game)

    # ===========================
    #   Module related commands
    # ===========================

    @commands.command(pass_context=True, hidden=True)
    async def load(self, ctx,  *, extension: str):
        """
        Load an extension.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        extension = extension.lower()
        try:
            self.bot.load_extension("plugin.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            a = await self.bot.say("Could not load `{}` -> `{}`".format(extension, e))
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
        else:
            a = await self.bot.say("Loaded cog `plugin.{}`.".format(extension))
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, hidden=True)
    async def unload(self, ctx, *, extension: str):
        """
        Unload an extension.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        extension = extension.lower()
        try:
            self.bot.unload_extension("plugin.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            a = await self.bot.say("Could not unload `{}` -> `{}`".format(extension, e))
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
        else:
            a = await self.bot.say("Unloaded `{}`.".format(extension))
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, hidden=True)
    async def reload(self, ctx, *, extension: str):
        """
        Reload an extension.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        extension = extension.lower()
        try:
            self.bot.unload_extension("plugin.{}".format(extension))
            self.bot.load_extension("plugin.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            a = await self.bot.say("Could not reload `{}` -> `{}`".format(extension, e))
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
        else:
            a = await self.bot.say("Reloaded `{}`.".format(extension))
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, hidden=True)
    async def reloadall(self, ctx):
        """
        Reload all extensions.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        for extension in self.bot.extensions:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            except Exception as e:
                a = await self.bot.say("Could not reload `{}` -> `{}`".format(extension, e))
                await self.bot.add_reaction(a, self.emojiUnicode['error'])

        a = await self.bot.say("Reloaded all.")
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, hidden=True)
    async def sendalldm(self, ctx, *, content: str = None):
        """
        Mass DM everyone in database
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        if content is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may want to read **`{}help sendalldm`** for more info'.format(self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        try:
            database = Database(self.bot)
            database.cur.execute("select id from botzilla.users;")
            rows = database.cur.fetchall()
            database.cur.execute("ROLLBACK;")
            for row in rows:
                row = str(row).replace('(', '')
                row = str(row).replace(',)', '')
                print(type(row))
                target = await self.bot.get_user_info(row)
                embed = discord.Embed(title='{}:'.format('Announcement'),
                                      description='{}'.format(content),
                                      colour=0xf20006)
                last_message = await self.bot.send_message(target, embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Done',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        except Exception as e:
            print(e.args)


    @commands.command(pass_context=True, hidden=True)
    async def senddm(self, ctx, *, user_id: str = None, Message: str = None):
        """
        DM single user
        First ID after ID message
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return


        id = [int(s) for s in user_id.split() if s.isdigit()]
        id = str(id).replace('[', '')
        id = id.replace(']', '')
        content = user_id.replace('{}'.format(id), '')
        await self.bot.delete_message(ctx.message)
        target = await self.bot.get_user_info(id)
        embed = discord.Embed(title='{}:'.format('Announcement'),
                              description='{}'.format(content),
                              colour=0xf20006)
        last_message = await self.bot.send_message(target, embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
        for owner in self.config['owner-id']:
            owner = await self.bot.get_user_info(owner)
            last_message = await self.bot.send_message(owner, embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(AdminCommands(bot))