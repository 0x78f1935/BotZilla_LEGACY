# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
from discord.ext.commands import Bot
import platform
import json
from options.opus_loader import load_opus_lib
from urllib.parse import quote as uriquote
import re
import csv
import asyncio


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
bot = Bot(description="BotZilla is built / maintained / self hosted by PuffDip", command_prefix=config['prefix'], pm_help=False)
music_channels = botzillaChannels['music']
database_file_found = False
try:
    database = Database(bot)
    database_file_found = True
except:
    print('Database files not found')
    pass


def dbimport():
    """
    Import CSV data from import folder
    """

    try:
        with open(database.database_import_location_users, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                row = str(row).replace('["', '')
                row = str(row).replace('"]', '')
                database.cur.execute("INSERT INTO botzilla.users (ID, name) VALUES({});".format(row))
    except Exception as e:
        print('Could not load data users\n{}'.format(e.args))


    try:
        with open(database.database_import_location_music_channels, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                row = str(row).replace('["', '')
                row = str(row).replace('"]', '')
                database.cur.execute("INSERT INTO botzilla.music (ID, channel_name, server_name, type_channel) VALUES({});".format(row))
    except Exception as e:
        print('Could not load music data\n{}'.format(e.args))


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
        "games",
        "gamestats",
        "information",
        "music",
        "nsfw",
        "python_code_in_dc",
        "test"
    )

    # load plugins

    for p in plugins:
        bot.load_extension("plugin.{}".format(p))

    print('Try auto connect music channel...')

    players = {}
    for server in bot.servers:
        for channel in server.channels:
            if 'music' in channel.name.lower():
                if str(channel.type) == 'voice':
                    print(f'item {channel.id} found, joining {channel.server.name} : {channel.name}')
                    channel = bot.get_channel(channel.id)
                    voice = await bot.join_voice_channel(channel)
                    try:
                        if database_file_found:
                            if database.database_online:
                                database.cur.execute("SELECT * from botzilla.musicque ORDER BY random() limit 1;")
                                rows = database.cur.fetchall()
                                rows = str(rows).replace('[(\'', '')
                                rows = str(rows).replace('\',)]', '')
                                print(rows)
                                voice.create_ytdl_player(f'{rows}')
                    except Exception as e:
                        print(f'Database seems offline:\n{e.args}')


    # if database_file_found:
    #     print('DatabaseFile found!')
    #     if database.database_online:
    #         try:
    #             dbimport()
    #             database.cur.execute("select id from botzilla.music where type_channel = 'voice';")
    #             music_channel_ids = database.cur.fetchall()
    #             for item in music_channel_ids:
    #                 try:
    #                     channel = bot.get_channel(str(item[0]))
    #                     if channel == None:
    #                         print(f'item {item[0]} MISMATCH, can\'t joining {channel.server.name} : {channel.name}')
    #                     else:
    #                         print(f'item {item[0]} found, joining {channel.server.name} : {channel.name}')
    #                         await bot.join_voice_channel(channel)
    #                 except Exception as e:
    #                     continue
    #         except Exception as e:
    #             print('Database seems offline:\n{}'.format(e.args))


@bot.event
async def on_message_delete(message):
    fmt = '**{0.author.server}** | ***{0.author.name}*** has deleted the message:\n{0.content}'
    for owners in config['owner-id']:
        owner = await bot.get_user_info(owners)
        await bot.send_message(owner, fmt.format(message))


@bot.event
async def on_message(message):
    if message.author.bot: return
    try:
        if 'how' in message.content.lower():
            search_term = re.search(r'\bhow\b.*$', message.content.lower()).group(0)
            search_term = uriquote(search_term)
            embed = discord.Embed(title='{}:'.format(message.author.name),
                                  description='{}'.format('http://lmgtfy.com/?q={}'.format(search_term)),
                                  colour=0xf20006)
            last_message = await bot.send_message(message.channel, embed=embed)
            await bot.add_reaction(last_message, emojiUnicode['succes'])
        await bot.process_commands(message)
    except:
        pass


if __name__ == '__main__':
    bot.run(config['bot-key'])