import json
import discord
from discord.ext import commands
import asyncio
import random

import datetime


try:
    from plugin.database import Database
except:
    pass

class CriminalWars:
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
    async def criminal(self, ctx, player : discord.Member = None):
        """
        Shows your criminal record. No worry...
        It is just a discord game. Look into !!help for more information.

        Alias = !!cr
        Usage:
            - !!criminals
                *Shows information about you*
            - !!criminals <discord player>
                *Shows information about a person*
        Example:
            - !!cr puffdip
                *Shows information about puffdip*
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!criminal <{player}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        await self.bot.send_typing(ctx.message.channel)

        def check_profile(self, ID):
            self.database.cur.execute(f"select * from cr.c_user where ID = '{ID}';")
            profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if profile is None:
                query = f"INSERT INTO cr.c_user(ID, LVL, XP, score, money, city, protected) VALUES({ID}, {int(1)}, {int(0)}, {int(0)}, {int(500)}, 'New York', 'TRUE')"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} created a criminal profile')
            else:
                pass

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
                              description='\t',
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

    @commands.cooldown(rate=1, per=10, type=commands.BucketType.user)
    @commands.command(pass_context=True)
    async def steal(self, ctx, item = None):
        """
        Steal something,.. Really depends on the city.
        Lets say you are in Amsterdam and you really need a bike.
        [!!steal bike], would solve your problem
        To get a more compact overview of things you can steal..
        Use [!!steal]. This will bring up a list with more detailed
        information about the different crimes. Choose one and do not get caught.

        Usage:
            - !!steal
                *List of items you can steal*
            - !!steal <item>
                *steal the prefered item*
        Example:
            - !!steal candy
                *steals candy in New York*
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!steal <{item}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        await self.bot.send_typing(ctx.message.channel)

        def check_profile(self, ID):
            self.database.cur.execute(f"select * from cr.c_user where ID = '{ID}';")
            profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if profile is None:
                query = f"INSERT INTO cr.c_user(ID, LVL, XP, score, money, city, protected) VALUES({ID}, {int(1)}, {int(0)}, {int(0)}, {int(500)}, 'New York', 'TRUE')"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} created a criminal profile')
            else:
                pass

        def jail_time(self, future, where):
            """
            need time from database to calculate if user is in jail
            true if in jail and returns remaining time
            false if not in jail
            """
            now = datetime.datetime.now()
            future = datetime.datetime.strptime(future, '%Y-%m-%d %H:%M:%S')
            if now >= future:
                self.database.cur.execute(f"delete from cr.{where} where ID = {ctx.message.author.id};")
                self.database.cur.execute("ROLLBACK;")
                return False
            else:
                return True

        def time_calc(self, what):
            self.database.cur.execute(f"select * from cr.{what} WHERE ID = {ctx.message.author.id};")
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

        def level(self, ID):
            self.database.cur.execute(f"select * from cr.c_user WHERE ID = {ctx.message.author.id};")
            user_level = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute(f"select * from cr.c_steal WHERE ID = {ID};")
            item = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

            item_level = int(item[10])
            user_level = int(user_level[1])
            if user_level >= item_level:
                return False
            else:
                return True

        check_profile(self, ctx.message.author.id)

        arg_check = item
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

        self.database.cur.execute(f"select * from cr.c_travel WHERE ID = {ctx.message.author.id};")
        travel = self.database.cur.fetchone()
        self.database.cur.execute("ROLLBACK;")

        if arg_check is None:
            self.database.cur.execute(f"select * from cr.c_steal WHERE city = '{user[5]}';")
            actions = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            b = []
            for i in actions:
                d = f'- **`Lvl.{i[10]}`** : **`{i[1]}`**'
                b.append(d)
            c = "\n".join(b)
            embed = discord.Embed(title='Unable to move',
                                  description=f'Your current location is: **`{user[5]}`**\nThe following things are your point of interest\n\n**Steal**\n{c}',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            return
        else:
            self.database.cur.execute(f"select name_item from cr.c_steal WHERE city = '{user[5]}';")
            actions = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            print(actions)
            if str(arg_check) not in str(actions):
                print('test')
                b = []
                for i in actions:
                    d = f'- **`Lvl.{i[10]}`** : **`{i[1]}`**'
                    b.append(d)
                c = "\n".join(b)
                embed = discord.Embed(title='Unable to move',
                                      description=f'Not able to steal: **`{arg_check}`**\nYour current location is: **`{user[5]}`**\nThe following things are your point of interest\n\n**Steal**\n{c}',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return

        if jail:
            if jail_time(self, jail[1], 'c_jail'):
                time_to_wait = time_calc(self, 'c_jail')
                embed = discord.Embed(title='Unable to move',
                                      description=f'You are unable to **{item[0][2]}**\nThis is because you are in **jail**.\nThe judge decided to lock you up until:\n**```py\n{jail[1]}\n```**\nIn **`{time_to_wait}`** you will be released.\nTry again in that time.',
                                      colour=0xf20006)
                embed.set_thumbnail(url='https://media.discordapp.net/attachments/407238426417430539/418754296780161024/power-of-family.png')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return
        else:
            pass

        if travel:
            if jail_time(self, travel[1], 'c_travel'):
                time_to_wait = time_calc(self, 'c_travel')
                embed = discord.Embed(title='Unable to move',
                                      description=f'You are on a plane to **`{travel[2]}`**.\nYou took a look at your planning schedule.\nAriving date:**```py\n{travel[1]}\n```**\nYou will arive in **`{time_to_wait}`**\nTry again in that time.',
                                      colour=0xf20006)
                embed.set_thumbnail(url='https://media.discordapp.net/attachments/407238426417430539/418839121348526091/surprising-airplane-facts-plane-crashes.png')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return
        else:
            pass

        test_level = level(self, int(item[0][0]))

        if test_level:
            self.database.cur.execute(f"select * from cr.c_steal WHERE ID = {int(item[0][0])};")
            item = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            desc = f'Your level is way too low. Please do a few "lower level crime" missions\nCurrent level: **`{user[1]}`**\nRequired for **`{item[1]}`** **`Lvl.{item[10]}`**'
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=desc,
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        if user_choice in str(item):
            if right_city(self, item[0][0]):
                embed = discord.Embed(title='{}:'.format(item[0][2]),
                                      description=f'You are not in the right city\nTravel to **`{item[0][12]}`** to **`{item[0][2]}`**\nYou can check out **`{self.config["prefix"]}`city** for more information',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return

            # Game itself

            jail_number = random.randint(0, 100)

            embed = discord.Embed(title='{}:'.format(item[0][2]),
                                  description=f'**Objective :**\n**```{str(item[0][3])}```**',
                                  colour=0xf20006)
            embed.set_thumbnail(url='https://media.discordapp.net/attachments/407238426417430539/418769190762315786/burglar-thief-costume-em3190--3119-pekm299x464ekm.jpg.png')
            embed.set_footer(text='Crime in 10 seconds')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

            await asyncio.sleep(10)
            if int(jail_number) >= int(item[0][11]):
                # win
                up = ':arrow_up_small:'
                experience = int(user[2]) + int(item[0][5])
                level = int(user[1])
                print_level = f':ok: LVL *`({level})`* ***-***'
                if int(experience) >= 100:
                    experience = 0
                    level = int(user[1]) + 1
                    print_level = f'{up} LVL *`({user[1]})`* ***+*** **1**'

                money = int(user[4]) + int(item[0][4])
                score = int(user[3]) + int(item[0][6])
                query = "UPDATE cr.c_user SET XP = {}, score = {}, LVL = {}, money = {} WHERE ID = '{}'".format(experience, score, level, money, ctx.message.author.id)
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")

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

                time_to_wait = time_calc(self, 'c_jail')

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
    async def city(self, ctx, *, city : str = None):
        """
        Shows information about a city.
        Default city is the city you are located in
        Citys currently in game:
        <New York>, <Amsterdam>

        Usage:
            - !!city
                *Shows current city info*
            - !!city <city>
                *shows info about a city*
        Example:
            - !!city Amsterdam
                *Shows city info Amsterdam*
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!city <{city}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        await self.bot.send_typing(ctx.message.channel)

        def check_profile(self, ID):
            self.database.cur.execute(f"select * from cr.c_user where ID = '{ID}';")
            profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if profile is None:
                query = f"INSERT INTO cr.c_user(ID, LVL, XP, score, money, city, protected) VALUES({ID}, {int(1)}, {int(0)}, {int(0)}, {int(500)}, 'New York', 'TRUE')"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} created a criminal profile')
            else:
                pass

        check_profile(self, ctx.message.author.id)

        if city is None:
            self.database.cur.execute(f"select city from cr.c_user where ID = {ctx.message.author.id};")
            user = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            city = user[0]
            self.database.cur.execute(f"select * from cr.c_steal where city = '{city}';")
            steal = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute(f"select * from cr.c_city where city = '{city}';")
            city = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            empty = []
            if steal == empty:
                steal_list = '- **`None`**'
            else:
                things_to_steal = []
                for i in steal:
                    things_to_steal.append(f'- **`{i[1]}`** : **`{i[11]}`** % fail rate')
                steal_list = '\n'.join(things_to_steal)

            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=f'The current city you are in is **`{city[1]}`**\n\n**```{city[2]}```**\n\n',
                                  colour=0xf20006)
            embed.add_field(name='This city offers the following:', value='-------------------------------', inline=False)
            embed.add_field(name='Items to steal', value=steal_list)

            embed.set_thumbnail(url=city[3])
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

        else:
            # search info about other city
            if ' ' in str(city):
                a = str(city).split(' ')
                c = []
                for i in a:
                    c.append(i.lower().capitalize())
                city = ' '.join(c)
            else:
                city = str(city).lower().capitalize()

            self.database.cur.execute(f"select city from cr.c_city;")
            city_check = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")

            if str(city) not in str(city_check):
                city_names = []
                for i in city_check:
                    city_names.append(f'- **`{i[0]}`**')
                avalaible_citys = '\n'.join(city_names)
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'Unfortunately **`{city}`** is not a location in the game.\n\nThe following locations are accesable:\n\n{avalaible_citys}',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return

            self.database.cur.execute(f"select * from cr.c_city where city = '{city}';")
            cityq = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

            self.database.cur.execute(f"select * from cr.c_steal where city = '{city}';")
            steal = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")

            empty = []
            if steal == empty:
                steal_list = '- **`None`**'
            else:
                things_to_steal = []
                for i in steal:
                    things_to_steal.append(f'- **`{i[1]}`** : **`{i[11]}`** % fail rate')
                steal_list = '\n'.join(things_to_steal)

            seconds = int(cityq[4])
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            average = f"{h}:{m}:{s}"
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=f'The city you selected is **`{cityq[1]}`**\nTravel time is average: **`{average}`** \n\n**```{cityq[2]}```**\n\n',
                                  colour=0xf20006)
            embed.add_field(name='This city offers the following:', value='-------------------------------', inline=False)
            embed.add_field(name='Items to steal', value=steal_list)

            embed.set_thumbnail(url=cityq[3])
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def travel(self, ctx, *, city : str = None):
        """
        Travel to another city. Time is expressed in [hh:mm:ss]
        Use !!travel for information about any flight to any city.
        If you found a flight that sounds interesting, for example Amsterdam.
        Use [!!travel amsterdam] to travel to Amsterdam!

        Usage:
            - !!travel
                *Shows information about locations even as prices*
            - !!travel <location>
                *Travel to the destination*
        Example:
            - !!travel Amsterdam
                *Travels to Amsterdam*
        """

        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!travel <{city}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        await self.bot.send_typing(ctx.message.channel)

        def check_profile(self, ID):
            self.database.cur.execute(f"select * from cr.c_user where ID = '{ID}';")
            profile = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            if profile is None:
                query = f"INSERT INTO cr.c_user(ID, LVL, XP, score, money, city, protected) VALUES({ID}, {int(1)}, {int(0)}, {int(0)}, {int(500)}, 'New York', 'TRUE')"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} created a criminal profile')
            else:
                pass

        def jail_time(self, future, where):
            """
            need time from database to calculate if user is in jail
            true if in jail and returns remaining time
            false if not in jail
            """
            now = datetime.datetime.now()
            future = datetime.datetime.strptime(future, '%Y-%m-%d %H:%M:%S')
            if now >= future:
                self.database.cur.execute(f"delete from cr.{where} where ID = {ctx.message.author.id};")
                self.database.cur.execute("ROLLBACK;")
                return False
            else:
                return True

        def time_calc(self, what):
            self.database.cur.execute(f"select * from cr.{what} WHERE ID = {ctx.message.author.id};")
            jail = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            now = datetime.datetime.now()
            future = datetime.datetime.strptime(jail[1], '%Y-%m-%d %H:%M:%S')
            time_to_wait = future - now
            time_to_wait = str(time_to_wait)[:8].replace('.', '')
            return time_to_wait

        check_profile(self, ctx.message.author.id)

        self.database.cur.execute(f"select * from cr.c_travel WHERE ID = {ctx.message.author.id};")
        travel = self.database.cur.fetchone()
        self.database.cur.execute("ROLLBACK;")


        self.database.cur.execute(f"select * from cr.c_jail WHERE ID = {ctx.message.author.id};")
        jail = self.database.cur.fetchone()
        self.database.cur.execute("ROLLBACK;")

        if jail:
            if jail_time(self, jail[1], 'c_jail'):
                time_to_wait = time_calc(self, 'c_jail')
                embed = discord.Embed(title='Unable to move',
                                      description=f'You are unable to travel\nThis is because you are in **jail**.\nThe judge decided to lock you up until:\n**```py\n{jail[1]}\n```**\nIn **`{time_to_wait}`** you will be released.\nTry again in that time.',
                                      colour=0xf20006)
                embed.set_thumbnail(url='https://media.discordapp.net/attachments/407238426417430539/418754296780161024/power-of-family.png')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return
        else:
            pass

        if travel:
            if jail_time(self, travel[1], 'c_travel'):
                time_to_wait = time_calc(self, 'c_travel')
                embed = discord.Embed(title='Unable to move',
                                      description=f'You are on a plane to **`{travel[2]}`**.\nYou took a look at your planning schedule.\nAriving date:**```py\n{travel[1]}\n```**\nYou will arive in **`{time_to_wait}`**\nTry again in that time.',
                                      colour=0xf20006)
                embed.set_thumbnail(url='https://media.discordapp.net/attachments/407238426417430539/418839121348526091/surprising-airplane-facts-plane-crashes.png')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return
        else:
            pass

        if city is None:
            self.database.cur.execute(f"select * from cr.c_city;")
            city_check = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")

            self.database.cur.execute(f"select * from cr.c_user WHERE ID = {ctx.message.author.id};")
            user = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

            city_names = []
            for i in city_check:
                seconds = int(i[4])
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                average = f"{h}:{m}:{s}"
                if user[5] == i[1]:
                    pass
                else:
                    city_names.append(f'- $**`{i[5]}`**,- : **`{i[1]}`**\n  *Travel time average: `{average}`*\n')
            avalaible_citys = '\n'.join(city_names)
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=f'Current location: **`{user[5]}`**\nYou can travel to the following locations in game:\n\n{avalaible_citys}\n\nIf you are stuck use **`{self.config["prefix"]}help travel`** for more information',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            return
        else:
            # search info about other city
            if ' ' in str(city):
                a = str(city).split(' ')
                c = []
                for i in a:
                    c.append(i.lower().capitalize())
                city = ' '.join(c)
            else:
                city = str(city).lower().capitalize()

            self.database.cur.execute(f"select city from cr.c_city;")
            city_check = self.database.cur.fetchall()
            self.database.cur.execute("ROLLBACK;")

            if str(city) not in str(city_check):
                city_names = []
                for i in city_check:
                    city_names.append(f'- **`{i[0]}`**')
                avalaible_citys = '\n'.join(city_names)
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'Unfortunately **`{city}`** is not a location in the game.\n\nThe following locations are accesable:\n\n{avalaible_citys}',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return

            self.database.cur.execute(f"select * from cr.c_city where city = '{city}';")
            city = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

            self.database.cur.execute(f"select * from cr.c_user where ID = {ctx.message.author.id};")
            user = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

            if city[1] == user[5]:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'If you know you absolutely cannot travel to the same location as where you are.\nYou are currently in **`{city[1]}`**\nIf you are lost, use **`{self.config["prefix"]}help city`** for more information',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return

            if int(city[5]) >= int(user[4]):
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'Unfortunately **`{city[1]}`** is to expensive for you\nMake sure your belance is enough for the plane ticket you need.\nThe plane ticket itself costs $**`{city[5]}`**\n\nCurrent balance: $**`{user[4]}`**',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                return

            jt = datetime.datetime.now() + datetime.timedelta(0, int(city[4]))
            jt = jt.strftime('%Y-%m-%d %H:%M:%S')
            try:
                query = f"INSERT INTO cr.c_travel(ID, travel_date, travel) VALUES({ctx.message.author.id}, '{jt}', '{city[1]}');"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                money = int(user[4]) - int(city[5])
                query = f"UPDATE cr.c_user SET city = '{city[1]}', money = {money} WHERE ID = {ctx.message.author.id};"
                self.database.cur.execute(query)
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
            except Exception as e:
                if 'duplicate key' in str(e.args):
                    pass
                else:
                    print(f'{type(e).__name__} : {e}')

            self.database.cur.execute(f"select * from cr.c_user where ID = {ctx.message.author.id};")
            user_n = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            time_to_wait = time_calc(self, 'c_travel')

            embed = discord.Embed(title='Flying to: '.format(city[1]),
                                  description=f'You took the airplane to **`{city[1]}`**\n:moneybag: $$ **`{user_n[4]}`** = **`{user[4]}`**( ***-*** **`{city[5]}`**)\nTime in plane: **`{time_to_wait}`**',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])

def setup(bot):
    bot.add_cog(CriminalWars(bot))