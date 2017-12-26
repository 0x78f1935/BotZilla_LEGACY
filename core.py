# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
from discord.ext.commands import Bot
import platform
import json
from options.opus_loader import load_opus_lib
from urllib.parse import quote as uriquote
import re
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
bot = Bot(description="BotZilla is build / maintained / self hosted by PuffDip", command_prefix=config['prefix'], pm_help=False)
music_channels = botzillaChannels['music']



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


    try:
        database = Database(bot)
        for item in database.music_channels:
            try:
                channel = bot.get_channel(str(item))
                if channel == None:
                    pass
                else:
                    print('Joined : {}'.format(channel))
                    await bot.join_voice_channel(channel)
            except Exception as e:
                continue
    except Exception as e:
        print(e.args)


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