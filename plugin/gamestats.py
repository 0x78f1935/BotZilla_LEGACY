import json
from discord.ext import commands
import discord
import aiohttp
import datetime



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


    @commands.command(pass_context=True)
    async def rs3(self, ctx, *, account: str = None):
        """
        Shows your Runescape 3 stats.
        Use your Runescape 3 username for this command
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!rs3 <{account}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if account is None:
            embed = discord.Embed(title="{}:".format(ctx.message.author.name),
                                  description="I wonder if i could sell you on the market instead :moneybag:, use **`{}help rs3`** instead".format(self.config['prefix']),
                                  color=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return
        else:
            old_account_name = account
            await self.bot.send_typing(ctx.message.channel)
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


    @commands.command(pass_context=True)
    async def osrs(self, ctx, *, account: str = None):
        """
        Shows your Oldschool Runscape stats.
        Use your Oldschool Runscape username for this command
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!osrs <{account}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if account is None:
            embed = discord.Embed(title="{}:".format(ctx.message.author.name),
                                  description="This is not that kind of a fantasy game, use **`{}help osrs`** instead".format(self.config['prefix']),
                                  color=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['warning'])
            return
        else:
            old_account = account
            await self.bot.send_typing(ctx.message.channel)
            try:
                if ' ' in account:
                    account = account.replace(' ', '%20')

                url = 'http://services.runescape.com/m=hiscore_oldschool/index_lite.ws?player={}'.format(account)
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as response:
                        source = await response.read()
                source = source.decode('utf-8')
                source = str(source).replace('\n', ',')
                source = source.split(',')
                lvl = []
                a = 0
                b  = 3
                for i in range(24):
                    result = tuple(source[a:b])
                    lvl.append(result)
                    a = a + 3
                    b = b + 3

                prayer_lvl = round(float(lvl[6][1])) // 2
                hp_defence = float(lvl[2][1]) + float(lvl[4][1])
                tmp_combat = prayer_lvl + hp_defence
                base_lvl = tmp_combat / 4
                ranged_lvl = float(lvl[3][1]) + float(lvl[1][1])

                melee_combat_lvl = ranged_lvl * 0.325
                combat_lvl = int(base_lvl + melee_combat_lvl)
                icon = {"Crafting": "<:Crafting:411683889099046924>",
                        "Fletching": "<:Fletching:411683889099309068>",
                        "Agility": "<:Agility:411683889116086273>",
                        "Construction": "<:Construction:411683889132601367>",
                        "Farming": "<:Farming:411683889229070348>",
                        "Ranged": "<:Ranged:411683889258692649>",
                        "Cooking": "<:Cooking:411683889291984897>",
                        "Slayer": "<:Slayer:411683889304698892>",
                        "Defence": "<:Defence:411683889308893195>",
                        "Runecrafting": "<:Runecrafting:411683889396842517>",
                        "Hunter": "<:Hunter:411683889476534272>",
                        "Firemaking": "<:Firemaking:411683889476534332>",
                        "Hitpoints": "<:Hitpoints:411683889510088704>",
                        "Mining": "<:Mining:411683889522671626>",
                        "Herblore": "<:Herblore:411683889526865920>",
                        "Attack": "<:Attack:411683889527128064>",
                        "Magic": "<:Magic:411683889552031764>",
                        "Thieving": "<:Thieving:411683889556226069>",
                        "Prayer": "<:Prayer:411683889581654016>",
                        "Strength": "<:Strength:411683889585586176>",
                        "Smithing": "<:Smithing:411683889594236928>",
                        "Fishing": "<:Fishing:411683889636048898>",
                        "Woodcutting": "<:Woodcutting:411683889694638090>",
                        "Overall": "<:Overall:411686480071622656>"}


                for item in icon:
                    if 'Attack' in item:
                        attack = f'{icon["Attack"]} **`{lvl[1][1]}`**'
                    if 'Defence' in item:
                        defence = f'{icon["Defence"]} **`{lvl[2][1]}`**'
                    if 'Strength' in item:
                        strength = f'{icon["Strength"]} **`{lvl[3][1]}`**'
                    if 'Hitpoints' in item:
                        hitpoints = f'{icon["Hitpoints"]} **`{lvl[4][1]}`**'
                    if 'Ranged' in item:
                        ranged = f'{icon["Ranged"]} **`{lvl[5][1]}`**'
                    if 'Prayer' in item:
                        prayer = f'{icon["Prayer"]} **`{lvl[6][1]}`**'
                    if 'Magic' in item:
                        magic = f'{icon["Magic"]} **`{lvl[7][1]}`**'
                    if 'Cooking' in item:
                        cooking = f'{icon["Cooking"]} **`{lvl[8][1]}`**'
                    if 'Woodcutting' in item:
                        woodcutting = f'{icon["Woodcutting"]} **`{lvl[9][1]}`**'
                    if 'Fletching' in item:
                        fletching = f'{icon["Fletching"]} **`{lvl[10][1]}`**'
                    if 'Fishing' in item:
                        fishing = f'{icon["Fishing"]} **`{lvl[11][1]}`**'
                    if 'Firemaking' in item:
                        firemaking = f'{icon["Firemaking"]} **`{lvl[12][1]}`**'
                    if 'Crafting' in item:
                        crafting = f'{icon["Crafting"]} **`{lvl[13][1]}`**'
                    if 'Smithing' in item:
                        smithing = f'{icon["Smithing"]} **`{lvl[14][1]}`**'
                    if 'Mining' in item:
                        mining = f'{icon["Mining"]} **`{lvl[15][1]}`**'
                    if 'Herblore' in item:
                        herblore = f'{icon["Herblore"]} **`{lvl[16][1]}`**'
                    if 'Agility' in item:
                        agility = f'{icon["Agility"]} **`{lvl[17][1]}`**'
                    if 'Thieving' in item:
                        thieving = f'{icon["Thieving"]} **`{lvl[18][1]}`**'
                    if 'Slayer' in item:
                        slayer = f'{icon["Slayer"]} **`{lvl[19][1]}`**'
                    if 'Farming' in item:
                        farming = f'{icon["Farming"]} **`{lvl[20][1]}`**'
                    if 'Runecrafting' in item:
                        runecrafting = f'{icon["Runecrafting"]} **`{lvl[21][1]}`**'
                    if 'Hunter' in item:
                        hunter = f'{icon["Hunter"]} **`{lvl[22][1]}`**'
                    if 'Construction' in item:
                        construction = f'{icon["Construction"]} **`{lvl[23][1]}`**'

                embed = discord.Embed(title='{} | {}:'.format(ctx.message.author.name, old_account),
                                      description='Combat LVL: **`{}`**\tOverall LVL: **`{}`**'.format(combat_lvl, lvl[0][1]),
                                      colour=0xf20006)
                embed.add_field(name='**Attack**', value=attack, inline=True)
                embed.add_field(name='**Hitpoints**', value=hitpoints, inline=True)
                embed.add_field(name='**Mining**', value=mining, inline=True)
                embed.add_field(name='**Strength**', value=strength, inline=True)
                embed.add_field(name='**Agility**', value=agility, inline=True)
                embed.add_field(name='**Smithing**', value=smithing, inline=True)
                embed.add_field(name='**Defence**', value=defence, inline=True)
                embed.add_field(name='**Herblore**', value=herblore, inline=True)
                embed.add_field(name='**Fishing**', value=fishing, inline=True)
                embed.add_field(name='**Ranged**', value=ranged, inline=True)
                embed.add_field(name='**Thieving**', value=thieving, inline=True)
                embed.add_field(name='**Cooking**', value=cooking, inline=True)
                embed.add_field(name='**Prayer**', value=prayer, inline=True)
                embed.add_field(name='**Crafting**', value=crafting, inline=True)
                embed.add_field(name='**Firemaking**', value=firemaking, inline=True)
                embed.add_field(name='**Magic**', value=magic, inline=True)
                embed.add_field(name='**Fletching**', value=fletching, inline=True)
                embed.add_field(name='**Woodcutting**', value=woodcutting, inline=True)
                embed.add_field(name='**Runecrafting**', value=runecrafting, inline=True)
                embed.add_field(name='**Slayer**', value=slayer, inline=True)
                embed.add_field(name='**Farming**', value=farming, inline=True)
                embed.add_field(name='**Construction**', value=construction, inline=True)
                embed.add_field(name='**Hunter**',value=hunter, inline=True)
                embed.add_field(name='-', value='-', inline=True)

                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            except Exception as e:
                print(e.args)
                embed = discord.Embed(title="{}:".format(ctx.message.author.name),
                                      description='User **`{}`** not found :cry:'.format(old_account),
                                      color=0xf20006)
                last_message = await self.bot.say(embed=embed)
                await self.bot.add_reaction(last_message, self.emojiUnicode['error'])

def setup(bot):
    bot.add_cog(GameStats(bot))