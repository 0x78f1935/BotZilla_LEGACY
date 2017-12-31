import asyncio
import discord
from discord.ext import commands
import json

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
            await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
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
        """
        Summons the bot to join your voice channel.
        You have to be in a voice channel to be able to use this command
        """
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You are not in a voice channel.\nConsider the **`{}help gif`** option..'.format(self.config['prefix']),
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
    async def play(self, ctx, *, song : str):
        """
        Plays a song.
        If there is a song currently in the queue, then it is
        queued until the next song is done playing.
        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```Python\n{}: {}\n```'
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=fmt.format(type(e).__name__, e),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['error'])
        else:
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player)
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Enqueued ' + str(entry),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int = None):
        """
        Sets the volume of the currently playing song.
        """
        if value is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='If you don\'t know how loud you want your volume\nI can\'t help you. Maybe `{}help volume` can'.format(self.config['prefix']),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return

        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Set the volume to {:.0%}'.format(player.volume),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """
        Pauses the currently played song.
        """
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Done. Use `{}resume` if u like to listen again'.format(self.config['prefix']),
                              colour=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """
        Resumes the currently played song.
        """
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='Done. You can pause anytime you want.\nJust use `{}pause` to pause'.format(self.config['prefix']),
                              colour=0xf20006)
        last_message = await self.bot.say(embed=embed)
        await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        """
        Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """

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


    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """
        Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

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
                                      description='Skip vote added, currently at [{}/3]'.format(total_votes),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='You have already voted to skip this song.',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['error'])

    @commands.command(pass_context=True, no_pm=True, name='np')
    async def playing(self, ctx):
        """
        Shows info about the currently played song.
        """

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
                                  description='Now playing {} [skips: {}/3]'.format(state.current, skip_count),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


def setup(bot):
    bot.add_cog(Music(bot))