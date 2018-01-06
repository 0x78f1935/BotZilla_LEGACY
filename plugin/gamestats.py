import urllib.request
import urllib.parse
import json
from discord.ext import commands
import discord
import aiohttp


class Leagues:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']


    @commands.command(pass_context=True)
    async def r6s(self, ctx, *, uplay_name=None):
        """Shows your Rainbow Six Siege stats.
        Use your Uplay username for this command"""

        if uplay_name is None:
            embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                  description="I hope you play the tutorial if you play a new game..\nTry `{}help r6s` instead".format(self.config['prefix']),
                                  color=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return
        else:
            url = "https://api.r6stats.com/api/v1/players/{}?platform=uplay".format(uplay_name)
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    source = await response.json()
            source = str(source).replace('\'', '"')
            print(source)
            data = json.loads(str(source))
            template = """
```Python
Player : [PLAYER]
Platform : [PLATFORM]
Level : [LVL]
XP : [XP]

The following stats are last updated around
[DATE]

Stats >>
    Ranked
        Participation : [RANKDEEDMEE]
        Wins : [RANKWIN]
        Losses: [RANKLOS]
        W/L Ratio : [RANKWLR]
        Kills : [RANKKIL]
        Deaths : [RANKDEAD]
        K/D Ratio : [RANKKD]
        Playtime : [RANKPLAY]

    Casual
        Participation : [CASDEEDMEE]
        Wins : [CASWIN]
        Losses: [CASLOS]
        W/L Ratio : [CASWL]
        Kills : [CASKILL]
        Deaths : [CASDEAD]
        K/D Ratio : [CASKD]
        Playtime : [CASPLAY]

    Overall
        Revives : [REV]
        Suicides : [SUC]
        Reinforcements Deployed: [RD]
        Barricades Built : [BB]
        Steps Moved : [SM]
        Bullets Fired : [BF]
        Bullets Hit : [BH]
        Headshots : [H]
        Melee Kills : [MELEE]
        Penetration Kills : [PENKILL]
        Assists : [ASSIST]
```
        """
            template = template.replace("[PLAYER]", str(data['player']['username']))
            template = template.replace("[PLATFORM]", str(data['player']['platform']))
            template = template.replace("[LVL]", str(data['player']['stats']['progression']['level']))
            template = template.replace("[XP]", str(data['player']['stats']['progression']['xp']))
            template = template.replace("[DATE]", str(data['player']['updated_at']))
            template = template.replace("[RANKDEEDMEE]", str(data['player']['stats']['ranked']['has_played']))
            template = template.replace("[RANKWIN]", str(data['player']['stats']['ranked']['wins']))
            template = template.replace("[RANKLOS]", str(data['player']['stats']['ranked']['losses']))
            template = template.replace("[RANKWLR]", str(data['player']['stats']['ranked']['wlr']))
            template = template.replace("[RANKKIL]", str(data['player']['stats']['ranked']['kills']))
            template = template.replace("[RANKDEAD]", str(data['player']['stats']['ranked']['deaths']))
            template = template.replace("[RANKKD]", str(data['player']['stats']['ranked']['kd']))
            template = template.replace("[RANKPLAY]", str(data['player']['stats']['ranked']['playtime']))
            template = template.replace("[CASDEEDMEE]", str(data['player']['stats']['casual']['has_played']))
            template = template.replace("[CASWIN]", str(data['player']['stats']['casual']['wins']))
            template = template.replace("[CASLOS]", str(data['player']['stats']['casual']['losses']))
            template = template.replace("[CASWL]", str(data['player']['stats']['casual']['wlr']))
            template = template.replace("[CASKILL]", str(data['player']['stats']['casual']['kills']))
            template = template.replace("[CASDEAD]", str(data['player']['stats']['casual']['deaths']))
            template = template.replace("[CASKD]", str(data['player']['stats']['casual']['kd']))
            template = template.replace("[CASPLAY]", str(data['player']['stats']['casual']['playtime']))
            template = template.replace("[REV]", str(data['player']['stats']['overall']['revives']))
            template = template.replace("[SUC]", str(data['player']['stats']['overall']['suicides']))
            template = template.replace("[RD]", str(data['player']['stats']['overall']['reinforcements_deployed']))
            template = template.replace("[BB]", str(data['player']['stats']['overall']['barricades_built']))
            template = template.replace("[SM]", str(data['player']['stats']['overall']['steps_moved']))
            template = template.replace("[BF]", str(data['player']['stats']['overall']['bullets_fired']))
            template = template.replace("[BH]", str(data['player']['stats']['overall']['bullets_hit']))
            template = template.replace("[H]", str(data['player']['stats']['overall']['headshots']))
            template = template.replace("[MELEE]", str(data['player']['stats']['overall']['melee_kills']))
            template = template.replace("[PENKILL]", str(data['player']['stats']['overall']['penetration_kills']))
            template = template.replace("[ASSIST]", str(data['player']['stats']['overall']['assists']))
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=template,
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])

def setup(bot):
    bot.add_cog(Leagues(bot))