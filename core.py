# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
from discord.ext.commands import Bot
import platform
import json
from options.opus_loader import load_opus_lib
import re
import csv
import asyncio
from plugin.music import Music
import psycopg2

try:
    from plugin.database import Database
except:
    pass

load_opus_lib()

### Core

tmp_config = json.loads(str(open('options/config.js').read()))
config = tmp_config['config']
emojiUnicode = tmp_config['unicode']
exchange = tmp_config['exchange']
botzillaChannels = tmp_config['channels']
# The help command is currently set to be Direct Messaged.
# If you would like to change that, change "pm_help = True" to "pm_help = False" on line 9.
bot = Bot(description="BotZilla is built / maintained / self hosted by PuffDip\nUserdata may be stored for better experience.", command_prefix=config['prefix'], pm_help=False)
music_channels = botzillaChannels['music']
database_file_found = False
database_settings = tmp_config['database']

try:
    database = Database(bot)
    database_file_found = True
except:
    print('Core: Database files not found')
    pass


async def dbimport():
    """
    Import CSV data from import folder
    """

    # Users
    try:
        with open(database.database_import_location_users, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                try:
                    row = str(row).replace('["', '')
                    row = str(row).replace('"]', '')
                    database.cur.execute("INSERT INTO botzilla.users (ID, name) VALUES{};".format(row))
                    database.cur.execute("ROLLBACK;")
                except:
                    pass
    except Exception as e:
        pass


    #music channels
    try:
        with open(database.database_import_location_music_channels, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                try:
                    row = str(row).replace('["', '')
                    row = str(row).replace('"]', '')
                    database.cur.execute("INSERT INTO botzilla.music (ID, channel_name, server_name, type_channel) VALUES{};".format(row))
                    database.cur.execute("ROLLBACK;")
                except:
                    pass
    except Exception as e:
        pass

    try:
        with open(database.database_import_location_blacklist, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                try:
                    row = str(row).replace('["', '')
                    row = str(row).replace('"]', '')
                    print(row)
                    database.cur.execute("INSERT INTO botzilla.blacklist (ID, server_name, reason, total_votes) VALUES{};".format(row))
                    database.cur.execute("ROLLBACK;")
                except:
                    pass
    except Exception as e:
        pass

    # music urls
    try:
        with open(database.database_import_musicque, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                b = re.search(r'^(.*)', str(row)).group()
                b = b.replace('[', '')
                b = b.replace('"(', '')
                b = b.replace(',)"', '')
                row = b.replace(']', '')
                database.cur.execute("INSERT INTO botzilla.musicque(url) VALUES({});".format(row))
                database.cur.execute("ROLLBACK;")
    except Exception as e:
        pass

    # Blacklist
    try:
        database.cur.execute("SELECT ID from botzilla.blacklist;")
        rows = database.cur.fetchall()
        database.cur.execute("ROLLBACK;")
        for item in rows:
            item = str(item).replace('(', '')
            item = item.replace(',)', '')
            database.blacklist.append(item)
    except Exception as e:
        print(f'Can\'t find database{e.args}')


async def get_users():
    """
    Update datebase with current active users
    """
    data_members = {"id" : "name"}
    for server in bot.servers:
        for member in server.members:
            data_members.update({member.id:member.name})

    for id_members, name_members in data_members.items():
        try:
            database.cur.execute('INSERT INTO botzilla.users (ID, name) VALUES ({}, \'{}\');'.format(
                id_members, str(name_members)))
            database.cur.execute("ROLLBACK;")
        except Exception as e:
            print('Error gathering info user:\n{}'.format(e.args))


async def auto_join_channels(music_playlist):
    music = Music(bot)
    for server in bot.servers:
        for channel in server.channels:
            if 'music' in channel.name.lower():
                if str(channel.type) == 'voice':
                    print(f'item {channel.id} found, joining {channel.server.name} : {channel.name}')
                    if database_file_found:
                        if database.database_online:
                            await dbimport()
                            # channel = bot.get_channel(f'{channel.id}')
                            music.voice_states.update({channel : server.id})
                            await music.summon(channel)
                else:
                    pass


async def total_online_user_tracker():
    while True:
        game = discord.Game(name='Online users: {}'.format(sum(1 for m in set(bot.get_all_members()) if m.status != discord.Status.offline)), type=0)
        await bot.change_presence(game=game)
        await asyncio.sleep(3)


@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + ' (ID:' + bot.user.id + ') | Connected to ' + str(
        len(bot.servers)) + ' servers | Connected to ' + str(len(set(bot.get_all_members()))) + ' users')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
                                                                               platform.python_version()))
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('--------')

    #plugins

    plugins = (
        "admin",
        "exchange",
        "database",
        "fun",
        "music",
        "games",
        "gamestats",
        "information",
        "python_code_in_dc",
        "test"
    )

    # load plugins
    for p in plugins:
        bot.load_extension("plugin.{}".format(p))

    # get playlist
    global music_playlist
    music_playlist = []
    if database_file_found:
        if database.database_online:
            await dbimport()
            database.cur.execute('select * from botzilla.musicque;')
            rows = database.cur.fetchall()
            database.cur.execute("ROLLBACK;")
            rows = str(rows).replace('[(\'', '')
            rows = rows.replace(',)', '')
            rows = rows.replace('(', '')
            rows = rows.replace('\'', '')
            links = rows.replace(' ', '')
            clean_links = links.split(',')
            for item in clean_links:
                music_playlist.append(item)

    # await auto_join_channels(music_playlist)

    database.conn = psycopg2.connect("dbname='{}' user='{}' host='{}' port='{}' password={}".format(
        database_settings['db_name'],
        database_settings['user'],
        database_settings['ip'],
        database_settings['port'],
        database_settings['password']
    ))

    await total_online_user_tracker()


# @bot.event
# async def on_message_delete(message):
#     fmt = '**{0.author.server}** | ***{0.author.name}*** has deleted the message:\n{0.content}'
#     for owners in config['owner-id']:
#         owner = await bot.get_user_info(owners)
#         await bot.send_message(owner, fmt.format(message))


@bot.event
async def on_message(message):
    if message.author.bot: return

    database.cur.execute("SELECT ID FROM botzilla.blacklist;")
    row = database.cur.fetchall()
    row = str(row).replace('[(', '')
    row = row.replace(',)]', '')
    database.cur.execute("ROLLBACK;")
    if str(message.author.id) in row:
        if str(message.content).startswith('{}'.format(config['prefix'])):
            database.cur.execute("SELECT reason FROM botzilla.blacklist where ID = {};".format(message.author.id))
            reason = database.cur.fetchall()
            database.cur.execute("ROLLBACK;")
            reason = str(reason).replace("[('", '')
            reason = reason.replace("',)]", '')

            database.cur.execute("SELECT total_votes FROM botzilla.blacklist where ID = {};".format(message.author.id))
            votes = database.cur.fetchall()
            database.cur.execute("ROLLBACK;")
            votes = str(votes).replace('[(', '')
            votes = votes.replace(',)]', '')

            embed = discord.Embed(title='{}:'.format(message.author.name),
                                  description='You have been blacklisted with **`{}`** votes,\n\nReason:\n```{}```'.format(votes, reason),
                                  colour=0xf20006)
            last_message = await bot.send_message(message.channel, embed=embed)
            await bot.add_reaction(last_message, emojiUnicode['warning'])
            return
        else:
            return


    if 'shit' in str(message.content).lower():
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'shit', total = (total+1) where name = 'shit';")
        database.cur.execute("ROLLBACK;")

    if 'fuck' in str(message.content).lower():
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'fuck', total = (total+1) where name = 'fuck';")
        database.cur.execute("ROLLBACK;")

    if 'damn' in str(message.content).lower():
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'damn', total = (total+1) where name = 'damn';")
        database.cur.execute("ROLLBACK;")

    if 'bitch' in str(message.content).lower():
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'bitch', total = (total+1) where name = 'bitch';")
        database.cur.execute("ROLLBACK;")

    if 'crap' in str(message.content).lower():
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'crap', total = (total+1) where name = 'crap';")
        database.cur.execute("ROLLBACK;")

    if 'pussy' in str(message.content).lower():
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'pussy', total = (total+1) where name = 'pussy';")
        database.cur.execute("ROLLBACK;")

    if 'asshole' in str(message.content).lower():
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'asshole', total = (total+1) where name = 'asshole';")
        database.cur.execute("ROLLBACK;")

    if 'fag' in str(message.content).lower():
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'fag', total = (total+1) where name = 'fag';")
        database.cur.execute("ROLLBACK;")

    if 'gay' in str(message.content).lower():
        database.cur.execute("UPDATE botzilla.swearwords SET swearword = 'gay', total = (total+1) where name = 'gay';")
        database.cur.execute("ROLLBACK;")


    # comment out if you like to use let me google that for u
    # try:
    #     if 'how' in message.content.lower():
    #         search_term = re.search(r'\bhow\b.*[?]', message.content.lower()).group(0)
    #         search_term = uriquote(search_term)
    #         embed = discord.Embed(title='{}:'.format(message.author.name),
    #                               description='{}'.format('http://lmgtfy.com/?q={}'.format(search_term)),
    #                               colour=0xf20006)
    #         last_message = await bot.send_message(message.channel, embed=embed)
    #         await bot.add_reaction(last_message, emojiUnicode['succes'])
    #     await bot.process_commands(message)
    # except:
    #     pass
    await bot.process_commands(message)


@bot.event
async def on_server_join(server):
    if database_file_found:
        if database.database_online:
            await get_users()

    # for channel in server.channels:
    #     if 'music' in channel.name.lower():
    #         if str(channel.type) == 'voice':
    #             print(f'item {channel.id} found, joining {channel.server.name} : {channel.name}')
    #             try:
    #                 if database_file_found:
    #                     if database.database_online:
    #                         # auto stats music here
    #                         pass
    #             except Exception as e:
    #                 pass

    print(server.name)


if __name__ == '__main__':
    bot.run(config['bot-key'])