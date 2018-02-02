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
            try:
                url = "https://api.r6stats.com/api/v1/players/{}?platform=uplay".format(uplay_name)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        source = await response.json(encoding='utf8')

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

                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Player **{}** not found'.format(uplay_name),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])


    @commands.command(pass_context=True, hidden=True)
    async def rs3(self, ctx, *, account: str = None):
        """Shows your Runescape 3 stats.
        Use your Runescape 3 username for this command"""

        if account is None:
            embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                  description="I wonder if i could sell you on the market :moneybag:, use `{}help rs3` instead".format(self.config['prefix']),
                                  color=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return
        else:
            old_account_name = account
            try:
                if ' ' in account:
                    account = account.replace(' ', '%20')

                url = "https://apps.runescape.com/runemetrics/profile?user={}".format(account)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        source = await response.json(encoding='utf8')

                source = json.dumps(source)
                data = json.loads(str(source))
                if data['rank'] == 'null':
                    rank = 'Not played'
                else:
                    rank = data['rank']

                embed = discord.Embed(title='{} | {}:'.format(ctx.message.author.name, data['name']),
                                      description='User: **{}**\nRanked: **{}**\nCombat LVL: **{}**\nMelee XP: **{}**\nRanged XP: **{}**\nMagic XP: **{}**\nTotal XP: **{}**\nOnline: **{}**'.format(
                                          data['name'], rank, data['combatlevel'], data['melee'], data['ranged'], data['magic'], data['totalxp'], data['loggedIn']
                                      ),
                                      colour=0xf20006)

                for item in data['skillvalues']:
                    if item['id'] is 0:
                        embed.add_field(name='**Attack**', value=item['level'], inline=True)

                    if item['id'] is 3:
                        embed.add_field(name='**Constitution**', value=item['level'], inline=True)

                    if item['id'] is 14:
                        embed.add_field(name='**Mining**', value=item['level'], inline=True)

                    if item['id'] is 2:
                        embed.add_field(name='**Strength**', value=item['level'], inline=True)

                    if item['id'] is 16:
                        embed.add_field(name='**Agility**', value=item['level'], inline=True)

                    if item['id'] is 13:
                        embed.add_field(name='**Smithing**', value=item['level'], inline=True)

                    if item['id'] is 1:
                        embed.add_field(name='**Defence**', value=item['level'], inline=True)

                    if item['id'] is 15:
                        embed.add_field(name='**Herblore**', value=item['level'], inline=True)

                    if item['id'] is 10:
                        embed.add_field(name='**Fishing**', value=item['level'], inline=True)

                    if item['id'] is 4:
                        embed.add_field(name='**Ranged**', value=item['level'], inline=True)

                    if item['id'] is 17:
                        embed.add_field(name='**Thieving**', value=item['level'], inline=True)

                    if item['id'] is 7:
                        embed.add_field(name='**Cooking**', value=item['level'], inline=True)

                    if item['id'] is 5:
                        embed.add_field(name='**Prayer**', value=item['level'], inline=True)

                    if item['id'] is 12:
                        embed.add_field(name='**Crafting**', value=item['level'], inline=True)

                    if item['id'] is 11:
                        embed.add_field(name='**Firemaking**', value=item['level'], inline=True)

                    if item['id'] is 6:
                        embed.add_field(name='**Magic**', value=item['level'], inline=True)

                    if item['id'] is 9:
                        embed.add_field(name='**Fletching**', value=item['level'], inline=True)

                    if item['id'] is 8:
                        embed.add_field(name='**Woodcutting**', value=item['level'], inline=True)

                    if item['id'] is 20:
                        embed.add_field(name='**Runecrafting**', value=item['level'], inline=True)

                    if item['id'] is 18:
                        embed.add_field(name='**Slayer**', value=item['level'], inline=True)

                    if item['id'] is 19:
                        embed.add_field(name='**Farming**', value=item['level'], inline=True)

                    if item['id'] is 22:
                        embed.add_field(name='**Construction**', value=item['level'], inline=True)

                    if item['id'] is 21:
                        embed.add_field(name='**Hunter**', value=item['level'], inline=True)

                    if item['id'] is 23:
                        embed.add_field(name='**Summoning**', value=item['level'], inline=True)

                    if item['id'] is 24:
                        embed.add_field(name='**Dungeoneering**', value=item['level'], inline=True)

                    if item['id'] is 25:
                        embed.add_field(name='**Divination**', value=item['level'], inline=True)

                    if item['id'] is 26:
                        embed.add_field(name='Invention', value=item['level'], inline=True)
                embed.set_footer(text='Data © Runescape contributors, https://apps.runescape.com/')

                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Player **{}** not found'.format(old_account_name),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])

def setup(bot):
    bot.add_cog(Leagues(bot))