from discord.ext import commands
import json
import discord
import traceback
import psycopg2
import csv


class Database:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']
        self.database_settings = self.tmp_config['database']
        self.database_online = False
        self.database_export_location_users = './export/DBE_users.csv'
        self.database_import_location_users = './import/DBE_users.csv'

        debounce = False
        reconnect_db_times = int(self.database_settings['reconnect_trys'])
        while True:
            if not debounce:
                debounce = True
                try:
                    self.conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port='{}' password={}".format(
                        self.database_settings['db_name'],
                        self.database_settings['user'],
                        self.database_settings['ip'],
                        self.database_settings['port'],
                        self.database_settings['password']
                    ))
                    self.cur = self.conn.cursor()
                    print('Established Database connection with:')
                    print("dbname={}\nhost={}\nport={}".format(
                        self.database_settings['db_name'],
                        self.database_settings['ip'],
                        self.database_settings['port']
                    ))
                    self.database_online = True
                    break
                except:
                    print('I am unable to connect to the Database')
                    debounce = False
                reconnect_db_times -= 1
                if reconnect_db_times <= 0:
                    print('failed to connect with the database giving up...')
                    break


    @commands.command(pass_context=True)
    async def sql(self, ctx, *, query: str = None):
        """
        Acces database and run a query.
        use a query psql based.
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        if not self.database_online:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Could not connect to database.',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        if query is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You should know what you are doing.\n Especially with this command! :angry:',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        try:
            self.cur.execute('{}'.format(str(query)))
            result_cur = self.cur.fetchall()
            if not result_cur:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='No data found :cry:',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                return

            embed = discord.Embed(title='{}:'.format('SQL Succes'),
                                  description='```sql\n{}```'.format(result_cur),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        except psycopg2.Error as e:
            if e.pgerror is None:
                embed = discord.Embed(title='{}:'.format('SQL Succes'),
                                      description='```sql\n{}```'.format(str(query)),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                return
            embed = discord.Embed(title='{}:'.format('SQL Error'),
                                  description='```sql\n{}```\nROLLBACK query:\n```sql\n{}```'.format(e.pgerror, 'ROLLBACK;'),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


    @commands.command(pass_context=True, hidden=True)
    async def get_users(self, ctx):
        """
        Update datebase with current active users
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        if not self.database_online:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Could not connect to database.',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        data_members = {"id" : "name"}
        for server in self.bot.servers:
            for member in server.members:
                data_members.update({member.id:member.name})

        self.cur.execute('ROLLBACK;')
        for id_members, name_members in data_members.items():
            try:
                self.cur.execute('INSERT INTO botzilla.users (ID, name, date_added) VALUES ({}, \'{}\', {});'.format(
                    id_members, str(name_members), 'current_timestamp'))
            except Exception as e:
                print('Error gathering info user:\n{}'.format(e.args))
                continue
        print("Done with gathering user info")


    @commands.command(pass_context=True)
    async def dbexport(self, ctx):
        """
        Export database data to export folder
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return


        if not self.database_online:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Could not connect to database.',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return


        self.cur.execute("SELECT * from botzilla.users;")
        rows = self.cur.fetchall()
        with open(self.database_export_location_users, 'w') as output:
            writer = csv.writer(output, lineterminator='\n')
            for val in rows:
                writer.writerow([val])


    @commands.command(pass_context=True)
    async def dbimport(self, ctx):
        """
        Import CSV data from import folder
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return


        if not self.database_online:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Could not connect to database.',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return


        with open(self.database_import_location_users, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                self.cur.execute("INSERT INTO botzilla.users (ID, name, date_added) VALUES {}".format(row))


def setup(bot):
    bot.add_cog(Database(bot))