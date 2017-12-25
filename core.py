# These are the dependecies. The bot depends on these to function, hence the name. Please do not change these unless your adding to them, because they can break the bot.
import discord
from discord.ext.commands import Bot
import platform
import json
from bot.options.opus_loader import load_opus_lib

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

    bot.load_extension('plugin.admin')
    bot.load_extension('plugin.exchange')
    bot.load_extension('plugin.fun')
    bot.load_extension('plugin.games')
    bot.load_extension('plugin.gamestats')
    bot.load_extension('plugin.information')
    bot.load_extension('plugin.music')
    bot.load_extension('plugin.nsfw')
    bot.load_extension('plugin.python_code_in_dc')
    bot.load_extension('plugin.test')

@bot.event
async def on_message_delete(message):
    fmt = '**{0.author.server}** | ***{0.author.name}*** has deleted the message:\n{0.content}'
    for owners in config['owner-id']:
        owner = await bot.get_user_info(owners)
        await bot.send_message(owner, fmt.format(message))


if __name__ == '__main__':
    bot.run(config['bot-key'])