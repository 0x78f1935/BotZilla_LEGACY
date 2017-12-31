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
from options import exceptions
from options.player import MusicPlayer
from options.playlist import Playlist
from options import downloader
from collections import defaultdict

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
downloader = downloader.Downloader(download_folder='audio_cache')
ssd_defaults = {'last_np_msg': None, 'auto_paused': False}
server_specific_data = defaultdict(lambda: dict(ssd_defaults))


class SkipState:
    def __init__(self):
        self.skippers = set()
        self.skip_msgs = set()

    @property
    def skip_count(self):
        return len(self.skippers)

    def reset(self):
        self.skippers.clear()
        self.skip_msgs.clear()

    def add_skipper(self, skipper, msg):
        self.skippers.add(skipper)
        self.skip_msgs.add(msg)
        return self.skip_count


class Response:
    def __init__(self, content, reply=False, delete_after=0):
        self.content = content
        self.reply = reply
        self.delete_after = delete_after


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


async def get_player(channel, music_playlist, create=False) -> MusicPlayer:
    server = channel.server
    print(f'{channel} : {server}')

    voice_client = await bot.get_voice_client(channel)

    player = MusicPlayer(bot, voice_client, music_playlist) \
        .on('play', bot.on_player_play) \
        .on('resume', bot.on_player_resume) \
        .on('pause', bot.on_player_pause) \
        .on('stop', bot.on_player_stop) \
        .on('finished-playing', bot.on_player_finished_playing) \
        .on('entry-added', bot.on_player_entry_added)
    print(player)
    player.skip_state = SkipState()
    bot.players[server.id] = player
    print(f'{bot.players[server.id]} : {server}')
    return bot.players[server.id]


async def safe_delete_message(message, *, quiet=False):
    try:
        return await bot.delete_message(message)

    except discord.Forbidden:
        if not quiet:
            print("Warning: Cannot delete message \"{}\", no permission".format(message.clean_content))

    except discord.NotFound:
        if not quiet:
            print("Warning: Cannot delete message \"{}\", message not found".format(message.clean_content))


async def on_player_play(player, entry):
    await update_now_playing(entry)
    player.skip_state.reset()

    channel = entry.meta.get('channel', None)
    author = entry.meta.get('author', None)

    if channel and author:
        last_np_msg = server_specific_data[channel.server]['last_np_msg']
        if last_np_msg and last_np_msg.channel == channel:

            async for lmsg in bot.logs_from(channel, limit=1):
                if lmsg != last_np_msg and last_np_msg:
                    await safe_delete_message(last_np_msg)
                    server_specific_data[channel.server]['last_np_msg'] = None
                break  # This is probably redundant

        embed = discord.Embed(title='{}:'.format(entry.title),
                              description='Now playing: **{}**'.format(player.voice_client.channel.name, ),
                              colour=0xf20006)
        last_message = await bot.say(embed=embed)
        await bot.add_reaction(last_message, emojiUnicode['succes'])

async def update_now_playing(self, entry=None, is_paused=False):
    await self.change_presence(game=discord.Game(name='Powerd by PuffDip'))

async def on_player_resume(self, entry, **_):
    await self.update_now_playing(entry)

async def on_player_pause(self, entry, **_):
    await self.update_now_playing(entry, True)

async def on_player_stop(self, **_):
    await self.update_now_playing()

async def on_player_entry_added(self, playlist, entry, **_):
    pass




async def on_player_finished_playing(player, music_playlist, **_,):
    while True:
        song_url = random.choice(music_playlist)
        info = await downloader.Downloader.safe_extract_info(player.playlist.loop, song_url, download=False, process=False)

        if not info:
            print("[Info] Removing unplayable song from autoplaylist: {}".format(song_url))
            music_playlist.remove(song_url)
            continue

        if info.get('entries', None):  # or .get('_type', '') == 'playlist'
            pass  # Wooo playlist
            # Blarg how do I want to do this

        # TODO: better checks here
        try:
            await player.playlist.add_entry(song_url, channel=None, author=None)
        except exceptions.ExtractionError as e:
            print("Error adding song from autoplaylist:", e)
            continue

        break

    if not music_playlist:
        print("[Warning] No playable songs in the autoplaylist, disabling.")


async def create_player(channel_id):
    channel = bot.get_channel(f'{channel_id}')
    voice = await bot.join_voice_channel(channel)
    while True:
        player = await voice.create_ytdl_player(f"{random.choice(music_playlist)}")
        if player.is_playing():
            player.start()
        await asyncio.sleep(player.duration)
        print('Song finished playing')


async def start_music(channel_id):
    while bot.loop:
        bot.loop.run_until_complete(create_player(channel_id))

async def auto_join_channels(music_playlist):
    for server in bot.servers:
        for channel in server.channels:
            if 'music' in channel.name.lower():
                if str(channel.type) == 'voice':
                    print(f'item {channel.id} found, joining {channel.server.name} : {channel.name}')
                    try:
                        if database_file_found:
                            if database.database_online:
                                await dbimport()
                                channel = bot.get_channel(f'{channel.id}')
                                await bot.join_voice_channel(channel)
                                player = await get_player(channel=channel, music_playlist=music_playlist, create=True)
                                if player.is_stopped:
                                    player.play()

                                await on_player_finished_playing(player)
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

    #plugins

    plugins = (
        "admin",
        "exchange",
        "database",
        "fun",
        "games",
        "gamestats",
        "information",
        "python_code_in_dc",
        "test"
    )

    # load plugins

    for p in plugins:
        bot.load_extension("plugin.{}".format(p))

    print('Try auto connect music channel...')
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

    await auto_join_channels(music_playlist)


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
            search_term = re.search(r'\bhow\b.*[?]', message.content.lower()).group(0)
            search_term = uriquote(search_term)
            embed = discord.Embed(title='{}:'.format(message.author.name),
                                  description='{}'.format('http://lmgtfy.com/?q={}'.format(search_term)),
                                  colour=0xf20006)
            last_message = await bot.send_message(message.channel, embed=embed)
            await bot.add_reaction(last_message, emojiUnicode['succes'])
        await bot.process_commands(message)
    except:
        pass


@bot.event
async def on_server_join(server):
    if database_file_found:
        if database.database_online:
            await get_users()
    for channel in server.channels:
        if 'music' in channel.name.lower():
            if str(channel.type) == 'voice':
                print(f'item {channel.id} found, joining {channel.server.name} : {channel.name}')
                try:
                    if database_file_found:
                        if database.database_online:
                            await start_music(channel.id)
                except Exception as e:
                    pass

    print(server.name)

if __name__ == '__main__':
    bot.run(config['bot-key'])