import discord
from discord.ext import commands
import json
import datetime
import random
import aiohttp
import ast
import os
import sys
import re
try:
    from plugin.database import Database
except Exception as e:
    pass

tmp_config = json.loads(str(open('./options/config.js').read()))
config = tmp_config['config']
owner_list = config['owner-id']


class TestScripts:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.battleship_emoji = json.loads(str(open('./options/battleship.js').read()))
        self.battleship_emoji_text = self.battleship_emoji['text']
        self.battleship_emoji_ascii = self.battleship_emoji['ascii']
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


    @commands.group(pass_context=True, hidden=True)
    async def hello(self, ctx):
        """
        This is a group with commands
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!hello in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        if ctx.invoked_subcommand is None:
            message = 'Hello {}'.format(ctx.message.author.name)
            embed = discord.Embed(title="{}".format(ctx.message.author.name),
                                  description="```**{}**```".format(message),
                                  color=0xf20006)
            embed.set_author(name="Example", url="http://www.example.com",
                          icon_url="https://cdn.discordapp.com/icons/265828729970753537/0c4fc42c61804747b54300282d0d7629.jpg")
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True)
    async def sebisauce(self, ctx):
        """
        Sebisauce, api
        """
        url = 'https://sebisauce.herokuapp.com/api/random'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                data = await response.json(encoding='utf8')

        im = data['file']
        embed = discord.Embed(title='\t', description='\t', color=0xf20006)
        embed.set_image(url=im)
        embed.set_footer(text="Data © Sebi\'s Bot Tutorial contributors, discord.gg/GWdhBSp")
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True)
    async def sebisauce_old(self, ctx):
        """
        Sebisauce, not api
        """
        await self.bot.send_typing(ctx.message.channel)
        sebisauce_img = ['https://cdn.discordapp.com/attachments/407238426417430539/414844386212446210/sebisauce_3.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844423382368277/sebisauce_1.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844448367968276/sebisauce_2.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844479519064064/sebisauce_6.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844498779176961/sebisauce_8.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844517032787979/sebisauce_9.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844533898084352/sebisauce_10.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844552730640384/sebisauce_12.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844574385569794/sebisauce_13.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844592048046090/sebisauce_14.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414844605885054976/sebisauce_15.png',
                         'https://media.discordapp.net/attachments/407238426417430539/414860605976084490/unknown.png']

        url = random.choice(sebisauce_img)
        embed = discord.Embed(title="\t",
                              description="\t",
                              color=0xf20006)
        embed.set_image(url=url)
        await self.bot.say(embed=embed)

#######################################################################################################################

    @commands.command(pass_context=True, aliases=["b2"])
    async def battleship2(self, ctx, COOR = None, multiplayer : discord.Member = None):
        """
        dev version
        """

        if ctx.message.author.id not in self.owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Only the owner of this bot can use this command',
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        # We need to make sure the user always give COOR as argument unless user want to see their profile
        if COOR:
            columns = {"a" : 1, "b" : 2, "c" : 3, "d" : 4, "e" : 5, "f" : 6, "g" : 7, "h" : 8, "i" : 9, "j" : 10}
            COOR = re.findall(r'[A-Za-z]|-?\d+\.\d+|\d+', str(COOR))
            try:
                if int(COOR[1]) > 10 or str(COOR[0]).lower() not in columns.keys():
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description=f'To become a pirate, men have to read the map: **`{self.config["prefix"]}help battleship`**',
                                          colour=0xf20006)
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['error'])
                    return
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'To become a pirate, men have to read the map: **`{self.config["prefix"]}help battleship`**',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                return

            # define the COOR
            row = COOR[1]
            column = columns[str(COOR[0]).lower()]

        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!battleship2 <{column}> <{row}> <{multiplayer}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

        def print_exception():
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            error = f'{exc_type} : {fname} : {exc_tb.tb_lineno}'
            return error

        def check_board(board):
            # Returns board as str
            tmp = []
            for i in board:
                tmp.append(str(i))
            current_board = "\n".join(tmp)
            return current_board

        def check_if_board_empty(board):
            # Check if board has 100 * 0. If so, board is empty
            total = 0
            current_board = check_board(board)
            for i in current_board:
                if 'O' in i:
                    total += 1
            if int(total) == int(100):
                return True
            else:
                return False

        def create_game(self, ID):
            gamehash = random.getrandbits(128)
            board = []
            for x in range(0, 10):
                board.append(['O'] * 10)
            board_str = str(board).replace("'", "<A>").replace(",", "<C>") # make seperater for db, A for ' C for
            score_int = 0
            row_str = random.randint(0, len(board) - 1)
            col_int = random.randint(0, len(board[0]) - 1)
            last_message_id = 0
            online_bool = 'False'
            enemy_id = 0
            self.database.cur.execute(f"INSERT INTO botzilla.battleship (ID, gamehash, board, score, ship_row, ship_col, last_message, online, enemy) VALUES ('{ID}', '{gamehash}', '{board_str}', '{score_int}', '{row_str}', '{col_int}', {last_message_id}, {online_bool}, {enemy_id});")
            self.database.conn.commit()
            self.database.cur.execute("ROLLBACK;")
            return


        def check_game(self, ID):
            # Check if game exist, needs user ID
            try:
                self.database.cur.execute(f"select * from botzilla.battleship where ID = '{ID}'")
                game = self.database.cur.fetchone()
                self.database.cur.execute("ROLLBACK;")
                if game is None:
                    return False
                else:
                    return True
            except Exception as e:
                return False


        def get_board(self, ID):
            self.database.cur.execute(f"select * from botzilla.battleship where ID = '{ID}';")
            boardgame = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            board = ast.literal_eval(str(boardgame[2]).replace("<A>", "'").replace('<C>', ','))
            return board

        def get_online(self, ID):
            self.database.cur.execute(f"select * from botzilla.battleship where ID = '{ID}';")
            online = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            return online

        def get_last_message(self, ID):
            self.database.cur.execute(f"select last_message from botzilla.battleship where ID = '{ID}';")
            last_message = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            return last_message

        def update_gamehash(self, ID):
            gamehash = random.getrandbits(128)
            self.database.cur.execute(f"UPDATE botzilla.battleship SET gamehash = '{gamehash}' where ID = '{ID}';")
            self.database.conn.commit()
            self.database.cur.execute("ROLLBACK;")

        def update_board(self, ID, board):

            self.database.cur.execute(f"UPDATE botzilla.battleship SET board = '{board}' where ID = '{ID}';")
            self.database.conn.commit()
            self.database.cur.execute("ROLLBACK;")

        def update_score(self, ID, score):

            self.database.cur.execute(f"UPDATE botzilla.battleship SET score = '{score}' where ID = '{ID}';")
            self.database.conn.commit()
            self.database.cur.execute("ROLLBACK;")

        def update_COOR(self, ID, col, row):
            print(ID, col, row)
            self.database.cur.execute(f"UPDATE botzilla.battleship SET ship_row = '{row}', ship_col = '{col}' where ID = '{ID}';")
            self.database.conn.commit()
            self.database.cur.execute("ROLLBACK;")

        def update_enemy(self, ID, enemy, online):
            if online:
                self.database.cur.execute(f"UPDATE botzilla.battleship SET enemy = '{enemy}', online = 'True' where ID = '{ID}';")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
            else:
                self.database.cur.execute(f"UPDATE botzilla.battleship SET enemy = '{enemy}', online = 'False' where ID = '{ID}';")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")


        if multiplayer:
            # Uncomment for anti-cheat
            # if multiplayer.id == ctx.message.author.id: return

            # Remove leftovers
            last_message_id = get_last_message(self, ctx.message.author.id)
            try:
                message_2_remove = await self.bot.get_message(ctx.message.channel, last_message_id[0])
                await self.bot.delete_message(message_2_remove)
            except Exception as e:
                pass
            try:
                await self.bot.delete_message(ctx.message)
            except Exception as e:
                pass

            try:
                if check_game(self, multiplayer.id):
                    print(f'player {multiplayer} found')
                    try:
                        board = get_board(self, int(multiplayer.id))
                    except Exception as e:
                        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                              description=f'Error requesting user **`{multiplayer}`**\n```py\n{print_exception()}\n{e.args}\n```',
                                              colour=0xf20006)
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, self.emojiUnicode['error'])
                        self.database.cur.execute(f"UPDATE botzilla.battleship SET last_message = '{a.id}' where ID = '{ctx.message.author.id}';")
                        self.database.conn.commit()
                        self.database.cur.execute("ROLLBACK;")
                        return

                    if check_if_board_empty(board):
                        print(f'board {multiplayer.id} is empty')
                        if 'False' in str(get_online(self, multiplayer.id)):
                            print(f'{multiplayer} not yet in a online game')
                            update_COOR(self, multiplayer.id, column, row)
                            print(f'COOR have been updated by enemy player, {ctx.message.author.name}')
                            update_enemy(self, multiplayer.id, ctx.message.author.id, True)
                            print(f'{ctx.message.author.name} started a match against {multiplayer}')
                            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                                  description=f'Started a match against **`{multiplayer}`**',
                                                  colour=0xf20006)
                            a = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                            return
                        else:
                            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                                  description='User **`{}`** has already a battle going.\nTry again later..'.format(multiplayer),
                                                  colour=0xf20006)
                            embed.set_footer(text='PuffDip#5369 ©')
                            a = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                            print(f'{multiplayer} had already a multiplayer game going on')
                            return
                    elif not check_if_board_empty(board):
                        # To do - notify user who already has a game that another user wants to play.
                        # Give them the option to quit the current game they are in.
                        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                              description=f'User **`{multiplayer}`** has already a battle going.\nTry again later..',
                                              colour=0xf20006)
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                        print(f'board of {multiplayer} is not empty')
                        return
                else:
                    # If player is not yet found, create brand new player
                    create_game(self, multiplayer.id)
                    print(f'{multiplayer} not yet in a online game')
                    update_COOR(self, multiplayer.id, column, row)
                    print(f'COOR have been updated by enemy player, {ctx.message.author.name}')
                    update_enemy(self, multiplayer.id, ctx.message.author.id, True)
                    print(f'{ctx.message.author.name} started a match against {multiplayer}')
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description=f'Started a match against **`{multiplayer}`**',
                                          colour=0xf20006)
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                    return

            # Error message if anything breaks
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'Error requesting user **`{multiplayer}`**"\n```py\n{print_exception()}\n{e.args}\n```',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                self.database.cur.execute(f"UPDATE botzilla.battleship SET last_message = '{a.id}' where ID = '{ctx.message.author.id}';")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                return

        # Remove leftovers
        last_message_id = get_last_message(self, ctx.message.author.id)
        try:
            message_2_remove = await self.bot.get_message(ctx.message.channel, last_message_id[0])
            await self.bot.delete_message(message_2_remove)
        except Exception as e:
            pass
        try:
            await self.bot.delete_message(ctx.message)
        except Exception as e:
            pass

        # await update_enemy(self, ctx.message.author.id, 'None', False) # Verplaatsen zodat player states offline wordt gezet nadat speler gewonnen heeft

        # If no game for user, Make game for user
        if not check_game(self, ctx.message.author.id):
            await create_game(self, ctx.message.author.id)

            # make sure user input is a number when exist
            user_row = int(row) - 1
            user_col = int(column) - 1

            print(user_col, user_row)

def setup(bot):
    bot.add_cog(TestScripts(bot))
