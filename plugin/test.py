import json
import discord
from discord.ext import commands
import aiohttp

import datetime


try:
    from plugin.database import Database
except:
    pass

class TestScripts:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']

        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except Exception as e:
            print('Test: Database files not found - {}'.format(e.args))
            pass


    @commands.command(pass_context=True)
    async def test(self, ctx, *, uplay_name=None):
        """
        Shows your Rainbow Six Siege stats.
        Use your Uplay username for this command
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!r6s <{uplay_name}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if uplay_name is None:
            embed = discord.Embed(title="{}:".format(ctx.message.author.name),
                                  description="I hope you play the tutorial if you play a new game..\nTry **`{}help r6s`** instead".format(self.config['prefix']),
                                  color=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return
        else:
            try:
                url = "https://api.r6stats.com/api/v1/players/{}?platform=uplay".format(uplay_name)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        source = await response.json(encoding='utf8')

                test = json.dumps(source, indent=2)
                print(test)

                source = json.dumps(source)

                data = json.loads(str(source))
                embed = discord.Embed(title='{} | {}:'.format(ctx.message.author.name, data['player']['username']),
                                      description='The following stats are last updated around\n```{}```'.format(data['player']['updated_at']),
                                      colour=0xf20006)
                embed.add_field(name='Ranked', value='Participation: {}'.format(data['player']['stats']['ranked']['has_played']), inline=True)
                embed.add_field(name='Casual', value='Participation: {}'.format(data['player']['stats']['casual']['has_played']), inline=True)
                embed.add_field(name='Overall', value='Headshots: {}'.format(data['player']['stats']['overall']['headshots']), inline=True)

                embed.add_field(name='Wins', value=data['player']['stats']['ranked']['wins'], inline=True)
                embed.add_field(name='Wins', value=data['player']['stats']['casual']['wins'], inline=True)
                embed.add_field(name='Revives', value=data['player']['stats']['overall']['revives'], inline=True)

                embed.add_field(name='Losses', value=data['player']['stats']['ranked']['losses'], inline=True)
                embed.add_field(name='Losses', value=data['player']['stats']['casual']['losses'], inline=True)
                embed.add_field(name='Suicides', value=data['player']['stats']['overall']['suicides'], inline=True)

                embed.add_field(name='W/L Ratio', value=data['player']['stats']['ranked']['wlr'], inline=True)
                embed.add_field(name='W/L Ratio', value=data['player']['stats']['casual']['wlr'], inline=True)
                embed.add_field(name='Reinforcements Deployed', value=data['player']['stats']['overall']['reinforcements_deployed'], inline=True)

                embed.add_field(name='Kills', value=data['player']['stats']['ranked']['kills'], inline=True)
                embed.add_field(name='Kills', value=data['player']['stats']['casual']['kills'], inline=True)
                embed.add_field(name='Barricades Built', value=data['player']['stats']['overall']['barricades_built'], inline=True)

                embed.add_field(name='Deaths', value=data['player']['stats']['ranked']['deaths'], inline=True)
                embed.add_field(name='Deaths', value=data['player']['stats']['casual']['deaths'], inline=True)
                embed.add_field(name='Steps Moved', value=data['player']['stats']['overall']['steps_moved'], inline=True)

                embed.add_field(name='K/D Ratio', value=data['player']['stats']['ranked']['kd'], inline=True)
                embed.add_field(name='K/D Ratio', value=data['player']['stats']['casual']['kd'], inline=True)
                embed.add_field(name='Bullets Fired', value=data['player']['stats']['overall']['bullets_fired'], inline=True)

                embed.add_field(name='Playtime', value=data['player']['stats']['ranked']['playtime'], inline=True)
                embed.add_field(name='Playtime', value=data['player']['stats']['casual']['playtime'], inline=True)
                embed.add_field(name='Bullets Hit', value=data['player']['stats']['overall']['bullets_hit'], inline=True)
                embed.set_footer(text='Data © Rainbow Six Siege contributors, https://r6stats.com/')

                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Player **{}** not found'.format(uplay_name),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])


def setup(bot):
    bot.add_cog(TestScripts(bot))