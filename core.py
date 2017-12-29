# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
from discord.ext.commands import Bot
import platform
import json
from options.opus_loader import load_opus_lib
from urllib.parse import quote as uriquote
import re
import random
import csv
import asyncio
from plugin.music import Music


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
music = Music(bot)

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
                row = str(row).replace('["', '')
                row = str(row).replace('"]', '')
                database.cur.execute("INSERT INTO botzilla.users (ID, name) VALUES{};".format(row))
                database.cur.execute("ROLLBACK;")
    except Exception as e:
        pass


    #music channels
    try:
        with open(database.database_import_location_music_channels, 'r') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                row = str(row).replace('["', '')
                row = str(row).replace('"]', '')
                database.cur.execute("INSERT INTO botzilla.music (ID, channel_name, server_name, type_channel) VALUES{};".format(row))
                database.cur.execute("ROLLBACK;")
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



@bot.event
async def on_ready():
    print('Logged in as ' + bot.user.name + ' (ID:' + bot.user.id + ') | Connected to ' + str(
        len(bot.servers)) + ' servers | Connected to ' + str(len(set(bot.get_all_members()))) + ' users')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(discord.__version__,
                                                                               platform.python_version()))
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('--------')
    dbimport()

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

    await music.get_playlist()
    await music.autojoin_music_channels(bot)


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