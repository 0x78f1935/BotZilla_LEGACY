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
            self.database.cur.execute(f"select * from cr.c_user where ID = '{ID}';")
            profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if profile is None:
                print('profile not found')
                query = f"INSERT INTO cr.c_user(ID, LVL, XP, score, money, city, protected) VALUES({ID}, {int(0)}, {int(0)}, {int(0)}, {int(500)}, 'New York', 'TRUE')"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                print('profile created')
            else:
                print('profile already exist')

        if player:
            # mpplayer found
            check_profile(self, player.id)
            self.database.cur.execute(f"select * from cr.c_user where ID = '{player.id}';")
            player_profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

        else:
            # player found
            check_profile(self, ctx.message.author.id)
            self.database.cur.execute(f"select * from cr.c_user where ID = '{ctx.message.author.id}';")
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
            embed.add_field(name='Protected', value='**`{}`**'.format(player_profile[6]), inline=True)

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
            self.database.cur.execute(f"select * from cr.c_user where ID = '{ID}';")
            profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if profile is None:
                print('profile not found')
                query = f"INSERT INTO cr.c_user(ID, LVL, XP, score, money, city, protected) VALUES({ID}, {int(0)}, {int(0)}, {int(0)}, {int(500)}, 'New York', 'TRUE')"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                print('profile created')
            else:
                print('profile already exist')

        def jail_time(self, future):
            """
            need time from database to calculate if user is in jail
            true if in jail and returns remaining time
            false if not in jail
            """
            print(future)
            now = datetime.datetime.now()
            future = datetime.datetime.strptime(future, '%Y-%m-%d %H:%M:%S')
            print(now)
            if now >= future:
                self.database.cur.execute(f"delete from cr.c_jail where ID = {ctx.message.author.id};")
                self.database.cur.execute("ROLLBACK;")
                return False
            else:
                return True

        def jail_time_calc(self):
            self.database.cur.execute(f"select * from cr.c_jail WHERE ID = {ctx.message.author.id};")
            jail = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            now = datetime.datetime.now()
            future = datetime.datetime.strptime(jail[1], '%Y-%m-%d %H:%M:%S')
            time_to_wait = future - now
            time_to_wait = str(time_to_wait)[:8].replace('.', '')
            return time_to_wait

        def right_city(self, item_id):
            # if not in same city return true
            self.database.cur.execute(f"select city from cr.c_user WHERE ID = {ctx.message.author.id};")
            user = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute(f"select city from cr.c_steal WHERE ID = {item_id};")
            item = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if str(item) == str(user):
                return False
            else:
                return True

        check_profile(self, ctx.message.author.id)

        user_choice = str(item).lower()
        self.database.cur.execute(f"select * from cr.c_steal where name_item = '{user_choice}';")
        item = self.database.cur.fetchall()
        self.database.cur.execute("ROLLBACK;")

        self.database.cur.execute(f"select * from cr.c_user where ID = {ctx.message.author.id};")
        user = self.database.cur.fetchone()
        self.database.cur.execute("ROLLBACK;")

        self.database.cur.execute(f"select * from cr.c_jail WHERE ID = {ctx.message.author.id};")
        jail = self.database.cur.fetchone()
        self.database.cur.execute("ROLLBACK;")

        if jail:
            if jail_time(self, jail[1]):
                time_to_wait = jail_time_calc(self)
                embed = discord.Embed(title='Unable to move',
                                      description=f'You are unable to **{item[0][2]}**\nThis is because you are in **jail**.\nThe judge decided to lock you up until:\n**```py\n{jail[1]}\n```**\nIn **`{time_to_wait}`** you will be released.\nTry again in that time.',
                                      colour=0xf20006)
                embed.set_thumbnail(url='https://media.discordapp.net/attachments/407238426417430539/418754296780161024/power-of-family.png')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return
        else:
            pass

        # Game itself
        if user_choice in str(item):
            if right_city(self, item[0][0]):
                embed = discord.Embed(title='{}:'.format(item[0][2]),
                                      description=f'You are not in the right city\nTravel to **`{item[0][12]}`** to **`{item[0][2]}`**\nYou can check out **`{self.config["prefix"]}`city** for more information',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return

            jail_number = random.randint(0, 100)

            embed = discord.Embed(title='{}:'.format(item[0][2]),
                                  description=f'**Objective :**\n**```{str(item[0][3])}```**',
                                  colour=0xf20006)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/407238426417430539/418769190762315786/burglar-thief-costume-em3190--3119-pekm299x464ekm.jpg.png')
            embed.set_footer(text='Crime in 10 seconds')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

            await asyncio.sleep(10)
            print(int(jail_number), int(item[0][11]))
            if int(jail_number) >= int(item[0][11]):
                # win
                up = ':arrow_up_small:'
                experience = int(user[2]) + int(item[0][5])
                print(f'xp: {experience}')
                level = int(user[1])
                print_level = f':ok: LVL *`({level})`* ***-***'
                print(f'lvl: {level}')
                if int(experience) >= 100:
                    experience = 0
                    level = int(user[1]) + 1
                    print_level = f'{up} LVL *`({user[1]})`* ***+*** **1**'
                print(f'xp: {experience}')
                print(f'lvl: {level}')
                money = int(user[4]) + int(item[0][4])
                print(f'money: {money}')

                score = int(user[3]) + int(item[0][6])
                print(f'score: {score}')
                query = "UPDATE cr.c_user SET XP = {}, score = {}, LVL = {}, money = {} WHERE ID = '{}'".format(experience, score, level, money, ctx.message.author.id)
                print(query)
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                print('query done')

                embed = discord.Embed(title='{}:'.format(item[0][2]),
                                      description=f'**Objective :**\n**```{item[0][3]}```**\n{up} XP *`({user[2]})`* ***+*** **{item[0][5]}**\n{print_level}\n:moneybag: $$$ *`({user[4]})`* ***+*** *`{item[0][4]}`*\n{up} SCORE *`({user[3]})`* ***+*** *`{item[0][6]}`* **```{item[0][7]}```**',
                                      colour=0xf20006)
                embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/407238426417430539/418770188045910026/18568092-successful-thief-Stock-Vector.png')
                await self.bot.edit_message(a, embed=embed)
            else:
                # lose
                jt = datetime.datetime.now() + datetime.timedelta(0, int(item[0][9]))
                jt = str(jt.strftime('%Y-%m-%d %H:%M:%S'))
                try:
                    query = f"INSERT INTO cr.c_jail(ID, jail_date) VALUES({ctx.message.author.id}, '{jt}');"
                    self.database.cur.execute(query)
                    self.database.conn.commit()
                    self.database.cur.execute("ROLLBACK;")

                except Exception as e:
                    if 'duplicate key' in str(e.args):
                        pass
                    else:
                        print(f'{type(e).__name__} : {e}')

                time_to_wait = jail_time_calc(self)

                embed = discord.Embed(title='{}:'.format(item[0][2]),
                                      description=f'**Objective :**\n**```{str(item[0][3])}```**\n:police_car::oncoming_police_car::police_car::oncoming_police_car::police_car::oncoming_police_car::police_car::oncoming_police_car::police_car::oncoming_police_car::police_car::oncoming_police_car::police_car::oncoming_police_car::police_car::oncoming_police_car:\n**```{item[0][8]}```**\nTime in jail: **`{time_to_wait}`**',
                                      colour=0xf20006)
                embed.set_thumbnail(url='https://media.discordapp.net/attachments/407238426417430539/418754296780161024/power-of-family.png')
                await self.bot.edit_message(a, embed=embed)
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You could find nothing to steal..\nYou decide to take a walk and observe the area.\nUse **`{}help steal`** if you are stuck',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\U0001f6b6')
            return


    @commands.command(pass_context=True)
    async def city(self, ctx, city=None):
        """
        Shows information about a city.
        Default city is the city you are located in
        Citys currently in game:
        <New York>, <Amsterdam>

        Usage:
            - !!city
        Or:
            - !!city Amsterdam
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!city <{city}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        def check_profile(self, ID):
            self.database.cur.execute(f"select * from cr.c_user where ID = '{ID}';")
            profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if profile is None:
                print('profile not found')
                query = f"INSERT INTO cr.c_user(ID, LVL, XP, score, money, city, protected) VALUES({ID}, {int(0)}, {int(0)}, {int(0)}, {int(500)}, 'New York', 'TRUE')"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                print('profile created')
            else:
                print('profile already exist')

        check_profile(self, ctx.message.author.id)

        if city is None:
            self.database.cur.execute(f"select city from cr.c_user where ID = {ctx.message.author.id};")
            user = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            city = user[0]
            self.database.cur.execute(f"select name_item from cr.c_steal where city = '{city}';")
            steal = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute(f"select * from cr.c_city where city = '{city}';")
            city = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            things_to_steal = []
            for i in steal:
                things_to_steal.append(f'- **`{i[0]}`**')
            steal_list = '\n'.join(things_to_steal)
            print(city)
            print(city[1])
            print(city[2])
            print(city[3])
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=f'The current city you are in is **`{city[1]}`**\n\n{city[2]}This city offers the following:\n\n**Items to steal**\n{steal_list}',
                                  colour=0xf20006)
            embed.set_thumbnail(url=city[3])
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])

        else:
            # search info about other city
            pass


def setup(bot):
    bot.add_cog(TestScripts(bot))
