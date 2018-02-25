from discord.ext import commands
import datetime
import json
import random
import discord
import asyncio
import ast
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


    @commands.command(pass_context=True)
    async def battleship(self, ctx, row=None, *, column=None):
        """
        Play Battleship the game!!
        Progres will be saved.

        Shows playground
            -  !!battleship
        Shoot
            -  !!battleship <row> <column>
        Example
            -  !!battleship 4 2
        """
        print(f'{datetime.date.today()} {datetime.datetime.now()} - {ctx.message.author} ran command !!battleship <column> <row> in -- Channel: {ctx.message.channel.name} Guild: {ctx.message.server.name}')
        try:
            self.database.cur.execute(f"select * from botzilla.battleship where ID = {ctx.message.author.id}};")
            game = self.database.cur.fetchone()
            self.database.cur.execute("ROLLBACK;")

            # If no game for user, Make game for user
            if game == None:
                board = []
                for x in range(0, 5):
                    board.append(['O'] * 5)
                score = 0
                ship_row = random.randint(0, len(board) - 1)
                ship_col = random.randint(0, len(board[0]) - 1)
                board_db_insert = str(board).replace("'", "<A>").replace(",", "<C>") # make seperater for db, A for ' C for ,

                print(f"INSERT INTO botzilla.battleship (ID, gamehash, board, score) VALUES ({ctx.message.author.id}, {random.getrandbits(128)}, '{board_db_insert}', {score}, {ship_row}, {ship_col});")
                self.database.cur.execute(f"INSERT INTO botzilla.battleship (ID, gamehash, board, score, ship_row, ship_col) VALUES ({ctx.message.author.id}, {random.getrandbits(128)}, '{board_db_insert}', {score}, {ship_row}, {ship_col});")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")

            # Get user game
            self.database.cur.execute(f"select * from botzilla.battleship where ID = {ctx.message.author.id};")
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

            # if no column or row show game board and info about game... TO DO
            if column is None or row is None:
                header = f"{random.choice(self.battleship_emoji_text['boats'])} {self.battleship_emoji_text['one']} {self.battleship_emoji_text['two']} {self.battleship_emoji_text['three']} {self.battleship_emoji_text['four']} {self.battleship_emoji_text['five']} "
                row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f"Score: **`{score}`**\n\n"
                                                  f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}"
                                                  f"\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
                                      colour=0xf20006)
                embed.set_footer(text='PuffDip ©')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                return

            # make sure user input is a number when exist
            try:
                user_row = int(row) - 1
                user_col = int(column) - 1
            except Exception as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='Please make sure the column and row you provided are numbers',
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                return

            # debug print
            # print(f'ID : {id}\nGameHash : {gamehash}\nBoard : {board}\nScore : {score}\nSHIP\nship row: {ship_row}\nship_col: {ship_col}\n###\nUser row: {int(user_row) + 1}\nUser col: {int(user_col) + 1}')

            #if user wins
            if user_row == ship_row and user_col == ship_col:
                board[user_row][user_col] = "2"
                header = f"{random.choice(self.battleship_emoji_text['boats'])} {self.battleship_emoji_text['one']} {self.battleship_emoji_text['two']} {self.battleship_emoji_text['three']} {self.battleship_emoji_text['four']} {self.battleship_emoji_text['five']} "
                row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description=f"**`DIRECT HIT`**\nScore: **`{score}`**\n\n"
                                                  f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}"
                                                  f"\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
                                      colour=0xf20006)
                embed.set_footer(text='PuffDip ©')
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])
                board = []
                for x in range(0, 5):
                    board.append(['O'] * 5)
                board_db_insert = str(board).replace("'", "<A>").replace(",", "<C>")  # make seperater for db, A for ' C for ,
                score += 1
                self.database.cur.execute(f"UPDATE botzilla.battleship SET board = '{board_db_insert}', score = {score} where ID = {id} and gamehash = '{gamehash}';")
                self.database.conn.commit()
                self.database.cur.execute("ROLLBACK;")


            else:
                if user_row not in range(5) or user_col not in range(5):
                    header = f"{random.choice(self.battleship_emoji_text['boats'])} {self.battleship_emoji_text['one']} {self.battleship_emoji_text['two']} {self.battleship_emoji_text['three']} {self.battleship_emoji_text['four']} {self.battleship_emoji_text['five']} "
                    row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                    row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                    row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                    row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                    row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description=f"**`Out of range`**\nScore: **`{score}`**\n"
                                                      f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}"
                                                      f"\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
                                          colour=0xf20006)
                    embed.set_footer(text='PuffDip ©')
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                elif board[user_row][user_col] == '1':
                    header = f"{random.choice(self.battleship_emoji_text['boats'])} {self.battleship_emoji_text['one']} {self.battleship_emoji_text['two']} {self.battleship_emoji_text['three']} {self.battleship_emoji_text['four']} {self.battleship_emoji_text['five']} "
                    row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                    row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                    row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                    row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                    row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire'])
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description=f"**You already shot in that direction!**\nScore: **`{score}`**\n\n"
                                                      f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}"
                                                      f"\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
                                          colour=0xf20006)
                    embed.set_footer(text='PuffDip ©')
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                else:
                    board[user_row][user_col] = "3"
                    header = f"{random.choice(self.battleship_emoji_text['boats'])} {self.battleship_emoji_text['one']} {self.battleship_emoji_text['two']} {self.battleship_emoji_text['three']} {self.battleship_emoji_text['four']} {self.battleship_emoji_text['five']} "
                    row_1 = str(" ".join(board[0])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_2 = str(" ".join(board[1])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_3 = str(" ".join(board[2])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_4 = str(" ".join(board[3])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    row_5 = str(" ".join(board[4])).replace('O', self.battleship_emoji_text['ocean']).replace('1', self.battleship_emoji_text['x']).replace('2', self.battleship_emoji_text['fire']).replace('3', self.battleship_emoji_text['bomb'])
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description=f"**`MISS`**\nScore: **`{score}`**\n\n"
                                                      f"{header}\n{self.battleship_emoji_text['one']} {row_1}\n{self.battleship_emoji_text['two']} {row_2}\n{self.battleship_emoji_text['three']} {row_3}\n{self.battleship_emoji_text['four']} {row_4}\n{self.battleship_emoji_text['five']} {row_5}"
                                                      f"\nGameHash:\n**{gamehash_1}\n{gamehash_2}**\nIf you are stuck\nuse **`{self.config['prefix']}help battleship`**",
                                          colour=0xf20006)
                    embed.set_footer(text='PuffDip ©')
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                    board[user_row][user_col] = "1"
                    board_db_insert = str(board).replace("'", "<A>").replace(",", "<C>")  # make seperater for db, A for ' C for ,
                    self.database.cur.execute(f"UPDATE botzilla.battleship SET board = '{board_db_insert}' where ID = {id} and gamehash = '{gamehash}';")
                    self.database.conn.commit()
                    self.database.cur.execute("ROLLBACK;")

        # If anything goes wrong, Raise exeption
        except Exception as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='Something went wrong, please notify me with **`{}report <How the error came up>`**\nError:\n**``{} : {}``**'.format(self.config['prefix'], type(e).__name__, e),
                                  colour=0xf20006)
            embed.set_footer(text='PuffDip ©')
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


def setup(bot):
    m = Games(bot)
    bot.add_cog(m)
