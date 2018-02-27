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
            print(COOR, row, column)

        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!battleship2 <{row}> <{column}> <{multiplayer}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

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

        def create_game(self, ID, board_str, score_int, col_int, row_str, last_message_id, online_bool, enemy_id):
            gamehash = random.getrandbits(128)
            online_bool = 'False'
            enemy_id = 'False'
            self.database.cur.execute(f"INSERT INTO botzilla.battleship (ID, gamehash, board, score, ship_row, ship_col) VALUES ('{ID}', '{gamehash}', '{board_str}', '{score_int}', '{row_str}', '{col_int}', {last_message_id}, {online_bool}, {enemy_id});")
            self.database.conn.commit()
            self.database.cur.execute("ROLLBACK;")
            return


        def check_game(self, ID):
            # Check if game exist, needs user ID
            try:
                print('Looking for user')
                self.database.cur.execute(f"select * from botzilla.battleship where ID = '{ID}'")
                game = self.database.cur.fetchone()
                self.database.cur.execute("ROLLBACK;")
                if game is None:
                    return False
                else:
                    return True
            except Exception as e:
                print('User not found')
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

        def player_in_battle(self, ctx):
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=f'User **`{multiplayer}`** has already a battle going.\nTry again later..',
                                  colour=0xf20006)
            a = self.bot.say(embed=embed)
            self.bot.add_reaction(a, self.emojiUnicode['warning'])


        # botzilla.battleship
        #     ID bigserial primary key,
        #     gamehash varchar(508),
        #     board varchar(1700),
        #     score varchar(508),
        #     ship_row varchar(508),
        #     ship_col varchar(508),
        #     last_message varchar(508),
        #     online VARCHAR(508),
        #     enemy VARCHAR(508)

        if multiplayer:
            if multiplayer.id == ctx.message.author.id: return
            try:
                if check_game(self, multiplayer.id):
                    print(f'player {multiplayer} found')
                    try:
                        board = get_board(self, int(multiplayer.id))
                    except Exception as e:
                        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                              description=f'Error requesting user **`{multiplayer}`**"\n```py\n{print_exception()}\n{e.args}\n```',
                                              colour=0xf20006)
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, self.emojiUnicode['error'])
                        return

                    if check_if_board_empty(board):
                        print(f'board {multiplayer.id} is empty')
                        if 'False' in str(get_online(self, multiplayer.id)):
                            print(f'{multiplayer} not yet in a online game')
                            update_COOR(self, multiplayer.id, column, row)
                            print(f'COOR have been updated by enemy player, {ctx.message.author.name}')
                            update_enemy(self, multiplayer.id, ctx.message.author.id, True)
                            print(f'{ctx.message.author.name} started a match against {multiplayer}')
                        else:
                            print(f'{multiplayer} had already a multiplayer game going on')
                            player_in_battle(self, ctx)
                            return

                    else:
                        # To do - notify user who already has a game that another user wants to play.
                        # Give them the option to quit the current game they are in.
                        print('board is not empty')
                        player_in_battle(self, ctx)
                        return
                else:
                    # If player is not yet found, create brand new player
                    pass

            # Error message if anything breaks
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f'Error requesting user **`{multiplayer}`**"\n```py\n{print_exception()}\n{e.args}\n```',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                return



        #
        # self.database.cur.execute(f"select * from botzilla.battleship where ID = {ctx.message.author.id};")
        # game = self.database.cur.fetchone()
        # self.database.cur.execute("ROLLBACK;")
        # self.database.cur.execute(f"select last_message from botzilla.battleship where ID = {ctx.message.author.id};")
        # last_message_id = self.database.cur.fetchone()
        # self.database.cur.execute("ROLLBACK;")
        #
        # if last_message_id:
        #     try:
        #         message_2_remove = await self.bot.get_message(ctx.message.channel, last_message_id[0])
        #         await self.bot.delete_message(message_2_remove)
        #     except Exception as e:
        #         pass
        #
        # If no game for user, Make game for user
        # if game is None:
        #     board = []
        #     for x in range(0, 10):
        #         board.append(['O'] * 10)
        #     score = 0
        #     ship_row = random.randint(0, len(board) - 1)
        #     ship_col = random.randint(0, len(board[0]) - 1)
        #     board_db_insert = str(board).replace("'", "<A>").replace(",", "<C>") # make seperater for db, A for ' C for ,
        #
        #     print(f"INSERT INTO botzilla.battleship (ID, gamehash, board, score) VALUES ({ctx.message.author.id}, {random.getrandbits(128)}, '{board_db_insert}', {score}, {ship_row}, {ship_col});")
        #     self.database.cur.execute(f"INSERT INTO botzilla.battleship (ID, gamehash, board, score, ship_row, ship_col) VALUES ({ctx.message.author.id}, {random.getrandbits(128)}, '{board_db_insert}', {score}, {ship_row}, {ship_col});")
        #     self.database.conn.commit()
        #     self.database.cur.execute("ROLLBACK;")
        #
        # # Get user game
        # self.database.cur.execute(f"select * from botzilla.battleship where ID = {ctx.message.author.id};")
        # game = self.database.cur.fetchone()
        # self.database.cur.execute("ROLLBACK;")
        #
        # # define fetch variables
        # id = int(game[0])
        # gamehash = int(game[1])
        # gamehash_lenght = len(str(gamehash)) // 2
        # gamehash_str = str(gamehash)
        # gamehash_1 = gamehash_str[:gamehash_lenght]
        # gamehash_2 = gamehash_str[gamehash_lenght:]
        # board = ast.literal_eval(str(game[2]).replace("<A>", "'").replace('<C>', ','))
        # score = int(game[3])
        # ship_row = int(game[4])
        # ship_col = int(game[5])
        # if ctx.message.author.id in self.owner_list:
        #     print(f'ANSWER : {int(ship_row) + 1} : {int(ship_col) + 1}')
        #
        # # if no column or row show game board and info about game... TO DO
        # if column is None or row is None:
        #     header = f"{random.choice(self.battleship_emoji_text['boats_emoji'])} {self.battleship_emoji_text['one']} {self.battleship_emoji_text['two']} {self.battleship_emoji_text['three']} {self.battleship_emoji_text['four']} {self.battleship_emoji_text['five']} {self.battleship_emoji_text['six']} {self.battleship_emoji_text['seven']} {self.battleship_emoji_text['eight']} {self.battleship_emoji_text['nine']} {self.battleship_emoji_text['ten']} "
        #     row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_6 = str(" ".join(board[5])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_7 = str(" ".join(board[6])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_8 = str(" ".join(board[7])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_9 = str(" ".join(board[8])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_10 = str(" ".join(board[9])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
        #                           description=f"{self.battleship_emoji_text['bb']}{self.battleship_emoji_text['a']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['l']}{self.battleship_emoji_text['e']}{self.battleship_emoji_text['s']}{self.battleship_emoji_text['h']}{self.battleship_emoji_text['i']}{self.battleship_emoji_text['p']}*V1.0*\n\nScore: **`{score}`**\n\n"
        #                                       f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}\n{self.battleship_emoji_text['six']} {row_6}\n{self.battleship_emoji_text['seven']} {row_7}\n{self.battleship_emoji_text['eight']} {row_8}\n{self.battleship_emoji_text['nine']} {row_9}\n{self.battleship_emoji_text['ten']} {row_10}"
        #                                       f"\n\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
        #                           colour=0xf20006)
        #     embed.set_footer(text='PuffDip#5369 ©')
        #     a = await self.bot.say(embed=embed)
        #     await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        #     self.database.cur.execute(f"UPDATE botzilla.battleship SET last_message = '{a.id}' where ID = {id} and gamehash = '{gamehash}';")
        #     self.database.conn.commit()
        #     self.database.cur.execute("ROLLBACK;")
        #     return
        #
        # # make sure user input is a number when exist
        # try:
        #     user_row = int(row) - 1
        #     user_col = int(column) - 1
        # except Exception as e:
        #     embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
        #                           description='Please make sure the column and row you provided are numbers',
        #                           colour=0xf20006)
        #     a = await self.bot.say(embed=embed)
        #     await self.bot.add_reaction(a, self.emojiUnicode['error'])
        #     self.database.cur.execute(f"UPDATE botzilla.battleship SET last_message = '{a.id}' where ID = {id} and gamehash = '{gamehash}';")
        #     self.database.conn.commit()
        #     self.database.cur.execute("ROLLBACK;")
        #     return
        #
        # # debug print
        # # print(f'ID : {id}\nGameHash : {gamehash}\nBoard : {board}\nScore : {score}\nSHIP\nship row: {ship_row}\nship_col: {ship_col}\n###\nUser row: {int(user_row) + 1}\nUser col: {int(user_col) + 1}')
        #
        # #if user wins
        # if user_row == ship_row and user_col == ship_col:
        #     board[user_row][user_col] = "2"
        #     header = f"{random.choice(self.battleship_emoji_text['boats_emoji'])} {self.battleship_emoji_text['one']} {self.battleship_emoji_text['two']} {self.battleship_emoji_text['three']} {self.battleship_emoji_text['four']} {self.battleship_emoji_text['five']} {self.battleship_emoji_text['six']} {self.battleship_emoji_text['seven']} {self.battleship_emoji_text['eight']} {self.battleship_emoji_text['nine']} {self.battleship_emoji_text['ten']} "
        #     row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_6 = str(" ".join(board[5])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_7 = str(" ".join(board[6])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_8 = str(" ".join(board[7])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_9 = str(" ".join(board[8])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #     row_10 = str(" ".join(board[9])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #
        #     embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
        #                           description=f"{self.battleship_emoji_text['bb']}{self.battleship_emoji_text['a']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['l']}{self.battleship_emoji_text['e']}{self.battleship_emoji_text['s']}{self.battleship_emoji_text['h']}{self.battleship_emoji_text['i']}{self.battleship_emoji_text['p']}*V1.0*\n\n**`DIRECT HIT`**\n\nScore: **`{score}`**\n\n"
        #                                       f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}\n{self.battleship_emoji_text['six']} {row_6}\n{self.battleship_emoji_text['seven']} {row_7}\n{self.battleship_emoji_text['eight']} {row_8}\n{self.battleship_emoji_text['nine']} {row_9}\n{self.battleship_emoji_text['ten']} {row_10}"
        #                                       f"\n\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
        #                           colour=0xf20006)
        #     embed.set_footer(text='PuffDip#5369 ©')
        #     embed.set_thumbnail(url=random.choice(self.battleship_emoji_text['exploded_boats']))
        #     a = await self.bot.say(embed=embed)
        #     await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        #
        #     self.database.cur.execute(f"UPDATE botzilla.battleship SET last_message = '{a.id}' where ID = {id} and gamehash = '{gamehash}';")
        #     self.database.conn.commit()
        #     self.database.cur.execute("ROLLBACK;")
        #
        #     board = []
        #     for x in range(0, 10):
        #         board.append(['O'] * 10)
        #     ship_row = random.randint(0, len(board) - 1)
        #     ship_col = random.randint(0, len(board[0]) - 1)
        #     board_db_insert = str(board).replace("'", "<A>").replace(",", "<C>")  # make seperater for db, A for ' C for ,
        #     score += 1
        #     self.database.cur.execute(f"UPDATE botzilla.battleship SET board = '{board_db_insert}', score = {score}, ship_row = {ship_row},ship_col = {ship_col} where ID = {id} and gamehash = '{gamehash}';")
        #     self.database.conn.commit()
        #     self.database.cur.execute("ROLLBACK;")
        #
        #
        # else:
        #     if user_row not in range(10) or user_col not in range(10):
        #         header = f"{random.choice(self.battleship_emoji_text['boats_emoji'])} {self.battleship_emoji_text['one']} {self.battleship_emoji_text['two']} {self.battleship_emoji_text['three']} {self.battleship_emoji_text['four']} {self.battleship_emoji_text['five']} {self.battleship_emoji_text['six']} {self.battleship_emoji_text['seven']} {self.battleship_emoji_text['eight']} {self.battleship_emoji_text['nine']} {self.battleship_emoji_text['ten']} "
        #         row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_6 = str(" ".join(board[5])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_7 = str(" ".join(board[6])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_8 = str(" ".join(board[7])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_9 = str(" ".join(board[8])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_10 = str(" ".join(board[9])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
        #                               description=f"{self.battleship_emoji_text['bb']}{self.battleship_emoji_text['a']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['l']}{self.battleship_emoji_text['e']}{self.battleship_emoji_text['s']}{self.battleship_emoji_text['h']}{self.battleship_emoji_text['i']}{self.battleship_emoji_text['p']}*V1.0*\n\n**`Out of range`**\n\nScore: **`{score}`**\n\n"
        #                                           f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}\n{self.battleship_emoji_text['six']} {row_6}\n{self.battleship_emoji_text['seven']} {row_7}\n{self.battleship_emoji_text['eight']} {row_8}\n{self.battleship_emoji_text['nine']} {row_9}\n{self.battleship_emoji_text['ten']} {row_10}"
        #                                           f"\n\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
        #                               colour=0xf20006)
        #         embed.set_footer(text='PuffDip#5369 ©')
        #         embed.set_thumbnail(url=random.choice(self.battleship_emoji_text['unexploded_boats']))
        #         a = await self.bot.say(embed=embed)
        #         await self.bot.add_reaction(a, self.emojiUnicode['warning'])
        #
        #         self.database.cur.execute(
        #             f"UPDATE botzilla.battleship SET last_message = '{a.id}' where ID = {id} and gamehash = '{gamehash}';")
        #         self.database.conn.commit()
        #         self.database.cur.execute("ROLLBACK;")
        #
        #     elif board[user_row][user_col] == '1':
        #         header = f"{random.choice(self.battleship_emoji_text['boats_emoji'])} {self.battleship_emoji_text['one']} {self.battleship_emoji_text['two']} {self.battleship_emoji_text['three']} {self.battleship_emoji_text['four']} {self.battleship_emoji_text['five']} {self.battleship_emoji_text['six']} {self.battleship_emoji_text['seven']} {self.battleship_emoji_text['eight']} {self.battleship_emoji_text['nine']} {self.battleship_emoji_text['ten']} "
        #         row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_6 = str(" ".join(board[5])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_7 = str(" ".join(board[6])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_8 = str(" ".join(board[7])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_9 = str(" ".join(board[8])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_10 = str(" ".join(board[9])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
        #                               description=f"{self.battleship_emoji_text['bb']}{self.battleship_emoji_text['a']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['l']}{self.battleship_emoji_text['e']}{self.battleship_emoji_text['s']}{self.battleship_emoji_text['h']}{self.battleship_emoji_text['i']}{self.battleship_emoji_text['p']}*V1.0*\n\n**You already shot in that direction!**\n\nScore: **`{score}`**\n\n"
        #                                           f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}\n{self.battleship_emoji_text['six']} {row_6}\n{self.battleship_emoji_text['seven']} {row_7}\n{self.battleship_emoji_text['eight']} {row_8}\n{self.battleship_emoji_text['nine']} {row_9}\n{self.battleship_emoji_text['ten']} {row_10}"
        #                                           f"\n\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
        #                               colour=0xf20006)
        #         embed.set_footer(text='PuffDip#5369 ©')
        #         embed.set_thumbnail(url=random.choice(self.battleship_emoji_text['unexploded_boats']))
        #         a = await self.bot.say(embed=embed)
        #         await self.bot.add_reaction(a, self.emojiUnicode['warning'])
        #
        #         self.database.cur.execute(
        #             f"UPDATE botzilla.battleship SET last_message = '{a.id}' where ID = {id} and gamehash = '{gamehash}';")
        #         self.database.conn.commit()
        #         self.database.cur.execute("ROLLBACK;")
        #
        #     else:
        #         board[user_row][user_col] = "3"
        #         header = f"{random.choice(self.battleship_emoji_text['boats_emoji'])} {self.battleship_emoji_text['one']} {self.battleship_emoji_text['two']} {self.battleship_emoji_text['three']} {self.battleship_emoji_text['four']} {self.battleship_emoji_text['five']} {self.battleship_emoji_text['six']} {self.battleship_emoji_text['seven']} {self.battleship_emoji_text['eight']} {self.battleship_emoji_text['nine']} {self.battleship_emoji_text['ten']} "
        #         row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_6 = str(" ".join(board[5])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_7 = str(" ".join(board[6])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_8 = str(" ".join(board[7])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_9 = str(" ".join(board[8])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         row_10 = str(" ".join(board[9])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
        #         embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
        #                               description=f"{self.battleship_emoji_text['bb']}{self.battleship_emoji_text['a']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['l']}{self.battleship_emoji_text['e']}{self.battleship_emoji_text['s']}{self.battleship_emoji_text['h']}{self.battleship_emoji_text['i']}{self.battleship_emoji_text['p']}*V1.0*\n\n**`MISS`**\n\nScore: **`{score}`**\n\n"
        #                                           f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}\n{self.battleship_emoji_text['six']} {row_6}\n{self.battleship_emoji_text['seven']} {row_7}\n{self.battleship_emoji_text['eight']} {row_8}\n{self.battleship_emoji_text['nine']} {row_9}\n{self.battleship_emoji_text['ten']} {row_10}"
        #                                           f"\n\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
        #                               colour=0xf20006)
        #         embed.set_footer(text='PuffDip#5369 ©')
        #         embed.set_thumbnail(url=self.battleship_emoji_text['boat_miss'])
        #         a = await self.bot.say(embed=embed)
        #         await self.bot.add_reaction(a, self.emojiUnicode['succes'])
        #
        #         board[user_row][user_col] = "1"
        #         board_db_insert = str(board).replace("'", "<A>").replace(",", "<C>")  # make seperater for db, A for ' C for ,
        #         self.database.cur.execute(f"UPDATE botzilla.battleship SET board = '{board_db_insert}', last_message = '{a.id}' where ID = {id} and gamehash = '{gamehash}';")
        #         self.database.conn.commit()
        #         self.database.cur.execute("ROLLBACK;")
        #
        # if ctx.message.author.id in owner_list:
        #     await self.bot.say(f'{check_board(board)}\n\n{check_if_board_empty(board)}')
        #
        # # # If anything goes wrong, Raise exeption
        # # except Exception as e:
        # #     embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
        # #                           description='Something went wrong, please notify me with **`{}report <How the error came up>`**\nError:\n**``{} : {}``**'.format(self.config['prefix'], type(e).__name__, e),
        # #                           colour=0xf20006)
        # #     embed.set_footer(text='PuffDip#5369 ©')
        # #     a = await self.bot.say(embed=embed)
        # #     await self.bot.add_reaction(a, self.emojiUnicode['error'])

def setup(bot):
    bot.add_cog(TestScripts(bot))
