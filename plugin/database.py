from discord.ext import commands
import json
import discord
import traceback
import psycopg2
import csv
import re
from io import BytesIO
from discord.errors import HTTPException
from options.utils import chat_formatting, dataIO, downloader
from collections import defaultdict


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
        self.database_export_location_music_channels = './export/DBE_music_channels.csv'
        self.database_import_location_music_channels = './import/DBE_music_channels.csv'
        self.database_export_musicque = './import/DBE_music_que.cxv'
        self.database_import_musicque = './import/DBE_music_que.cxv'
        self.client = discord.Client()
        self.music_channels = []
        self.downloader = downloader.Downloader()
        self.reconnect_db_times = int(self.database_settings['reconnect_trys'])

        for i in range(self.reconnect_db_times):
            print('Loading database')
            try:
                self.conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port='{}' password={}".format(
                    self.database_settings['db_name'],
                    self.database_settings['user'],
                    self.database_settings['ip'],
                    self.database_settings['port'],
                    self.database_settings['password']
                ))
                self.cur = self.conn.cursor()
                print('Established Database connection')
                self.cur.execute("select id from botzilla.music where type_channel = 'voice';")
                rows = self.cur.fetchall()
                for row in rows:
                    for item in row:
                        self.music_channels.append(item)
                self.database_online = True
                break
            except:
                print('I am unable to connect to the Database')
            print('failed to connect with the database giving up...')

        ## autoconnect to music channel
        # select id from botzilla.music where type_channel = 'voice';
        # prep for autojoin




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
                                  description='```sql\n{}```\nROLLBACK query:\n```sql\n{}sql ROLLBACK;```'.format(
                                      e.pgerror, self.config['prefix']),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
        except HTTPException as e:
            embed = discord.Embed(title='{}:'.format('Error'),
                                  description='Try to use `limit 10`. Output may be to big\n{}'.format(e.args),
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
                self.cur.execute('INSERT INTO botzilla.users (ID, name) VALUES ({}, \'{}\');'.format(
                    id_members, str(name_members)))
            except Exception as e:
                print('Error gathering info user:\n{}'.format(e.args))
                continue
        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Done with gathering user info!',
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, hidden=True)
    async def get_music(self, ctx):
        """
        Update datebase with current active music channels
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

        data_channels = []
        for server in self.bot.servers:
            for channel in server.channels:
                if 'music' in str(channel).lower():
                    channel_type = str(channel.type)
                    print(channel_type)
                    data = [int(channel.id), str(channel.name), re.sub('\W+', '', str(server.name)), str(channel.type)]
                    data_channels.append(data)


        self.cur.execute('ROLLBACK;')
        for items in data_channels:
            try:
                self.cur.execute(
                    'INSERT INTO botzilla.music (ID, channel_name, server_name, type_channel) VALUES ({}, \'{}\', \'{}\', \'{}\');'.format(
                        items[0], items[1], items[2], items[3]
                    ))
            except Exception as e:
                print('Error gathering info music channels:\n{}'.format(e.args))
                continue

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Done with gathering music channel info!',
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def pldumpdb(self, ctx, *, song_url):
        """
        Dumps the individual urls of a playlist
        into the database botzilla.musicque
        """
        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You may not use this command :angry: only admins!',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        try:
            info = await self.downloader.extract_info(self.loop, song_url.strip('<>'), download=False, process=False)
        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Could not extract info from input url\nError:\n```Python\n{}```\n'.format(e.args),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        if not info:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Could not extract info from input url, No data',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        if not info.get('entries', None):
            # TODO: Retarded playlist checking
            # set(url, webpageurl).difference(set(url))

            if info.get('url', None) != info.get('webpage_url', info.get('url', None)):
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='This does not seems to be a playlist\nI\'m confident you could use **`{}help pldump`** instead'.format(self.config['prefix']),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                return
            else:
                return await self.cmd_pldump(ctx.message.channel, info.get(''))

        linegens = defaultdict(lambda: None, **{
            "youtube":    lambda d: 'https://www.youtube.com/watch?v=%s' % d['id'],
            "soundcloud": lambda d: d['url'],
            "bandcamp":   lambda d: d['url']
        })

        exfunc = linegens[info['extractor'].split(':')[0]]

        if not exfunc:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Could not extract info from input url, unsupported playlist type.',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        with BytesIO() as fcontent:
            for item in info['entries']:
                fcontent.write(exfunc(item).encode('utf8') + b'\n')

            fcontent.seek(0)
            await self.bot.send_file(ctx.message.channel,
                                     fcontent,
                                     filename='playlist.txt',
                                     content="Here's the url dump for {}".format(song_url))

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description=':mailbox_with_mail:',
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


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

        try:
            self.cur.execute("SELECT * from botzilla.users;")
            rows = self.cur.fetchall()
            with open(self.database_export_location_users, 'w') as output:
                writer = csv.writer(output, lineterminator='\n')
                for val in rows:
                    writer.writerow([val])
        except Exception as e:
            embed = discord.Embed(title='{}:'.format('Error'),
                                  description='{}'.format(e.args),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


        try:
            self.cur.execute("SELECT * from botzilla.music;")
            rows = self.cur.fetchall()
            with open(self.database_export_location_music_channels, 'w') as output:
                writer = csv.writer(output, lineterminator='\n')
                for val in rows:
                    writer.writerow([val])
        except Exception as e:
            embed = discord.Embed(title='{}:'.format('Error'),
                                  description='{}'.format(e.args),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


        try:
            self.cur.execute("SELECT * from botzilla.musicque;")
            rows = self.cur.fetchall()
            with open(self.database_export_musicque, 'w') as output:
                writer = csv.writer(output, lineterminator='\n')
                for val in rows:
                    writer.writerow([val])
        except Exception as e:
            embed = discord.Embed(title='{}:'.format('Error'),
                                  description='{}'.format(e.args),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Done!',
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


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

        try:
            with open(self.database_import_location_users, 'r') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    row = str(row).replace('["', '')
                    row = str(row).replace('"]', '')
                    self.cur.execute("INSERT INTO botzilla.users (ID, name) VALUES {}".format(row))
        except Exception as e:
            embed = discord.Embed(title='{}:'.format('Error'),
                                  description='{}'.format(e.args),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


        try:
            with open(self.database_import_location_music_channels, 'r') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    row = str(row).replace('["', '')
                    row = str(row).replace('"]', '')
                    self.cur.execute("INSERT INTO botzilla.music (ID, channel_name, server_name, type_channel) VALUES {}".format(row))
        except Exception as e:
            embed = discord.Embed(title='{}:'.format('Error'),
                                  description='{}'.format(e.args),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


        try:
            with open(self.database_import_musicque, 'r') as file:
                reader = csv.reader(file, delimiter=',')
                for row in reader:
                    row = str(row).replace('["', '')
                    row = str(row).replace('"]', '')
                    self.cur.execute("INSERT INTO botzilla.musicque (url) VALUES {}".format(row))
        except Exception as e:
            embed = discord.Embed(title='{}:'.format('Error'),
                                  description='{}'.format(e.args),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Done!',
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Database(bot))