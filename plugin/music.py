import discord
from discord.ext.commands import Bot
from discord.ext import commands
import json
import random

try:
    from plugin.database import Database
    database_file_found = True
except:
    print('Music: Database files not found')
    pass

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']
        self.blue_A = '\U0001f1e6'
        self.red_B = '\U0001f171'
        self.blue_I = '\U0001f1ee'
        self.blue_L = '\U0001f1f1'
        self.blue_O = '\U0001f1f4'
        self.blue_T = '\U0001f1f9'
        self.blue_Z = '\U0001f1ff'
        self.arrow_up = '\u2b06'
        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except:
            print('AdminPanel: Database files not found')
            pass
        self.music_playlist = []


    async def done_playing(self, channel_id):
        channel = self.bot.get_channel(channel_id)
        voice = self.bot.join_voice_channel(channel)
        player = voice.create_ytdl_player(f"{random.choice(music_playlist)}", after=Music.done_playing(channel_id))
        if player.is_playing():
            player.start()



    async def get_playlist(self):
        # get playlist

        if database_file_found:
            if self.database.database_online:
                self.database.cur.execute('select * from botzilla.musicque;')
                rows = self.database.cur.fetchall()
                self.database.cur.execute("ROLLBACK;")
                rows = str(rows).replace('[(\'', '')
                rows = rows.replace(',)', '')
                rows = rows.replace('(', '')
                rows = rows.replace('\'', '')
                links = rows.replace(' ', '')
                clean_links = links.split(',')
                for item in clean_links:
                    self.music_playlist.append(item)
        print(self.music_playlist)


    async def autojoin_music_channels(self, ctx):
        for server in self.bot.servers:
            for channel in server.channels:
                if 'music' in channel.name.lower():
                    if str(channel.type) == 'voice':
                        print(f'item {channel.id} found, joining {channel.server.name} : {channel.name}')
                        channel_id = channel.id
                        channel = self.bot.get_channel(channel.id)
                        voice = self.bot.join_voice_channel(channel)
                        try:
                            if database_file_found:
                                if self.database.database_online:
                                    try:
                                        player = voice.create_ytdl_player(f"{random.choice(music_playlist)}", after=await Music.done_playing(self, channel_id))
                                        if player.is_playing():
                                            player.start()
                                    except Exception as e:
                                        print(
                                            f'item {channel.id} found, FAILED to join {channel.server.name} : {channel.name}\n{e.args}')
                        except Exception as e:
                            print(f'Database seems offline:\n{e.args}')


def setup(bot):
    bot.add_cog(Music(bot))