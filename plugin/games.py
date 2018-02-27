from discord.ext import commands
import datetime
import json
import random
import discord
import asyncio
import ast
import sys
import os
import re
try:
    from plugin.database import Database
except Exception as e:
    pass


class Games:
    def __init__(self, bot):
        self.bot = bot
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']
        self.battleship_emoji = json.loads(str(open('./options/battleship.js').read()))
        self.battleship_emoji_text = self.battleship_emoji['text']
        self.battleship_emoji_ascii = self.battleship_emoji['ascii']

        try:
            self.database = Database(self.bot)
            self.database_file_found = True
        except Exception as e:
            print('games: Database files not found - {}'.format(e.args))
            pass


    @commands.command(pass_context=True, name='8ball')
    async def ball8(self, ctx , *, question: str = None):
        """
        8ball! Ask BotZilla Any question.
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!8ball <{question}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        question = question.lower()
        ball = random.randint(1, 20)

        # uncomment the following line to let the user now what number is picked by 8ball
        # ball_anaunce = await self.safe_send_message(channel, "8Ball chose number %s" % (ball))

        if question is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: You did not fully address your question!',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, self.emojiUnicode['Warning'])
            return

        if ball == 1:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: It is certain',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f605') # Done
            return

        if ball == 2:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: It is decidedly so',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f913') # Done
            return

        if ball == 3:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Without a doubt',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f611') # Done
            return

        if ball == 4:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Yes, definitely!',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f98b') # Done
            return

        if ball == 5:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: You may rely on it',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f60c') # Done
            return

        if ball == 6:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: As I see it, yes',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f48d') # Done
            return

        if ball == 7:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Most likely',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f609') # Done
            return

        if ball == 8:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Outlook good',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f44c') # done
            return

        if ball == 9:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Yes',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f525') # Done
            return

        if ball == 10:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Signs point to yes',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f607') # Done
            return

        if ball == 11:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Reply hazy try again',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f47b') # Done
            return

        if ball == 12:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Ask again later',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f550') # Done
            return

        if ball == 13:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Better not tell you now',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\u2620') # Done
            return

        if ball == 14:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Cannot predict now',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f914') # Done
            return

        if ball == 15:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Concentrate and ask again',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f616') # Done
            return

        if ball == 16:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Don\'t count on it',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f625') # Done
            return

        if ball == 17:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: My reply is no',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f4a9') # Done
            return

        if ball == 18:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: My sources say no',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f614') # Done
            return

        if ball == 19:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Outlook not so good',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f60f') # Done
            return

        if ball == 20:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description=':8ball: Very doubtful',
                                  colour=0xf20006)
            last_message = await self.bot.say(embed=embed)
            await self.bot.add_reaction(last_message, '\U0001f61f') # Done
            return


    @commands.command(pass_context=True, name='highlow')
    async def HighLow(self, ctx):
        """
        Higher or Lower? Gamble your way out! 0 ~ 1.000
        Is the next number higher or lower then your current number?
        Vote with the whole server!
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!highlow in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        while True:
            number = random.randrange(0,1000)
            embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                  description='Higher or Lower than: **`{}`**\n**`10`** Seconds to vote..'.format(number),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, '\U0001f53c')
            await self.bot.add_reaction(a, '\U0001f53d')
            await asyncio.sleep(10)
            new_number = random.randrange(0,1000)

            message = await self.bot.get_message(ctx.message.channel, a.id)
            more = message.reactions[0]
            less = message.reactions[1]
            total_more = more.count - 1
            total_less = less.count - 1
            total_votes = total_more + total_less
            vote_list = [total_more, total_less]
            winner = max(vote_list)
            await self.bot.delete_message(a)

            if total_votes == 0:
                embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                      description='GameOver! Nobody voted...\nUse **`{}highlow`** to start a new game'.format(self.config['prefix']),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, '\U0001f480')
                break

            elif total_less == total_more:
                embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                      description='Vote Draw!\nContinue? **`10`** Seconds remaining'.format(new_number),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                await self.bot.add_reaction(a, '\U0001f3f3')
                await asyncio.sleep(10)
                message = await self.bot.get_message(ctx.message.channel, a.id)
                emoji_continue = message.reactions[0]
                total_continue = emoji_continue.count - 1
                await self.bot.delete_message(a)
                if total_continue == 0:
                    embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                          description='Gameover! Nobody to play with...\nStart a new game with **`{}highlow`**'.format(self.config['prefix']),
                                          colour=0xf20006)
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, '\U0001f60f')
                    break


            elif winner == total_more and new_number >= number:
                embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                      description='Victorious! You hit number **`{}`**\nYour previous number was **`{}`**\n\nTotals\n-------\n:arrow_up_small: : **`{}`**    :arrow_down_small: : **`{}`**\nTotal Votes: **`{}`**\n\nNext round in **`10`** Seconds'.format(new_number, number, total_more, total_less, total_votes),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                await asyncio.sleep(10)
                await self.bot.delete_message(a)

            elif winner == total_less and new_number <= number:
                embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                      description='Victorious! You hit number **`{}`**\nYour previous number was **`{}`**\n\nTotals\n-------\n:arrow_up_small:  : **`{}`**    :arrow_down_small: : **`{}`**\nTotal Votes: **`{}`**\n\nNext round in **`10`** Seconds'.format(new_number, number, total_more, total_less, total_votes),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                await asyncio.sleep(10)
                await self.bot.delete_message(a)

            else:
                embed = discord.Embed(title='HighLow started by {}:'.format(ctx.message.author.name),
                                      description='GameOver! You hit number **`{}`**\nYour previous number was **`{}`**\n\nTotals\n-------\n:arrow_up_small:  : **`{}`**    :arrow_down_small: : **`{}`**\nTotal Votes: **`{}`**\n\nUse **`{}highlow`** for a new game!'.format(new_number, number, total_more, total_less, total_votes, self.config['prefix']),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, '\U0001f480')
                break

    @commands.cooldown(rate=1, per=2, type=commands.BucketType.user)
    @commands.command(pass_context=True, aliases=["b"])
    async def battleship(self, ctx, COOR = None, multiplayer : discord.Member = None):
        """
        Play Battleship the game!!
        Progress will be saved.

        alias = !!b

        Shows playground a.k.a map
            -  !!battleship
        Shoot
            -  !!battleship <COORDS>
        Example
            -  !!battleship G3
        Multiplayer
            - !!battleship <COORDS> <[player ping] | [name] | [ID]>
        Example Multiplayer
            - !!battleship G3 @puffdip#5369
            - !!battleship G3 puffdip
            - !!battleship G3 343549587853803531
        """

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
            self.brow = int(COOR[1]) - 1
            self.bcolumn = int(columns[str(COOR[0]).lower()]) - 1
        else:
            self.bcolumn = None
            self.brow = None



        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!battleship2 <{COOR}> <{multiplayer}> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')

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
                self.database.cur.execute(f"select * from botzilla.battleship where ID = '{ID}';")
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
            if online is None:
                return None
            else:
                return online

        def get_last_message(self, ID):
            self.database.cur.execute(f"select last_message from botzilla.battleship where ID = '{ID}';")
            last_message = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            return last_message

        def update_COOR(self, ID, col, row):
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
            print('multiplayer request found')
            # Uncomment for anti-cheat
            if multiplayer.id == ctx.message.author.id:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='You cannot play a multiplayer game with yourself :smirk:',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                print(f'Cannot play a multiplayer with yourself {multiplayer} vs {ctx.message.author}')
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

            try:
                if check_game(self, multiplayer.id):
                    print(f'player {multiplayer} found')
                    try:
                        await self.bot.get_user_info(multiplayer.id)
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
                            update_COOR(self, multiplayer.id, self.bcolumn, self.brow)
                            print(f'COOR have been updated by enemy player, {ctx.message.author.name}')
                            update_enemy(self, multiplayer.id, ctx.message.author.id, True)
                            print(f'Coords has been set\nStarted a match against **`{multiplayer}`**\n\n**`{multiplayer}`** :vs: **`{ctx.message.author}`**')
                            embed = discord.Embed(title='\t',
                                                  description=f'Coords has been set\nStarted a match against **{multiplayer.mention}**\n\n**`{multiplayer}`** :vs: **`{ctx.message.author}`**\n\nIf you are stuck\nuse **`{self.config["prefix"]}help battleship`**',
                                                  colour=0xf20006)
                            a = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                            send_dm_invite = await self.bot.get_user_info(multiplayer.id)
                            dm = await self.bot.send_message(send_dm_invite, embed=embed)
                            await self.bot.add_reaction(dm, self.emojiUnicode['succes'])
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
                    update_COOR(self, multiplayer.id, self.bcolumn, self.brow)
                    print(f'COOR have been updated by enemy player, {ctx.message.author.name}')
                    update_enemy(self, multiplayer.id, ctx.message.author.id, True)
                    print(f'{ctx.message.author.name} started a match against {multiplayer}')
                    embed = discord.Embed(title='\t',
                                          description=f'Coords has been set\nStarted a match against **{multiplayer.mention}**\n\n**`{multiplayer}`** :vs: **`{ctx.message.author}`**\n\nIf you are stuck\nuse **`{self.config["prefix"]}help battleship`**',
                                          colour=0xf20006)
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                    send_dm_invite = await self.bot.get_user_info(multiplayer.id)
                    dm = await self.bot.send_message(send_dm_invite, embed=embed)
                    await self.bot.add_reaction(dm, self.emojiUnicode['succes'])
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
        print('singleplayer request found')
        self.database.cur.execute(f"select last_message from botzilla.battleship where ID = {ctx.message.author.id};")
        last_message_id = self.database.cur.fetchone()
        self.database.cur.execute("ROLLBACK;")
        try:
            message_2_remove = await self.bot.get_message(ctx.message.channel, last_message_id[0])
            await self.bot.delete_message(message_2_remove)
        except Exception as e:
            pass
        try:
            await self.bot.delete_message(ctx.message)
        except Exception as e:
            pass

        await self.bot.send_typing(ctx.message.channel)

        try:
            self.database.cur.execute(f"select * from botzilla.battleship where ID = {ctx.message.author.id};")
            game = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")
            self.database.cur.execute(f"select last_message from botzilla.battleship where ID = {ctx.message.author.id};")
            last_message_id = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

            if last_message_id:
                try:
                    message_2_remove = await self.bot.get_message(ctx.message.channel, last_message_id[0])
                    await self.bot.delete_message(message_2_remove)
                except Exception as e:
                    pass

            # If no game for user, Make game for user
            if game is None:
                gamehash = random.getrandbits(128)
                board = []
                for x in range(0, 10):
                    board.append(['O'] * 10)
                board_str = str(board).replace("'", "<A>").replace(",", "<C>")  # make seperater for db, A for ' C for
                score_int = 0
                row_str = random.randint(0, len(board) - 1)
                col_int = random.randint(0, len(board[0]) - 1)
                last_message_id = 0
                online_bool = 'False'
                enemy_id = 0
                self.database.cur.execute(f"INSERT INTO botzilla.battleship (ID, gamehash, board, score, ship_row, ship_col, last_message, online, enemy) VALUES ('{ctx.message.author.id}', '{gamehash}', '{board_str}', '{score_int}', '{row_str}', '{col_int}', {last_message_id}, {online_bool}, {enemy_id});")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")

            # Get user game
            self.database.cur.execute(f"select * from botzilla.battleship where ID = '{ctx.message.author.id}';")
            game = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

            # define fetch variables
            id = int(game[0])
            gamehash = int(game[1])
            gamehash_lenght = len(str(gamehash)) // 2
            gamehash_str = str(gamehash)
            gamehash_1 = gamehash_str[:gamehash_lenght]
            gamehash_2 = gamehash_str[gamehash_lenght:]
            board = ast.literal_eval(str(game[2]).replace("<A>", "'").replace('<C>', ','))
            score = int(game[3])
            ship_row = int(game[4])
            ship_col = int(game[5])
            online = str(game[7])
            enemy = game[8]
            if ctx.message.author.id in self.owner_list:
                p = ['A','B','C','D','E','F', 'G', 'H', 'I', 'J']
                print(f'ANSWER : {p[int(ship_col)]} : {int(ship_row) + 1} ')

            # if no column or row show game board and info about game... TO DO
            if self.bcolumn is None or self.brow is None:
                header = f"{random.choice(self.battleship_emoji_text['boats_emoji'])} {self.battleship_emoji_text['a']} {self.battleship_emoji_text['b']} {self.battleship_emoji_text['c']} {self.battleship_emoji_text['d']} {self.battleship_emoji_text['e']} {self.battleship_emoji_text['f']} {self.battleship_emoji_text['g']} {self.battleship_emoji_text['h']} {self.battleship_emoji_text['i']} {self.battleship_emoji_text['j']}"
                row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_6 = str(" ".join(board[5])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_7 = str(" ".join(board[6])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_8 = str(" ".join(board[7])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_9 = str(" ".join(board[8])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_10 = str(" ".join(board[9])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f"{self.battleship_emoji_text['bb']}{self.battleship_emoji_text['a']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['l']}{self.battleship_emoji_text['e']}{self.battleship_emoji_text['s']}{self.battleship_emoji_text['h']}{self.battleship_emoji_text['i']}{self.battleship_emoji_text['p']}*V2.0*\n\nScore: **`{score}`**\n\n"
                                                  f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}\n{self.battleship_emoji_text['six']} {row_6}\n{self.battleship_emoji_text['seven']} {row_7}\n{self.battleship_emoji_text['eight']} {row_8}\n{self.battleship_emoji_text['nine']} {row_9}\n{self.battleship_emoji_text['ten']} {row_10}"
                                                  f"\n\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nThis is a map overview of your playground\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
                                      colour=0xf20006)
                if online != 'False' and int(enemy) != 0:
                    enemy_player = await self.bot.get_user_info(int(enemy))
                    embed.add_field(name='You are fighting against a player!', value=f'**`{enemy_player.name}`**')

                embed.set_footer(text='PuffDip#5369 ©')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                self.database.cur.execute(f"UPDATE botzilla.battleship SET last_message = '{a.id}' where ID = {id} and gamehash = '{gamehash}';")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")
                return

            #if user wins
            if self.brow == ship_row and self.bcolumn == ship_col:
                board[self.brow][self.bcolumn] = "2"
                header = f"{random.choice(self.battleship_emoji_text['boats_emoji'])} {self.battleship_emoji_text['a']} {self.battleship_emoji_text['b']} {self.battleship_emoji_text['c']} {self.battleship_emoji_text['d']} {self.battleship_emoji_text['e']} {self.battleship_emoji_text['f']} {self.battleship_emoji_text['g']} {self.battleship_emoji_text['h']} {self.battleship_emoji_text['i']} {self.battleship_emoji_text['j']}"
                row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_6 = str(" ".join(board[5])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_7 = str(" ".join(board[6])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_8 = str(" ".join(board[7])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_9 = str(" ".join(board[8])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                row_10 = str(" ".join(board[9])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])

                if online != 'False' and int(enemy) != 0:
                    enemy_player = await self.bot.get_user_info(int(enemy))
                    say_score = f'{score} + 3 | {enemy_player.name} ship sank'
                else:
                    say_score = f'{score} + 1 | AI ship sank'

                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f"{self.battleship_emoji_text['bb']}{self.battleship_emoji_text['a']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['t']}{self.battleship_emoji_text['l']}{self.battleship_emoji_text['e']}{self.battleship_emoji_text['s']}{self.battleship_emoji_text['h']}{self.battleship_emoji_text['i']}{self.battleship_emoji_text['p']}*V2.0*\n\n**`DIRECT HIT`**\n\nScore: **`{say_score}`**\n\n"
                                                  f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}\n{self.battleship_emoji_text['six']} {row_6}\n{self.battleship_emoji_text['seven']} {row_7}\n{self.battleship_emoji_text['eight']} {row_8}\n{self.battleship_emoji_text['nine']} {row_9}\n{self.battleship_emoji_text['ten']} {row_10}"
                                                  f"\n\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
                                      colour=0xf20006)
                if online != 'False' and int(enemy) != 0:
                    enemy_player = await self.bot.get_user_info(int(enemy))
                    embed.add_field(name='A player ship sank in perfect clear water..', value=f'**`{enemy_player.name}`** lost his ship')

                embed.set_footer(text='PuffDip#5369 ©')
                embed.set_thumbnail(url=random.choice(self.battleship_emoji_text['exploded_boats']))
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])

                board = []
                for x in range(0, 10):
                    board.append(['O'] * 10)
                board_str = str(board).replace("'", "<A>").replace(",", "<C>")  # make seperater for db, A for ' C for
                score_int = int(score) + 1
                if online != 'False' and enemy != '0':
                    score_int += 2
                row_str = random.randint(0, len(board) - 1)
                col_int = random.randint(0, len(board[0]) - 1)
                online_bool = 'False'
                enemy_id = 0

                self.database.cur.execute(f"UPDATE botzilla.battleship SET last_message = '{a.id}', score = '{score_int}', board = '{board_str}', online = '{online_bool}', enemy = '{enemy_id}', ship_row = '{row_str}', ship_col = '{col_int}' where ID = {id} and gamehash = '{gamehash}';")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")

            else:
                if board[self.brow][self.bcolumn] == '1':
                    header = f"{random.choice(self.battleship_emoji_text['boats_emoji'])} {self.battleship_emoji_text['a']} {self.battleship_emoji_text['b']} {self.battleship_emoji_text['c']} {self.battleship_emoji_text['d']} {self.battleship_emoji_text['e']} {self.battleship_emoji_text['f']} {self.battleship_emoji_text['g']} {self.battleship_emoji_text['h']} {self.battleship_emoji_text['i']} {self.battleship_emoji_text['j']}"
                    row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_6 = str(" ".join(board[5])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_7 = str(" ".join(board[6])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_8 = str(" ".join(board[7])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_9 = str(" ".join(board[8])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_10 = str(" ".join(board[9])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description=f"**You already shot in that direction!**\nScore: **`{score}`**\n\n"
                                                      f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}\n{self.battleship_emoji_text['six']} {row_6}\n{self.battleship_emoji_text['seven']} {row_7}\n{self.battleship_emoji_text['eight']} {row_8}\n{self.battleship_emoji_text['nine']} {row_9}\n{self.battleship_emoji_text['ten']} {row_10}"
                                                      f"\n\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
                                          colour=0xf20006)
                    if online != 'False' and int(enemy) != 0:
                        enemy_player = await self.bot.get_user_info(int(enemy))
                        embed.add_field(name='You are fighting against a player!', value=f'**`{enemy_player.name}`**')

                    embed.set_footer(text='PuffDip#5369 ©')
                    embed.set_thumbnail(url=random.choice(self.battleship_emoji_text['unexploded_boats']))
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['warning'])

                    self.database.cur.execute(
                        f"UPDATE botzilla.battleship SET last_message = '{a.id}' where ID = {id} and gamehash = '{gamehash}';")
                    self.database.conn.commit()
                    self.database.cur.execute("ROLLBACK;")

                else:
                    board[self.brow][self.bcolumn] = "3"
                    header = f"{random.choice(self.battleship_emoji_text['boats_emoji'])} {self.battleship_emoji_text['a']} {self.battleship_emoji_text['b']} {self.battleship_emoji_text['c']} {self.battleship_emoji_text['d']} {self.battleship_emoji_text['e']} {self.battleship_emoji_text['f']} {self.battleship_emoji_text['g']} {self.battleship_emoji_text['h']} {self.battleship_emoji_text['i']} {self.battleship_emoji_text['j']}"
                    row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_6 = str(" ".join(board[5])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_7 = str(" ".join(board[6])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_8 = str(" ".join(board[7])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_9 = str(" ".join(board[8])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_10 = str(" ".join(board[9])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description=f"**`MISS`**\nScore: **`{score}`**\n\n"
                                                      f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}\n{self.battleship_emoji_text['six']} {row_6}\n{self.battleship_emoji_text['seven']} {row_7}\n{self.battleship_emoji_text['eight']} {row_8}\n{self.battleship_emoji_text['nine']} {row_9}\n{self.battleship_emoji_text['ten']} {row_10}"
                                                      f"\n\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
                                          colour=0xf20006)
                    if online != 'False' and int(enemy) != 0:
                        enemy_player = await self.bot.get_user_info(int(enemy))
                        embed.add_field(name='You are fighting against a player!', value=f'**`{enemy_player.name}`**')

                    embed.set_footer(text='PuffDip#5369 ©')
                    embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/407238426417430539/417154157724827668/miss.jpg')
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['succes'])

                    board[self.brow][self.bcolumn] = "1"
                    board_db_insert = str(board).replace("'", "<A>").replace(",", "<C>")  # make seperater for db, A for ' C for ,
                    self.database.cur.execute(f"UPDATE botzilla.battleship SET board = '{board_db_insert}', last_message = '{a.id}' where ID = {id} and gamehash = '{gamehash}';")
                    self.database.conn.commit()
                    self.database.cur.execute("ROLLBACK;")

        # If anything goes wrong, Raise exeption
        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Something went wrong, please notify me with **`{}report <error below>`**\n**```{} : {}\n\n{}```**'.format(self.config['prefix'], type(e).__name__, e, print_exception()),
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip#5369 ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


def setup(bot):
    m = Games(bot)
    bot.add_cog(m)
