import asyncio
import discord
import re
from enum import Enum
from discord.ext import commands
from math import ceil
from collections import namedtuple, deque
import json
from options import checks
from discord.ext.commands.cooldowns import BucketType
try:
    from plugin.database import Database
except:
    pass


class PlayerType(Enum):
    YOUTUBE = 0
    LOCAL = 1


class VoiceEntry:
    def __init__(self, message, player, playerType=PlayerType.LOCAL):
        self.requester = message.author
        self.channel = message.channel
        self.player = player
        self.playerType = playerType

    def __str__(self):
        fmt = '*{0.title}* uploaded by {0.uploader} and requested by {1.display_name}'
        try:
            if self.player.duration:
                fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(self.player.duration, 60))
        except Exception:
            print("no duration found")
        finally:
            try:
                return fmt.format(self.player, self.requester)
            except Exception as e:
                print(str(e))
                return '*A locally stored file* uploaded by @zhu.exe, probably, and requested by {0.display_name}'.format(
                    self.requester)


class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.can_skip = True
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()  # a set of user_ids that voted
        self.skip_threshold = 3
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())
        self.opts = {
            'default_search': 'auto',
            'quiet': True,
            'no_playlist': True,
        }

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    def update_skip_threshold(self, vChannel):
        numUsers = len(vChannel.voice_members)
        self.skip_threshold = ceil((numUsers - 1) * 0.4)
        print("updated skip threshold: " + str(self.skip_threshold))

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
            self.play_next_song.clear()  # make sure we wait until the next song is done
            self.current = await self.songs.get()  # grab the current song
            await self.bot.send_typing(self.current.channel)
            if self.current.playerType == PlayerType.YOUTUBE:
                self.current.player = await self.voice.create_ytdl_player(self.current.player.url,
                                                                          ytdl_options=self.opts,
                                                                          after=self.toggle_next, use_avconv=True)
            await self.bot.send_message(self.current.channel, 'Now playing ' + str(self.current))
            self.update_skip_threshold(self.voice.channel)
            self.current.player.start()
            self.can_skip = True
            await self.play_next_song.wait()


class Music:
    """Voice related commands.

        Works in multiple servers at once.
        """

    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}
        self.USE_AVCONV = True

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
    async def queue(self, ctx, *, args=''):
        """Says the music queue.
        Usage:
        .queue
            [remove QUEUENUM] (Requires Bot Mod or Manage Messages)"""
        state = self.get_voice_state(ctx.message.server)

        if not state.is_playing():
            await self.bot.say('Not playing any music right now...')
            return

        queue = state.songs._queue

        if 'remove' not in args:
            queueStr = "```"
            totalDuration = 0
            for pos, s in enumerate(queue):
                try:
                    totalDuration += s.player.duration
                except:
                    pass
            queueStr += "Length of queued songs: {}\n".format(str(timedelta(seconds=totalDuration)))
            queueStr += "\nNow Playing: {}".format(
                state.current.player.title if state.current.player.title else "Unknown Song")
            for pos, s in enumerate(queue):
                queueStr += "\n{0}: {1}".format(pos + 1,
                                                s.player.title if s.player.title is not None else "Unknown Song")
            queueStr += "```"

            await self.bot.say(queueStr)
        elif checks.mod_or_permissions(manage_messages=True):
            try:
                to_remove = int(args.split('remove ')[1]) - 1
                if to_remove < 0:
                    raise Exception
            except:
                await self.bot.say("Incorrect usage. Use .help queue for help.")
                return

            try:
                removed = queue[to_remove]
                queue.remove(queue[to_remove])
                await self.bot.say("Removed {}.".format(removed.player.title))
            except Exception as e:
                await self.bot.say("Something went wrong trying to remove a song: {}".format(e))
        else:
            raise commands.CheckFailure

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def play(self, ctx, *, song: str):
        """Plays a song.

            If there is a song currently in the queue, then it is
            queued until the next song is done playing.

            Cooldown: 5 sec
            """

        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
            'no_playlist': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next,
                                                          use_avconv=self.USE_AVCONV)
        except Exception as e:
            fmt = 'An error occurred while processing this request: ```py\n{}: {}\n```'
            await self.bot.send_message(ctx.message.channel, fmt.format(type(e).__name__, e))
        else:
            if player.duration > 18000:
                await self.bot.say("Please request a song that is less than 5 hours long.")
                return
            player.volume = 0.6
            entry = VoiceEntry(ctx.message, player, playerType=PlayerType.YOUTUBE)
            await self.bot.say('Enqueued ' + str(entry))
            await state.songs.put(entry)


    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, *, value=None):
        """Sets the volume of the currently playing song.
        Use it like `!volume 80`"""
        if value is None:
            embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                  description='Use `{}help volume` to start a volume tutorial!'.format(self.config['prefix']),
                                  color=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return
        try:
            value = int(value)
            state = self.get_voice_state(ctx.message.server)
            if state.is_playing():
                player = state.player
                player.volume = value / 100
                embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                      description='Set the volume to {:.0%}'.format(player.volume),
                                      color=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        except ValueError:
            embed = discord.Embed(title="{}".format("Volume"),
                                  description='Are you drunk? Consider using `{}help volume` instead.'.format(self.config['prefix']),
                                  color=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        """Pauses the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Music is paused, use **`{}resume`** to unpause'.format(self.config['prefix']),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        """Resumes the currently played song."""
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Music is unpaused, use **`{}pause`** to pause'.format(self.config['prefix']),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


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
        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass
        finally:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Succesfully disconnected, Call me agian with **`{}summon`**'.format(self.config['prefix']),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.
        3 skip votes are needed for the song to be skipped.
        """

        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format('Not playing any music right now...'),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['error'])
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format('Requester requested skipping song...'),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='{}'.format('Skip vote passed, skipping song...'),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
                state.skip()
            else:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Skip vote added, currently at [{}/3]'.format(total_votes),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
        else:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format('You have already voted to skip this song.'),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])


    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        """Shows info about the currently played song."""

        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format('Not playing anything.'),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
        else:
            skip_count = len(state.skip_votes)
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Now playing **{}**\n[skips: {}/3]'.format(state.current, skip_count),
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])


def setup(bot):
    bot.add_cog(Music(bot))