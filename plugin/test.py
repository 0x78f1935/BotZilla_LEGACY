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
            await self.bot.send_typing(ctx.message.channel)
            try:
                url = "https://api.r6stats.com/api/v1/players/{}?platform=uplay".format(uplay_name)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        source = await response.json(encoding='utf8')

                test = json.dumps(source, indent=2)
                print(test)

                source = json.dumps(source)
                data = json.loads(str(source))

                last_updated = datetime.datetime.strptime(str(data['player']['updated_at']), '%Y-%m-%dT%H:%M:%S.%fZ')
                last_updated = str(last_updated).split('.')
                last_updated = last_updated[0]

                embed = discord.Embed(
                    title='{} | {}:'.format(ctx.message.author.name, data['player']['username']),
                    description=f"The following stats are last updated:\n```py\n{last_updated}\n```",
                    colour=0xf20006
                )

                embed.add_field(
                    name='Ranked',
                    value=f"Participation: **`{data['player']['stats']['ranked']['has_played']}`**\n"
                          f"Wins: **`{data['player']['stats']['ranked']['wins']}`**\n"
                          f"Losses: **`{data['player']['stats']['ranked']['losses']}`**\n"
                          f"W/L Ratio: **`{data['player']['stats']['ranked']['wlr']}`**\n"
                          f"Kills: **`{data['player']['stats']['ranked']['kills']}`**\n"
                          f"Deaths: **`{data['player']['stats']['ranked']['deaths']}`**\n"
                          f"K/D Ratio: **`{data['player']['stats']['ranked']['kd']}`**\n"
                          f"Playtime: **`{data['player']['stats']['ranked']['playtime']}`**\n\n",
                    inline=True
                )

                embed.add_field(
                    name='Casual',
                    value=f"Participation: **`{data['player']['stats']['casual']['has_played']}`**\n"
                          f"Wins: **`{data['player']['stats']['casual']['wins']}`**\n"
                          f"Losses: **`{data['player']['stats']['casual']['losses']}`**\n"
                          f"W/L Ratio: **`{data['player']['stats']['casual']['wlr']}`**\n"
                          f"Kills: **`{data['player']['stats']['casual']['kills']}`**\n"
                          f"Deaths: **`{data['player']['stats']['casual']['deaths']}`**\n"
                          f"K/D Ratio: **`{data['player']['stats']['casual']['kd']}`**\n"
                          f"Playtime: **`{data['player']['stats']['casual']['playtime']}`**\n\n",
                    inline=True
                )

                embed.add_field(
                    name='Overall',
                    value=f"Headshots: **`{data['player']['stats']['overall']['headshots']}`**\n"
                          f"Revives: **`{data['player']['stats']['overall']['revives']}`**\n"
                          f"Suicides: **`{data['player']['stats']['overall']['suicides']}`**\n"
                          f"Reinforcements Deployed: **`{data['player']['stats']['overall']['reinforcements_deployed']}`**\n"
                          f"Barricades Built: **`{data['player']['stats']['overall']['barricades_built']}`**\n"
                          f"Steps Moved: **`{data['player']['stats']['overall']['steps_moved']}`**\n"
                          f"Bullets Fired: **`{data['player']['stats']['overall']['bullets_fired']}`**\n"
                          f"Bullets Hit: **`{data['player']['stats']['overall']['bullets_hit']}`**",
                    inline=True
                )

                embed.set_footer(text='Data © Rainbow Six Siege contributors, https://r6stats.com/')
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Player **`{}`** not found'.format(uplay_name),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])


def setup(bot):
    bot.add_cog(TestScripts(bot))