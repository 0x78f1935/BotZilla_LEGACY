import asyncio
import discord
from discord.ext import commands
import json
import datetime
import re
import aiohttp
import isodate
try:
    from plugin.database import Database
except:
    pass


if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            embed = discord.Embed(title='MusicPlayer:',
                                  description='Now playing: **`{}`**'.format(self.current),
                                  colour=0xf20006)
            last_message = await self.bot.send_message(self.current.channel, embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f3b5')
            self.current.player.start()
            await self.play_next_song.wait()

class Music:
    """
    Voice related commands.
    Works in multiple servers at once.
    """
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.channels = self.tmp_config['channels']
        self.emojiUnicode = self.tmp_config['unicode']
        self.owner_list = self.config['owner-id']
        self.music_playing = {}
        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except:
            print('Music: Database files not found')
            pass

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True)
    async def summon(self, ctx):
        """
        Summons the bot to join your voice channel.
        You have to be in a voice channel to be able to use this command
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!summon in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You are not in a voice channel.\nConsider the **`{}help summon`** option..'.format(self.config['prefix']),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You can stop me at any time.\nUse `{}stop` to stop me. You can also pause and resume me\nuse `{}help Music` for more information'.format(self.config['prefix'], self.config['prefix']),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Music is already playing in another voice channel.\nJoin that one instead :smile:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
        return True


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

        if url:
            if re.search(r'(https?://)?(www.)?youtube(.com)/[\w\d_\-?=&/]+', url):
                if 'index' in url.lower() or 'list' in url.lower():
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='Please.. don\'t use a youtube playlists, use **`{}help play`** instead'.format(self.config['prefix']),
                                          colour=0xf20006)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                    return

                else:

                    # somewhere here is a weird duplication bug. The bot triggers why, i have no clue why
                    if ctx.message.server.id not in self.music_playing:
                        self.music_playing[ctx.message.server.id] = ['0', ['t']]
                        server_que = self.music_playing[ctx.message.server.id][1]
                        if url in server_que:
                            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                                  description='**`{}`** has **already** been added to the playlist'.format(url),
                                                  colour=0xf20006)
                            last_message = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                            return
                        else:
                            server_que.append(url)
                            server_que.pop(0)
                            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                                  description='**`{}`** has been **added** to the playlist'.format(url),
                                                  colour=0xf20006)
                            last_message = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
                            print(self.music_playing[ctx.message.server.id])
                    else:
                        server_que = self.music_playing[ctx.message.server.id][1]
                        if url in server_que:
                            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                                  description='**`{}`** has **already** been added to the playlist'.format(url),
                                                  colour=0xf20006)
                            last_message = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
                            return
                        else:
                            server_que.append(url)
                            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                                  description='**`{}`** has been **added** to the playlist'.format(url),
                                                  colour=0xf20006)
                            last_message = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
                            print(self.music_playing[ctx.message.server.id])
                    # The weird bug section ends here.. fixed it with this if else statement

            else:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Please.. use a youtube link or use **`{}help play`** instead'.format(
                                          self.config['prefix']),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['error'])

        if ctx.message.server.id in self.music_playing:
            if self.music_playing[ctx.message.server.id][0] == '1':
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Music is **already** playing in another voice channel.\nJoin that one instead :smile:',
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

        if url is None:
            state = self.get_voice_state(ctx.message.server)
            opts = {
                'default_search': 'auto',
                'quiet': True,
            }

            if state.voice is None:
                success = await ctx.invoke(self.summon)
                if not success:
                    return

            if ctx.message.server.id not in self.music_playing:
                self.music_playing[ctx.message.server.id] = ['1', ['https://www.youtube.com/watch?v=cdwal5Kw3Fc']]

            self.music_playing[ctx.message.server.id][0] = 1
            print(self.music_playing)

            try:
                for songs in range(100):
                    self.database.cur.execute("select * from botzilla.musicque order by random() limit 1;")
                    song = self.database.cur.fetchall()
                    self.database.cur.execute("ROLLBACK;")
                    server_que = self.music_playing[ctx.message.server.id][1]
                    server_que.append(song[0][0])
                    print(self.music_playing)

                    if not server_que:
                        embed = discord.Embed(title='MusicPlayer:',
                                              description='Playlist is **empty**, use **`{}play`** for a new playlist!'.format(
                                                  self.config['prefix']),
                                              colour=0xf20006)
                        last_message = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
                    else:

                        player = await state.voice.create_ytdl_player(server_que.pop(0), ytdl_options=opts)
                        player.volume = 1
                        player.start()

                        embed = discord.Embed(title='MusicPlayer:',
                                              description='**Now playing:**\n`{}`\n**Duration:**\n`{}` seconds\n\nYou can stop me anytime with **`{}stop`**'.format(
                                                  player.title, player.duration, self.config['prefix']),
                                              colour=0xf20006)
                        last_message = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(last_message, '\U0001f3b5')

                        await asyncio.sleep(player.duration)

                        if self.music_playing[ctx.message.server.id][0] == '0':
                            await ctx.invoke(self.stop)
                            break

                        player.stop()

                embed = discord.Embed(title='MusicPlayer:',
                                      description='Playlist is **empty**, use **`{}play`** for a new playlist!'.format(
                                          self.config['prefix']),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

            except Exception as e:
                fmt = 'An error occurred while processing this request: ```Python\n{}: {}\n```\nPlease send a {}report <error message>'.format(type(e).__name__, e.args, self.config['prefix'])
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=fmt,
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['error'])
                await ctx.invoke(self.stop)


    async def volume(self, ctx, value : int = None):
        """
        Sets the volume of the currently playing song.
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!volume <{value}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if value is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='If you don\'t know how loud you want your volume\nI can\'t help you. Maybe **`{}help volume`** can'.format(self.config['prefix']),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Set the volume to **`{:.0%}`**'.format(player.volume),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


    async def pause(self, ctx):
        """
        Pauses the currently played song.
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!pause in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Done. Use **`{}resume`** if u like to listen again'.format(self.config['prefix']),
                              colour=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


    async def resume(self, ctx):
        """
        Resumes the currently played song.
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!resume in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Done. You can pause anytime you want.\nJust use **`{}pause`** to pause'.format(self.config['prefix']),
                              colour=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """
        Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!stop in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        if ctx.message.server.id not in self.music_playing:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='There is no music playing :( use **`{}help play`** for more information'.format(
                                      self.config['prefix']),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return

        if ctx.message.server.id in self.music_playing and self.music_playing[ctx.message.server.id][0] == '0':
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='There is no music playing :( use **`{}help play`** for more information'.format(
                                      self.config['prefix']),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return

        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass
        finally:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Oke then... :angry:',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f44b')
            self.music_playing[ctx.message.server.id][0] = 0


    async def skip(self, ctx):
        """
        Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!skip in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Not playing any music right now...',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Requester requested skipping song...',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Skip vote passed, skipping song...',
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
                state.skip()
            else:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Skip vote added, currently at {}/3'.format(total_votes),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You have already voted to skip this song.',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['error'])


    async def np(self, ctx):
        """
        Shows info about the currently played song.
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!playing in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Not playing anything.',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f622')
        else:
            skip_count = len(state.skip_votes)
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Now playing\n```{}```\nSkips: {}/3'.format(state.current, skip_count),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Music(bot))