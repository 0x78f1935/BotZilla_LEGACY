from discord.ext import commands
import traceback
import discord
import inspect
import textwrap
from contextlib import redirect_stdout
import io
import json

tmp_config = json.loads(str(open('./options/config.js').read()))
config = tmp_config['config']

owner_list = config['owner-id']

class REPL:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.sessions = set()
        self.tmp_config = json.loads(str(open('./options/config.js').read()))
        self.config = self.tmp_config['config']
        self.emojiUnicode = self.tmp_config['unicode']
        self.exchange = self.tmp_config['exchange']
        self.botzillaChannels = self.tmp_config['channels']
        self.owner_list = self.config['owner-id']

    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    def get_syntax_error(self, e):
        if e.text is None:
            return '```py\n{0.__class__.__name__}: {0}\n```'.format(e)
        return '```py\n{0.text}{1:>{0.offset}}\n{2}: {0}```'.format(e, '^', type(e).__name__)

    @commands.command(pass_context=True, hidden=True, name='exec')
    async def _eval(self, ctx, *, body: str = None):
        if ctx.message.author.id not in owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format('Only the owner of this bot can use this command'),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        if body is None:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format('Please, use `{}exec [python code]` to get the most out of the command'.format(
                                      config['prefix'])),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.message.channel,
            'author': ctx.message.author,
            'server': ctx.message.server,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = 'async def func():\n%s' % textwrap.indent(body, '  ')

        try:
            exec(to_compile, env)
        except SyntaxError as e:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format(self.get_syntax_error(e)),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='```py\n{}{}\n```'.format(value, traceback.format_exc()),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])


        else:
            value = stdout.getvalue()


            if ret is None:
                if value:
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='```py\n{}\n```'.format(value),
                                          colour=0xf20006)
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['succes'])
            else:
                self._last_result = ret
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='```py\n{}{}\n```'.format(value, ret),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['succes'])


    @commands.command(pass_context=True, hidden=True)
    async def repl(self, ctx):
        if ctx.message.author.id not in owner_list:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format('Only the owner of this bot can use this command'),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['error'])
            return

        msg = ctx.message

        variables = {
            'ctx': ctx,
            'bot': self.bot,
            'message': msg,
            'server': msg.server,
            'channel': msg.channel,
            'author': msg.author,
            '_': None,
        }

        if msg.channel.id in self.sessions:
            embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                  description='{}'.format('Already running a REPL session in this channel. Exit it with `quit`.'),
                                  colour=0xf20006)
            a = await self.bot.say(embed=embed)
            await self.bot.add_reaction(a, self.emojiUnicode['warning'])
            return

        self.sessions.add(msg.channel.id)
        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                              description='{}'.format('Enter code to execute or evaluate. `exit()` or `quit` to exit.'),
                              colour=0xf20006)
        a = await self.bot.say(embed=embed)
        await self.bot.add_reaction(a, self.emojiUnicode['warning'])
        while True:
            response = await self.bot.wait_for_message(author=msg.author, channel=msg.channel,
                                                       check=lambda m: m.content.startswith('`'))

            cleaned = self.cleanup_code(response.content)

            if cleaned in ('quit', 'exit', 'exit()'):
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='{}'.format('Exiting.'),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['warning'])
                self.sessions.remove(msg.channel.id)
                return

            executor = exec
            if cleaned.count('\n') == 0:
                # single statement, potentially 'eval'
                try:
                    code = compile(cleaned, '<repl session>', 'eval')
                except SyntaxError:
                    pass
                else:
                    executor = eval

            if executor is exec:
                try:
                    code = compile(cleaned, '<repl session>', 'exec')
                except SyntaxError as e:
                    embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                          description='{}'.format(self.get_syntax_error(e)),
                                          colour=0xf20006)
                    a = await self.bot.say(embed=embed)
                    await self.bot.add_reaction(a, self.emojiUnicode['error'])
                    continue

            variables['message'] = response

            fmt = None
            stdout = io.StringIO()

            try:
                with redirect_stdout(stdout):
                    result = executor(code, variables)
                    if inspect.isawaitable(result):
                        result = await result
            except Exception as e:
                value = stdout.getvalue()
                fmt = '```py\n{}{}\n```'.format(value, traceback.format_exc())
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='```py\n{}{}\n```'.format(value, traceback.format_exc()),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])
                continue
            else:
                value = stdout.getvalue()
                if result is not None:
                    fmt = '```py\n{}{}\n```'.format(value, result)
                    variables['_'] = result
                elif value:
                    fmt = '```py\n{}\n```'.format(value)

            try:
                if fmt is not None:
                    if len(fmt) > 2000:
                        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                              description='{}'.format('Content too big to be printed.'),
                                              colour=0xf20006)
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, self.emojiUnicode['error'])
                    else:
                        embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                              description='{}'.format(fmt),
                                              colour=0xf20006)
                        a = await self.bot.say(embed=embed)
                        await self.bot.add_reaction(a, self.emojiUnicode['succes'])

            except discord.Forbidden:
                pass
            except discord.HTTPException as e:
                embed = discord.Embed(title='{}:'.format(ctx.message.author.name),
                                      description='{}'.format('Unexpected error: `{}`'.format(e)),
                                      colour=0xf20006)
                a = await self.bot.say(embed=embed)
                await self.bot.add_reaction(a, self.emojiUnicode['error'])

def setup(bot):
    bot.add_cog(REPL(bot))