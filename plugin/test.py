import discord
from discord.ext import commands
import json
import datetime
import asyncio
import random
import aiohttp
import ast
import os
import sys
import re
try:
    from plugin.database import Database
except Exception as e:
    pass

tmp_config = json.loads(str(open('./options/config.js').read()))
config = tmp_config['config']
owner_list = config['owner-id']


class TestScripts:
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
        except Exception as e:
            print('Test: Database files not found - {}'.format(e.args))
            pass


    @commands.command(pass_context=True)
    async def cp(self, ctx, player : discord.Member = None):
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!cprofile <{player}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        print('load function')
        def check_profile(self, ID):
            self.database.cur.execute(f"select * from botzilla.c_user where ID = '{ID}';")
            profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            print('query executed')
            if profile is None:
                print('profile not found')
                return True
            else:
                print('profile found')
                return False

        if player:
            # mpplayer found
            print('mpplayer found')
            # If player doesnt exist
            if check_profile(self, player.id):
                # create profile
                print('No profile found')
            else:
                #profile found
                print('profile found')
        else:
            # player found
            print('player found')
            if check_profile(self, player.id):
                # create profile
                print('No profile found')
            else:
                #profile found
                print('profile found')

def setup(bot):
    bot.add_cog(TestScripts(bot))
