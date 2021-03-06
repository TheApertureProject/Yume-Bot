#  Copyright (c) 2019.
#  MIT License
#
#  Copyright (c) 2019 YumeNetwork
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.


import asyncio
import json
import random

import discord
from discord.ext import commands

from modules.utils import lists
from modules.utils.format import Embeds

with open('./config/config.json', 'r') as cjson:
    config = json.load(cjson)

SUGGESTION = config['suggestion']
FEEDBACK = config["feedback"]
GUILD = config['support']


class Gestion(commands.Cog):
    conf = {}

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config

    @commands.command()
    async def suggestion(self, ctx, *, content: str):

        guild = self.bot.get_guild(int(GUILD))
        for chan in guild.channels:
            if chan.id == int(SUGGESTION):
                channel = chan
        tip = random.choice(lists.tip)

        em = discord.Embed(timestamp=ctx.message.created_at)
        em.set_author(
            name=f"Suggestion from {ctx.message.author.name}", icon_url=ctx.message.author.avatar_url)
        em.set_footer(text=f'Tip: {tip}')
        em.description = f'{content}'

        reactions = ['✅', '❌', '➖']

        msg = await channel.send(embed=em)

        for reaction in reactions:
            await msg.add_reaction(reaction)

    @suggestion.error
    async def suggestion_error(self, ctx, error):
        if isinstance(error, commands.UserInputError):
            help = self.bot.get_cog('Help')
            await ctx.invoke(help.suggestion)

    @commands.command()
    async def feedback(self, ctx):

        auth = ctx.message.author
        guild = ctx.message.guild

        # owner = await self.bot.get_user_info(OWNER)
        server = self.bot.get_guild(int(GUILD))
        for chan in server.channels:
            if chan.id == int(FEEDBACK):
                channel = chan

        await ctx.send("{}, Tell me your feedback".format(ctx.message.author.mention), delete_after=70)

        def check(m):
            if m.author == ctx.message.author:
                return True
            else:
                return False

        try:
            msg = await self.bot.wait_for('message', timeout=60.0, check=check)

        except asyncio.TimeoutError:
            await ctx.send('👎')
            return

        else:
            success = True
            await ctx.send('👍')

        await msg.delete()
        em = await Embeds().format_feedback_embed(ctx, auth, guild, success, msg)
        await channel.send(embed=em)


def setup(bot):
    bot.add_cog(Gestion(bot))
