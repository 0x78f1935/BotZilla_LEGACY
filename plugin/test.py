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


    @commands.command(pass_context=True, aliases=["cr"])
    async def criminals(self, ctx, player : discord.Member = None):
        """
        Shows your criminal record. No worry...
        It is just a discord game. Look into !!help for more information
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!cr <{player}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        await self.bot.send_typing(ctx.message.channel)
        def check_profile(self, ID):
            self.database.cur.execute(f"select * from botzilla.c_user where ID = '{ID}';")
            profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if profile is None:
                print('profile not found')
                query = f"INSERT INTO botzilla.c_user(ID, LVL, XP, score, money, city, jail, jail_date, protected) VALUES({ID}, {int(0)}, {int(0)}, {int(0)}, {int(500)}, 'New York', 'FALSE', '{int(0)}', 'TRUE')"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                print('profile created')
            else:
                print('profile already exist')

        if player:
            # mpplayer found
            check_profile(self, player.id)
            self.database.cur.execute(f"select * from botzilla.c_user where ID = '{player.id}';")
            player_profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

        else:
            # player found
            check_profile(self, ctx.message.author.id)
            self.database.cur.execute(f"select * from botzilla.c_user where ID = '{ctx.message.author.id}';")
            player_profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

        requested_user = await self.bot.get_user_info(player_profile[0])
        embed = discord.Embed(title='Criminal Record of {} [CR]'.format(requested_user.name),
                              description=f'CR ID: **`{player_profile[0]}`**',
                              colour=0xf20006)

        if player:
            embed.add_field(name='Level', value='**`{}`**'.format(player_profile[1]), inline=True)
            embed.add_field(name='Experience', value='**`{}`**'.format(player_profile[2]), inline=True)
            embed.add_field(name='Highscore', value='**`{}`**'.format(player_profile[3]), inline=True)
            embed.add_field(name='Location', value='*`Unknown`*', inline=True)
            embed.add_field(name='Money', value='*`Unknown`*', inline=True)
            embed.add_field(name='Protected', value='*`Unknown`*', inline=True)
        else:
            embed.add_field(name='Level', value='**`{}`**'.format(player_profile[1]), inline=True)
            embed.add_field(name='Experience', value='**`{}`**'.format(player_profile[2]), inline=True)
            embed.add_field(name='Highscore', value='**`{}`**'.format(player_profile[3]), inline=True)
            embed.add_field(name='Location', value='**`{}`**'.format(player_profile[5]), inline=True)
            embed.add_field(name='Money', value='**`${},-`**'.format(player_profile[4]), inline=True)
            embed.add_field(name='Protected', value='**`{}`**'.format(player_profile[8]), inline=True)

        embed.set_thumbnail(url=f'{requested_user.avatar_url}')
        embed.set_footer(text=f'ID Number : {requested_user.id}')
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def steal(self, ctx, item = None):
        """
        Steal something,..
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!steal <{item}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        def check_profile(self, ID):
            self.database.cur.execute(f"select * from botzilla.c_user where ID = '{ID}';")
            profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if profile is None:
                print('profile not found')
                query = f"INSERT INTO botzilla.c_user(ID, LVL, XP, score, money, city, jail, jail_date, protected) VALUES({ID}, {int(0)}, {int(0)}, {int(0)}, {int(500)}, 'New York', 'FALSE', '{int(0)}', 'TRUE')"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                print('profile created')
            else:
                print('profile already exist')

        def time_to_wait(self, start_time):
            b = datetime.datetime.now()
            c = b - start_time
            # returns hour[0] minute[1]
            # if time > jail, example
            return divmod(c.days * 86400 + c.seconds, 60)

        check_profile(self, ctx.message.author.id)
        user_choice = str(item).lower()
        self.database.cur.execute(f"select * from botzilla.c_steal where name_item = '{user_choice}';")
        item = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")
        self.database.cur.execute(f"select * from botzilla.c_user where ID = '{ctx.message.author.id}';")
        game = self.database.cur.fetchone()
        self.database.cur.execute("ROLLBACK;")
        if user_choice in str(item):
            jail_number = random.randint(0, 100)

            print(item)
            print(item[0][0])
            print(item[0][1])
            print(item[0][2])
            print(item[0][3])
            print(item[0][4])
            print(item[0][5])
            print(item[0][6])
            print(item[0][7])
            print(item[0][8])
            print(item[0][9])
            print(item[0][10])

            print(game)
            print(game[0])
            print(game[1])
            print(game[2])
            print(game[3])
            print(game[4])
            print(game[5])
            print(game[6])
            print(game[7])
            print(game[8])

            embed = discord.Embed(title='{}:'.format(str(item[0][2])),
                                  description=f'*Objective :*\n**```{str(item[0][3])}```**',
                                  colour=0xf20006)
            embed.set_footer(text='Next page in 10 seconds')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

            await asyncio.sleep(10)

            if int(jail_number) >= int(item[0][9]):
                # win
                experience = int(game[2]) + int(item[0][5])
                level = int(game[1])
                if int(experience) >= 100:
                    experience = 0
                    level = int(game[1]) + 1
                money = int(game[4]) + int(item[0][4])
                jail = 'FALSE'
                jail_date = '0'
                score = int(game[3]) + int(item[0][6])
                query = "UPDATE botzilla.c_user SET XP = {}, score = {}, LVL {}, money = {}, jail = {}, jail_date = {} WHERE ID = '{}'".format(experience, score, level, money, jail, jail_date, ctx.message.author.id)
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                embed = discord.Embed(title='{}:'.format(item[0][2]),
                                      description=f'**```{str(item[0][6])}```**',
                                      colour=0xf20006)
                await self.bot.edit_message(a, embed=embed)
            else:
                # lose
                jail = 'TRUE'
                jail_date = f'{datetime.datetime.now()}'
                query = f"INSERT INTO botzilla.c_user(jail, jail_date) VALUES({jail}, {jail_date})"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                t = time_to_wait(self, datetime.datetime.now())
                embed = discord.Embed(title='{}:'.format(str(item[0][2])),
                                      description=f'**```{str(item[0][7])}```**\nTime to wait {t}',
                                      colour=0xf20006)
                await self.bot.edit_message(a, embed=embed)


        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You could find nothing to steal..\nYou decide to take a walk and observe the erea.',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\U0001f6b6')
            return



def setup(bot):
    bot.add_cog(TestScripts(bot))
