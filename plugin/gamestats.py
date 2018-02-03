import json
from discord.ext import commands
import discord
import aiohttp


class GameStats:
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
                embed.set_footer(text='Data © Rainbow Six Siege contributors, https://r6stats.com/')

                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Player **{}** not found'.format(uplay_name),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])


    @commands.command(pass_context=True)
    async def rs3(self, ctx, *, account: str = None):
        """Shows your Runescape 3 stats.
        Use your Runescape 3 username for this command"""

        if account is None:
            embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                  description="I wonder if i could sell you on the market instead :moneybag:, use `{}help rs3` instead".format(self.config['prefix']),
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
                if data['rank'] is None:
                    rank = 'Not played'
                else:
                    rank = data['rank']

                embed = discord.Embed(title='{} | {}:'.format(ctx.message.author.name, data['name']),
                                      description='Ranked: **{}**\nCombat LVL: **{}**\nTotal XP: **{}**\nOnline: **{}**'.format(
                                          rank, data['combatlevel'], data['totalxp'], data['loggedIn']
                                      ),
                                      colour=0xf20006)

                for item in data['skillvalues']:
                    if item['id'] == 0:
                        attack = item['level']
                    if item['id'] == 3:
                        constitution = item['level']
                    if item['id'] == 14:
                        mining = item['level']
                    if item['id'] == 2:
                        strength = item['level']
                    if item['id'] == 16:
                        agility = item['level']
                    if item['id'] == 13:
                        smithing = item['level']
                    if item['id'] == 1:
                        defence = item['level']
                    if item['id'] == 15:
                        herblore = item['level']
                    if item['id'] == 10:
                        fishing = item['level']
                    if item['id'] == 4:
                        ranged = item['level']
                    if item['id'] == 17:
                        thieving = item['level']
                    if item['id'] == 7:
                        cooking = item['level']
                    if item['id'] == 5:
                        prayer = item['level']
                    if item['id'] == 12:
                        crafting = item['level']
                    if item['id'] == 11:
                        firemaking = item['level']
                    if item['id'] == 6:
                        magic = item['level']
                    if item['id'] == 9:
                        fletching = item['level']
                    if item['id'] == 8:
                        woodcutting = item['level']
                    if item['id'] == 20:
                        runecrafting = item['level']
                    if item['id'] == 18:
                        slayer = item['level']
                    if item['id'] == 19:
                        farming = item['level']
                    if item['id'] == 22:
                        construction = item['level']
                    if item['id'] == 21:
                        hunter = item['level']
                    if item['id'] == 23:
                        summoning = item['level']
                    if item['id'] == 24:
                        dungeoneering = item['level']
                    if item['id'] == 25:
                        divination = item['level']
                    if item['id'] == 26:
                        invention = item['level']

                icon = {"Crafting": "<:Crafting:406361343168610305>",
                        "Agility": "<:Agility:406361343210553344>",
                        "Constitution": "<:Constitution:406361343222874112>",
                        "Attack": "<:Attack:406361343223136256>",
                        "Ranged": "<:Ranged:406361343298502658>",
                        "Construction":"<:Construction:406361343302565888>",
                        "Thieving": "<:Thieving:406361343302696962>",
                        "Defence": "<:Defence:406361343348834304>",
                        "Fletching": "<:Fletching:406361343353159691>",
                        "Strength": "<:Strength:406361343357222914>",
                        "Cooking": "<:Cooking:406361343361548298>",
                        "Divination": "<:Divination:406361343374131211>",
                        "Dungeoneering": "<:Dungeoneering:406361343386451979>",
                        "Slayer": "<:Slayer:406361343407685633>",
                        "Hunter": "<:Hunter:406361343474532353>",
                        "Smithing": "<:Smithing:406361343487115265>",
                        "Mining": "<:Mining:406361343583584256>",
                        "Fishing": "<:Fishing:406361343583846410>",
                        "Invention": "<:Invention:406361343591972864>",
                        "Runecrafting": "<:Runecrafting:406361343596298250>",
                        "Woodcutting": "<:Woodcutting:406361343718064128>",
                        "Firemaking": "<:Firemaking:406361343718064129>",
                        "Summoning": "<:Summoning:406361343843631107>",
                        "blank": "<:blank:406378361418547201>",
                        "Farming": "<:Farming:406361343407423498>",
                        "Prayer": "<:Prayer:406361343445434390>",
                        "Magic": "<:Magic:406361343608881152>",
                        "Herblore": "<:Herblore:406361343554355210>"}

                embed.add_field(name='**Attack**', value='{}{}'.format(icon['Attack'], attack), inline=True)
                embed.add_field(name='**Constitution**', value='{}{}'.format(icon['Constitution'], constitution), inline=True)
                embed.add_field(name='**Mining**', value='{}{}'.format(icon['Mining'], mining), inline=True)
                embed.add_field(name='**Strength**', value='{}{}'.format(icon['Strength'], strength), inline=True)
                embed.add_field(name='**Agility**', value='{}{}'.format(icon['Agility'], agility), inline=True)
                embed.add_field(name='**Smithing**', value='{}{}'.format(icon['Smithing'], smithing), inline=True)
                embed.add_field(name='**Defence**', value='{}{}'.format(icon['Defence'], defence), inline=True)
                embed.add_field(name='**Herblore**', value='{}{}'.format(icon['Herblore'], herblore), inline=True)
                embed.add_field(name='**Fishing**', value='{}{}'.format(icon['Fishing'], fishing), inline=True)
                embed.add_field(name='**Ranged**', value='{}{}'.format(icon['Ranged'], ranged), inline=True)
                embed.add_field(name='**Thieving**', value='{}{}'.format(icon['Thieving'], thieving), inline=True)
                embed.add_field(name='**Cooking**', value='{}{}'.format(icon['Cooking'], cooking), inline=True)
                embed.add_field(name='**Prayer**', value='{}{}'.format(icon['Prayer'], prayer), inline=True)
                embed.add_field(name='**Crafting**', value='{}{}'.format(icon['Crafting'], crafting), inline=True)
                embed.add_field(name='**Firemaking**', value='{}{}'.format(icon['Firemaking'], firemaking), inline=True)
                embed.add_field(name='**Magic**', value='{}{}'.format(icon['Magic'], magic), inline=True)
                embed.add_field(name='**Fletching**', value='{}{}'.format(icon['Fletching'], fletching), inline=True)
                embed.add_field(name='**Woodcutting**', value='{}{}'.format(icon['Woodcutting'], woodcutting), inline=True)
                embed.add_field(name='**Runecrafting**', value='{}{}'.format(icon['Runecrafting'], runecrafting), inline=True)
                embed.add_field(name='**Slayer**', value='{}{}'.format(icon['Slayer'], slayer), inline=True)
                embed.add_field(name='**Farming**', value='{}{}'.format(icon['Farming'], farming), inline=True)
                embed.add_field(name='**Construction**', value='{}{}\n**Dungeoneering**\n{}{}'.format(icon['Construction'], construction, icon['Dungeoneering'], dungeoneering), inline=True)
                embed.add_field(name='**Hunter**', value='{}{}\n**Divination**\n{}{}'.format(icon['Hunter'], hunter, icon['Divination'], divination), inline=True)
                embed.add_field(name='**Summoning**', value='{}{}\n**Invention**\n{}{}'.format(icon['Summoning'], summoning, icon['Invention'], invention), inline=True)
                # embed.add_field(name='**Dungeoneering**', value='{}{}'.format(icon['Dungeoneering'], dungeoneering), inline=True)
                # embed.add_field(name='**Divination**', value='{}{}'.format(icon['Divination'], divination), inline=True)
                # embed.add_field(name='Invention', value='{}{}'.format(icon['Invention'], Invention), inline=True)

                embed.set_footer(text='Data © Runescape contributors, https://apps.runescape.com/runemetrics/app/welcome')

                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['succes'])
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Player **{}** not found'.format(old_account_name),
                                      colour=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])

def setup(bot):
    bot.add_cog(GameStats(bot))