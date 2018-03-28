from discord.ext import commands
import os
import json
import discord
import traceback
import aiohttp
import datetime
from bs4 import BeautifulSoup
from ftplib import FTP
import random
try:
    from plugin.database import Database
except Exception as e:
    pass
import asyncio


class AdminCommands:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']
        self.ftp_conf = self.tmp_config['FTP']
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
    async def kick(self, ctx, member:discord.Member = None):
        """
        Kick a discord member from your server.
        You must have the proper permissions in the server where you use the kick command.
        Only the owner of this bot can use this command.

        Usage:
          - !!kick <user.mention | user.id | user.name>
        Example:
          - !!kick PuffDip
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!kick <{member}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        if member is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You forgot a user to kick :rofl:',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])

        try:
            await self.bot.kick(member)
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You kicked **`{}`** from **`{}`**'.format(
                                      member.mention, ctx.message.server.name),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command you do not have permission in server:\n{}'.format(
                                      ctx.message.server.name),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])

    # ===========================
    #   Module related commands
    # ===========================

    @commands.command(pass_context=True, hidden=True)
    async def load(self, ctx,  *, extension: str):
        """
        Load an extension.
        Only the owner of this bot can use this command.

        Usage:
          - !!load <cogname>
        Example:
          - !!load fun
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!load <{extension}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        extension = extension.lower()
        try:
            self.bot.load_extension("plugin.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description="Could not load `{}` -> `{}`".format(extension, e),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description="Loaded cog `plugin.{}`.".format(extension),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, hidden=True)
    async def unload(self, ctx, *, extension: str):
        """
        Unload an extension.
        Only the owner of this bot can use this command.

        Usage:
          - !!unload <cogname>
        Example:
          - !!unload fun
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!unload <{extension}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        extension = extension.lower()
        try:
            self.bot.unload_extension("plugin.{}".format(extension))
        except Exception as e:
            traceback.print_exc()
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description="Could not unload `{}` -> `{}`".format(extension, e),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description="Unloaded `{}`.".format(extension),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, hidden=True)
    async def reload(self, ctx, *, extension: str):
        """
        Reload an extension.
        Only the owner of this bot can use this command.

        Usage:
          - !!reload <cogname>
        Example:
          - !!reload fun
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!reload <{extension}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
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
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description="Could not reload `{}` -> `{}`".format(extension, e),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description="Reloaded `{}`.".format(extension),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, hidden=True)
    async def reloadall(self, ctx):
        """
        Reload all extensions.
        Only the owner of this bot can use this command.

        Usage:
          - !!reloadall
        Example:
          - !!reloadall
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!reloadall in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        for extension in self.bot.extensions:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description="Could not reload `{}` -> `{}`".format(extension, e),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description="Reloaded all.",
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, hidden=True)
    async def sendalldm(self, ctx, *, content: str = None):
        """
        Mass DM everyone in database
        Only the owner of this bot can use this command.

        Usage:
          - !!sendalldm <message>
        Example:
          - !!sendalldm Hello all
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!sendalldm in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        if content is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may want to read **`{}help sendalldm`** for more info'.format(
                                      self.config['prefix']),
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
                try:
                    target = await self.bot.get_user_info(int(row))
                    await asyncio.sleep(1)
                    embed = discord.Embed(title='{}:'.format('Announcement'),
                                          description='{}'.format(content),
                                          colour=0xf20006)
                    last_message = await self.bot.send_message(target, embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
                    print(f'succesfull send {row}')
                except Exception as e:
                    print(f'can\'t send to {row}\n{e.args}')
        except Exception as e:
            print(e.args)

    @commands.command(pass_context=True, hidden=True)
    async def senddm(self, ctx, user_id: discord.Member = None, *, MSG: str = None):
        """
        DM single user
        Only the owner of this bot can use this command.

        Usage:
          -  !!senddm <member> <message>
        Example:
          - !!senddm PuffDip hello world
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!senddm <{user_id.id}> <{MSG}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        await self.bot.delete_message(ctx.message)
        target = await self.bot.get_user_info(user_id.id)
        embed = discord.Embed(title='{}:'.format('Announcement'),
                              description='{}'.format(MSG),
                              colour=0xf20006)
        last_message = await self.bot.send_message(target, embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

        for owner in self.config['owner-id']:
            owner = await self.bot.get_user_info(owner)
            last_message = await self.bot.send_message(owner, embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, hidden=True)
    async def ip(self, ctx):
        """
        Show server IP
        Only the owner of this bot can use this command.

        Usage:
          - !!ip
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!ip in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.ipify.org/') as response:
                source = await response.read()

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description=f"```py\n{source.decode('utf-8')}\n```",
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, hidden=True)
    async def purge(self, ctx):
        """
        Purge bot messages.
        Only the owner of this bot can use this command.

        Usage:
          - !!purge
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!purge in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        def is_me(m):
            return m.author == self.bot.user

        def is_command(m):
            if str(m.content).startswith(self.config['prefix']):
                return True

        try:
            deleted_bot_messages = await self.bot.purge_from(ctx.message.channel, limit=500, check=is_me)
            deleted_user_messages = await self.bot.purge_from(ctx.message.channel, limit=500, check=is_command)
            total = len(deleted_bot_messages) + len(deleted_user_messages)
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Deleted {} message(s)'.format(total),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            await asyncio.sleep(3)
            try:
                await self.bot.delete_message(a)
            except Exception as e:
                pass
        except discord.ext.commands.CommandInvokeError as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=f'**{type(e).__name__}:**\n```py\n{e}```',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            await asyncio.sleep(7)
            try:
                await self.bot.delete_message(a)
            except Exception as e:
                pass
        except discord.HTTPException as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=f'**{type(e).__name__}:**\n```py\n{e}```',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            await asyncio.sleep(7)
            try:
                await self.bot.delete_message(a)
            except Exception as e:
                pass

    @commands.command(pass_context=True, hidden=True)
    async def git(self, ctx):
        """
        Pull latest branch and shows information about the pull.
        Only the owner of this bot can use this command.

        Usage:
          - !!git
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!git in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        else:
            pull = os.popen('git pull').read()
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Pull success :ok_hand:\n```py\n{}\n```'.format(pull),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, hidden=True, name='ct')
    async def clean_terminal(self, ctx):
        """
        Cleans terminal server [LINUX]
        Only the owner of this bot can use this command.

        Usage:
          - !!ct
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!clean_terminal in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        try:
            os.system('clear')
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Terminal server cleaned!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=f'**{type(e).__name__}:**\n```py\n{e}```',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])

    @commands.command(pass_context=True, hidden=True)
    async def mute(self, ctx, *, user_id: str = None):
        """
        Mute user. Bot roll has to be higher then user roll in order to work.
        Only the owner of this bot can use this command.

        Usage:
          - !!mute <user ID>
        Example:
          - !!mute PuffDip
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!mute <{user_id}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        if user_id is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Enter a user to **`mute`**',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        try:
            try:
                username = user_id.replace('<@', '')
                username = username.replace('>', '')
                username = username.replace('!', '')
                user = await self.bot.get_user_info(username)
                self.database.cur.execute(f"INSERT INTO botzilla.mute (ID) VALUES ('{user.id}');")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'**`{user.name}`** Muted',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])

            except Exception as e:
                user = await self.bot.get_user_info(user_id)
                self.database.cur.execute(f"INSERT INTO botzilla.mute (ID) VALUES ('{user.id}');")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'**`{user.name}`** Muted',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])

        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=f'**{type(e).__name__}:**\n```py\n{e}```',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])

    @commands.command(pass_context=True, hidden=True)
    async def unmute(self, ctx, *, user_id: str = None):
        """
        Unmute user. Remove user who is muted from database.
        Only the owner of this bot can use this command.

        Usage:
          - !!unmute <user ID>
        Example:
          - !!unmute PuffDip
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!mute <{user_id}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        if user_id is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Enter a user to **`mute`**',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        try:
            try:
                username = user_id.replace('<@', '')
                username = username.replace('>', '')
                username = username.replace('!', '')
                username = int(username)
                user = await self.bot.get_user_info(username)
                self.database.cur.execute(f"DELETE FROM botzilla.mute where ID = '{user.id}';")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'**`{user.name}`** Unmuted',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])

            except Exception as e:
                user = await self.bot.get_user_info(user_id)
                self.database.cur.execute(f"DELETE FROM botzilla.mute where ID = '{user.id}';")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'**`{user.name}`** Unmuted',
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
    async def sebisauce(self, ctx):
        """
        Get a image related to Sebi.
        Sebi is a random guy with perfect code related sentences.

        Usage:
          - !!sebisauce
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!sebisauce in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        await self.bot.send_typing(ctx.message.channel)

        async with aiohttp.ClientSession() as session:
            async with session.get('http://ikbengeslaagd.com/API/sebisauce.json') as response:
                source = await response.json(encoding='utf8')

        total_sebi = 0
        for key in dict.keys(source):
            total_sebi += 1

        im = random.randint(0, int(total_sebi) - 1)

        embed = discord.Embed(title='\t', description='\t', color=0xf20006)
        embed.set_image(url=source[str(im)])
        embed.set_footer(text="Data © Sebi\'s Bot Tutorial contributors, discord.gg/GWdhBSp")
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def updatesebi(self, ctx):
        """
        Update sebisauce API
        Only the owner of this bot can use this command.

        Usage:
          - !!updatesebi
        """

        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!sebiupdate in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        hrefs = []
        sebisauce = []
        url = 'https://github.com/AnakiKaiver297/sebisauce'

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                html = await response.read()

        bs = BeautifulSoup(html, 'lxml')
        for link in bs.find_all('a'):
            if link.has_attr('href'):
                hrefs.append(link.attrs['href'])

        for i in hrefs:
            if 'sebisauce/blob/master' in str(i):
                im = 'https://github.com' + i + '?raw=true'
                sebisauce.append(im)
        api = {}
        count = 0
        for i in sebisauce:
            api[count] = i
            count += 1
        api = json.dumps(api, indent=2)

        ftp = FTP(self.ftp_conf['ip'])
        ftp.login(user=self.ftp_conf['user'], passwd=self.ftp_conf['pass'])
        ftp.cwd('/official website/GUI/Pages/API/')
        filename = 'sebisauce.json'
        with open(filename, 'w') as fp:
            fp.write(api)

        ftp.storbinary('STOR ' + filename, open(filename, 'rb'))

        async with aiohttp.ClientSession() as session:
            async with session.get('http://ikbengeslaagd.com/API/sebisauce.json') as response:
                source = await response.json(encoding='utf8')

        total_sebi = 0
        for key in dict.keys(source):
            total_sebi += 1

        embed = discord.Embed(title='Sebisauce Collection is up-to-date',
                              description=f'Currently there are **`{total_sebi}`** entities',
                              colour=0xf20006)
        embed.set_footer(text='http://ikbengeslaagd.com/API/sebisauce.json')
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])

def setup(bot):
    bot.add_cog(AdminCommands(bot))