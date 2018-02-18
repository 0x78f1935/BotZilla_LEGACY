import discord
from discord.ext import commands
import youtube_dl
import functools
import asyncio
import datetime
import math
import random
import re
from collections import deque
import json
try:
    from plugin.database import Database
except Exception as e:
    pass


def setup(bot):
    bot.add_cog(Music(bot))


class VoiceEntry:

    def __init__(self, bot, message, url):
        self.requester = message.author
        self.bot = bot
        self.channel = message.channel
        self.url = url
        self.info = None
        self.download_url = None
        self.views = None
        self.is_live = None
        self.likes = None
        self.dislikes = None
        self.duration = None
        self.uploader = None
        self.title = None
        self.description = None
        self.upload_date = None
        self.doit = True

    async def getInfo(self):
        opts = {
            "format": 'webm[abr>0]/bestaudio/best',
            "ignoreerrors": True,
            "default_search": "auto",
            "source_address": "0.0.0.0",
            'quiet': True}
        ydl = youtube_dl.YoutubeDL(opts)
        func = functools.partial(ydl.extract_info, self.url, download=False)
        info = await self.bot.loop.run_in_executor(None, func)
        try:
            if "entries" in info:
                info = info['entries'][0]
            self.info = info
            self.download_url = info.get('url')
            self.views = info.get('view_count')
            self.is_live = bool(info.get('is_live'))
            self.likes = info.get('like_count')
            self.dislikes = info.get('dislike_count')
            self.duration = info.get('duration')
            if self.duration is None:
                self.duration = 0
            self.uploader = info.get('uploader')

            is_twitch = 'twitch' in self.url
            if is_twitch:
                self.title = info.get('description')
                self.description = None
            else:
                self.title = info.get('title')
                self.description = info.get('description')

            date = info.get('upload_date')
            if date:
                try:
                    date = datetime.datetime.strptime(date, '%Y%M%d').date()
                except ValueError:
                    date = None

            self.upload_date = date
        except TypeError:
            self.doit = False
            embed = discord.Embed(title='MusicPlayer:',
                                  description='Something went wrong with gathering the info.\nSkipping url..',
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, '\u23e9')
            await asyncio.sleep(5)
            await self.bot.delete_message(out)

    def __str__(self):
        fmt = '**{0.title}** uploaded by **{0.uploader}** and requested by **{1.display_name}**'
        if self.duration:
            fmt += ' `[length: {0[0]}m {0[1]}s]`'.format(
                divmod(self.duration, 60))
        return fmt.format(self, self.requester)

    def __repr__(self):
        return '<{0.title}, {0.requester.display_name}>'.format(self)


class VoiceState:

    def __init__(self, _bot):
        self.current = None
        self.voice = None
        self.currenttime = None
        self.empty = None
        self.currentplayer = None
        self.repeat = False
        self.bot = _bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()  # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.currentplayer is None:
            return False

        player = self.currentplayer
        return not player.is_done()

    @property
    def player(self):
        return self.currentplayer

    def sortclumps(self, l, n, queue=[]):
        def safe_list_get(l, idx, default):
            try:
                return l[idx]
            except IndexError:
                l.append(default)
                return default

        def nextclump(ind, i):
            ind += 1
            try:
                clump = newqueue[ind]
            except IndexError:
                newqueue.append([])
                clump = newqueue[ind]
            userclump = [hash(e.requester) for e in clump]
            if userclump.count(hash(i.requester)) < n:
                clump.append(i)
            else:
                nextclump(ind, i)
        newqueue = queue.copy()
        ind = 0
        clump = safe_list_get(newqueue, 0, [])
        for i in l:
            userclump = [hash(e.requester) for e in clump]
            if userclump.count(hash(i.requester)) < n:
                clump.append(i)
            else:
                nextclump(ind, i)
        return deque([j for i in newqueue for j in i])

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    def create_player(self, entry):
        player = self.voice.create_ffmpeg_player(
            entry.download_url, after=self.toggle_next)
        player.volume = 0.55
        return player

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.skip_votes.clear()
            self.empty = self.songs.empty()
            if not self.repeat:
                self.current = await self.songs.get()
                try:
                    self.songs._queue = self.sortclumps(self.songs._queue, 2, deque())
                except Exception as e:
                    self.songs._queue = self.sortclumps(self.songs._queue, 2, [x for x in self.songs._queue])
            self.currentplayer = self.create_player(self.current)
            if not self.empty:
                if not self.repeat:
                    embed = discord.Embed(title='MusicPlayer:',
                                          description='Now playing: **`{}`**'.format(str(self.current)),
                                          colour=0xf20006)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, '\U0001f3b5')
                else:
                    embed = discord.Embed(title='MusicPlayer:',
                                          description='Repeating: **`{}`**'.format(str(self.current)),
                                          colour=0xf20006)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, '\U0001f3b5')
            self.currenttime = datetime.datetime.now()
            self.currentplayer.start()
            await self.play_next_song.wait()


class Music:

    def __init__(self, _bot):
        self.bot = _bot
        self.voice_states = {}
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.owner_list = self.config['owner-id']
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

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            embed = discord.Embed(title='MusicPlayer:',
                                  description='You are not in a voice channel.',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song: str):
        """Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        ytdl = youtube_dl.YoutubeDL({
            "format": 'best',
            "ignoreerrors": True,
            "default_search": "ytsearch",
            "source_address": "0.0.0.0"})
        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return
        shuffle = True if ' +shuffle' in song else False
        if shuffle:
            song.replace(' +shuffle', '')
        if re.search(r'(https?://)?(www.)?youtube(.com)/[\w\d_\-?=&/]+', song):
            #If playlist
            if 'index' in song.lower() or 'list' in song.lower():
                embed = discord.Embed(title='MusicPlayer:',
                                      description='Playlist detected, enqueuing all items...',
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, '\U0001f3b5')
                info = ytdl.extract_info(song, download=False, process=False)
                songlist = []
                for e in info['entries']:
                    if e:
                        if 'youtube' in info['extractor']:
                            songlist.append(
                                'https://www.youtube.com/watch?v={}'.format(e['id']))

                firstsong = None
                weeee = True if not state.is_playing() else False
                if shuffle:
                    random.shuffle(songlist)
                for video in songlist:
                    entry = VoiceEntry(self.bot, ctx.message, video)
                    await entry.getInfo()
                    if not entry.doit:
                        continue
                    if songlist.index(video) == 0:
                        firstsong = entry
                    await state.songs.put(entry)
                if weeee:
                    embed = discord.Embed(title='MusicPlayer:',
                                          description='Successfully enqueued\n**`{}`**\nentries and started playing\n**`{}`**'.format(len(songlist), firstsong),
                                          colour=0xf20006)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
                    out = None
                else:
                    embed = discord.Embed(title='MusicPlayer:',
                                          description='Successfully enqueued **`{}`** entries!'.format(len(songlist)),
                                          colour=0xf20006)
                    out = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(out, self.emojiUnicode['succes'])
        else:
            entry = VoiceEntry(self.bot, ctx.message, song)
            await entry.getInfo()
            if entry.doit:
                if not state.is_playing():
                    embed = discord.Embed(title='MusicPlayer:',
                                          description='Enqueued and now playing\n**`{}`**'.format(str(entry)),
                                          colour=0xf20006)
                    last_message = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
                    out = None
                    await state.songs.put(entry)
                else:
                    embed = discord.Embed(title='MusicPlayer:',
                                          description='Enqueued : **`{}`**'.format(str(entry)),
                                          colour=0xf20006)
                    out = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(out, self.emojiUnicode['succes'])
                    await state.songs.put(entry)
            else:
                await self.bot.delete_message(ctx.message)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value: int):
        """Sets the volume of the currently playing song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            if value > 200:
                value = 200
            player.volume = value / 100
            embed = discord.Embed(title='MusicPlayer:',
                                  description='Set the volume to {:.0%}'.format(player.volume),
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()
        else:
            if state.current is None:
                embed = discord.Embed(title='MusicPlayer:',
                                      description='Not playing anything.',
                                      colour=0xf20006)
                out = await self.bot.say(embed=embed)
                await self.bot.add_reaction(out, self.emojiUnicode['warning'])


    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()
        else:
            if state.current is None:
                embed = discord.Embed(title='MusicPlayer:',
                                      description='Not playing anything.',
                                      colour=0xf20006)
                out = await self.bot.say(embed=embed)
                await self.bot.add_reaction(out, self.emojiUnicode['warning'])


    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()
        else:
            if state.current is None:
                embed = discord.Embed(title='MusicPlayer:',
                                      description='Not playing anything.',
                                      colour=0xf20006)
                out = await self.bot.say(embed=embed)
                await self.bot.add_reaction(out, self.emojiUnicode['warning'])
                return

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """
        Vote to skip a song. The song requester can force skip.
        Majority vote is needed for the song to be skipped.
        """
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            embed = discord.Embed(title='MusicPlayer:',
                                  description='Not playing any music right now...\nUse **`{}help skip`** for more info'.format(self.config['prefix']),
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, self.emojiUnicode['warning'])
            return

        voter = ctx.message.author
        if voter.id in self.owner_list:
            embed = discord.Embed(title='MusicPlayer:',
                                  description='Bot owner requested skipping song...',
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, self.emojiUnicode['succes'])
            state.toggle_next()
            return

        elif voter == state.current.requester:
            embed = discord.Embed(title='MusicPlayer:',
                                  description='Requester requested skipping song...',
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, self.emojiUnicode['succes'])
            state.toggle_next()
            return

        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= math.ceil(int(round((len(ctx.message.server.me.voice_channel.voice_members) - 1) / 2))):
                embed = discord.Embed(title='MusicPlayer:',
                                      description='Skip vote passed, skipping song...',
                                      colour=0xf20006)
                out = await self.bot.say(embed=embed)
                await self.bot.add_reaction(out, self.emojiUnicode['succes'])
                state.toggle_next()
                return

            else:
                embed = discord.Embed(title='MusicPlayer:',
                                      description='Skip vote added, currently at [{}/{}]'.format(total_votes, math.ceil((len(ctx.message.server.me.voice_channel.voice_members) - 1) / 2)),
                                      colour=0xf20006)
                out = await self.bot.say(embed=embed)
                await self.bot.add_reaction(out, self.emojiUnicode['succes'])
                return
        else:
            embed = discord.Embed(title='MusicPlayer:',
                                  description='You have already voted to skip this song.',
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, self.emojiUnicode['warning'])
            return

    @commands.command(pass_context=True, no_pm=True)
    async def np(self, ctx):
        """Shows the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            embed = discord.Embed(title='MusicPlayer:',
                                  description='Not playing anything.',
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, self.emojiUnicode['warning'])
        else:
            skip_count = len(state.skip_votes)
            t1 = state.currenttime
            t2 = datetime.datetime.now()
            duration = (t2 - t1).total_seconds()
            embed = discord.Embed(title='MusicPlayer:',
                                  description='Now playing {0} `[skips: {1}/{2}] [{3[0]}m {3[1]}s/{4[0]}m {4[1]}s]`'.format(state.current, skip_count, math.ceil((len(ctx.message.server.me.voice_channel.voice_members) - 1) / 2), divmod(math.floor(duration), 60), divmod(state.current.duration, 60)),
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, self.emojiUnicode['succes'])


    @commands.command(name='que', pass_context=True, no_pm=True)
    async def _list(self, ctx):
        """Shows the queue for your server."""
        state = self.get_voice_state(ctx.message.server)
        entries = [x for x in state.songs._queue]
        if len(entries) == 0:
            embed = discord.Embed(title='MusicPlayer:',
                                  description='There are currently no songs in the queue!',
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, self.emojiUnicode['warning'])

        else:
            counter = 1
            totalduration = 0
            send = 'Found queue of **{1}** for **{0}**\n'.format(
                ctx.message.server.name, len(entries))
            for entry in entries[:10]:
                requester = entry.requester
                send += '`[{0[0]}m {0[1]}s]` {1}. **{2}** requested by **{3}**\n'.format(
                    divmod(entry.duration, 60), counter, entry.title, requester.display_name)
                counter += 1
            if len(entries) > 10:
                send += 'And {} more...\n'.format(str(len(entries) - 10))
            for entry in entries:
                if entry.duration is None:
                    entry.duration = 0
                totalduration += entry.duration
            send += 'Total duration: `[{0}]`'.format(
                datetime.timedelta(seconds=totalduration))
            embed = discord.Embed(title='MusicPlayer:',
                                  description='{}'.format(send),
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, self.emojiUnicode['succes'])
            await asyncio.sleep(10)


    @commands.command(name="info", pass_context=True, no_pm=True)
    async def _info(self, ctx):
        """Shows info about the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            embed = discord.Embed(title='MusicPlayer:',
                                  description='Not playing anything.',
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, self.emojiUnicode['warning'])
        else:
            skip_count = len(state.skip_votes)
            t1 = state.currenttime
            t2 = datetime.datetime.now()
            duration = (t2 - t1).total_seconds()
            send = """Currently played song: **{0.title}**
Uploader: **{0.uploader}**
Views: *{0.views}*
Likes/Dislikes: *{0.likes}/{0.dislikes}*
Upload date: **{0.upload_date}**
Skips: `[skips: {1}/{2}]`
Duration: `[{3[0]}m {3[1]}s/{4[0]}m {4[1]}s]`
""".format(state.current, skip_count, math.ceil((len(ctx.message.server.me.voice_channel.voice_members) - 1) / 2), divmod(math.floor(duration), 60), divmod(state.current.duration, 60))
            embed = discord.Embed(title='MusicPlayer:',
                                  description='{}'.format(send),
                                  colour=0xf20006)
            out = await self.bot.say(embed=embed)
            await self.bot.add_reaction(out, self.emojiUnicode['succes'])