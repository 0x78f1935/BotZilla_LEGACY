import asyncio
import discord
from discord.ext import commands
import json
import datetime
import re
try:
    from plugin.database import Database
except Exception as e:
    pass

if not discord.opus.is_loaded():
    discord.opus.load_opus('opus')

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.owner_list = self.config['owner-id']
        self.music_json = {}
        for server in self.bot.servers:
            music_js_raw =  {
                server.id : {
                    'playing' : 'False',
                    'voice_channel' : 'False',
                    'que' : []
                }
            }
            self.music_json.update(music_js_raw)
        with open('./options/musicplayer.json', 'w') as self.music_conf:
            json.dump(self.music_json, self.music_conf)

        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except:
            print('Music: Database files not found')
            pass






def setup(bot):
    bot.add_cog(Music(bot))