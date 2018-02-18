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
                    'voice_channel_name' : 'None',
                    'que' : []
                }
            }
            self.music_json.update(music_js_raw)

        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except:
            print('Music: Database files not found')
            pass


    @commands.command(pass_context=True)
    async def play(self, ctx, url=None):
        """
        This command is multifunctional.
        Use !!play to start the playlist.
        Random tracks will be added to the playlist.
        This keeps going until 100 tracks are finished with playing.
        Use !!play <youtube url> to add a song to the playlist
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!play in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        #global function variables
        # - server_que : list
        server_que = self.music_json[ctx.message.server.id]['que']
        que_add = False

        #If url exist
        if url and re.search(r'(https?://)?(www.)?youtube(.com)/[\w\d_\-?=&/]+', url):
            #If playlist
            if 'index' in url.lower() or 'list' in url.lower():
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Please.. don\'t use a youtube playlists, use **`{}help play`** instead'.format(
                                          self.config['prefix']),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                return
            else:
                # If url already exist in playlist/que
                if url in server_que:
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='**`{}`** has **already** been added to the playlist'.format(url),
                                          colour=0xf20006)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                    return

                # If url not in playlist/que
                if url not in server_que:
                    server_que.append(url)
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='**`{}`** has been **added** to the playlist'.format(url),
                                          colour=0xf20006)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
                    que_add = True

        # reload global function variables
        # - is_playing : str-bool
        is_playing = self.music_json[ctx.message.server.id]['playing']
        #- is_in_voice_channel : str-bool
        is_in_voice_channel = self.music_json[ctx.message.server.id]['voice_channel']

        # If already in voice channel and if already playing
        if is_in_voice_channel == 'True' or is_playing == 'True':
            # If song has been added, no message. otherwise message
            if que_add:
                pass
            else:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='I am already playing music in a voice channel\nJoin that one instead :smiley:',
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                return
            return

        # if not in voice channel
        if is_in_voice_channel == 'False':
            self.requester_in_voice_channel = ctx.message.author.voice_channel
            # If requester is not in voice channel
            if self.requester_in_voice_channel is None:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='You are not in a voice channel.\nConsider the **`{}help summon`** option..'.format(
                                          self.config['prefix']),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                return

            # Change is_in_voice_channel to true
            if self.requester_in_voice_channel:
                self.player = self.bot.join_voice_channel(self.requester_in_voice_channel)
                self.music_json[ctx.message.server.id]['voice_channel'] = 'True'
                self.music_json[ctx.message.server.id][self.requester_in_voice_channel] = self.requester_in_voice_channel


        if is_playing == 'False':
            # reload global function variables
            # - server_que : list
            server_que = self.music_json[ctx.message.server.id]['que']
            # - is_playing : str-bool
            is_playing = self.music_json[ctx.message.server.id]['playing']
            # - is_in_voice_channel : str-bool
            is_in_voice_channel = self.music_json[ctx.message.server.id]['voice_channel']

            # If no server_que, retrieve song from database and nothing is playing
            if server_que == 'False' and is_playing == 'False':
                self.database.cur.execute("select * from botzilla.musicque order by random() limit 1;")
                song = self.database.cur.fetchall()
                self.database.cur.execute("ROLLBACK;")
                server_que.append(song[0][0])

            # If not in voicechannel raise error
            if is_in_voice_channel == 'False':
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='I am not in a voice channel, use **`{}help play`** for more info'.format(
                                          self.config['prefix']),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                return

            ## If in voice_channel play music
            if is_in_voice_channel == 'True':
                # reload global function variables
                # - server_que : list
                server_que = self.music_json[ctx.message.server.id]['que']

                # Raise error if there are no items in the server_que
                if not server_que:
                    self.database.cur.execute("select * from botzilla.musicque order by random() limit 1;")
                    song = self.database.cur.fetchall()
                    self.database.cur.execute("ROLLBACK;")
                    server_que.append(song[0][0])

                # Dubble is_playing check
                if is_playing == 'False':
                    # If there is a server_que
                    self.channel_name = self.music_json[ctx.message.server.id]['voice_channel_name']
                    if server_que:
                        requester_in_voice_channel_new = ctx.message.author.voice_channel
                        if que_add:
                            return
                        if requester_in_voice_channel_new != self.channel_name:
                            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                                  description='Please use the music channel, currently:\n**`{}`**'.format(self.channel_name),
                                                  colour=0xf20006)
                            last_message = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                            return
                        else:
                            song = server_que.pop(0)
                            self.player = await self.player(song)
                            self.player.volume = 1
                            self.player.start()


















def setup(bot):
    bot.add_cog(Music(bot))