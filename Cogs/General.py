import discord
from discord.ext import commands
import datetime
from math import trunc
import random

class General(commands.Cog, name = "General"):
    def __init__(self, bot):
        self.bot = bot
        print("Loaded General Cog.")

    @commands.command(name='uptime', help = 'Returns the amount of time the bot has been online.')
    async def uptime(self, ctx):
        if self.bot.delete_commands:
            await ctx.message.delete()

        seconds = trunc((datetime.datetime.now(datetime.timezone.utc) - self.bot.start_time).total_seconds())
        hours = trunc(seconds / 3600)
        seconds = trunc(seconds - (hours * 3600))
        minutes = trunc(seconds / 60)
        seconds = trunc(seconds - (minutes * 60))

        if self.bot.use_timestamp:
            embed = discord.Embed(
                title = ":alarm_clock: {} Uptime".format(self.bot.user.name),
                description = "{} Hours\n{} Minutes\n{} Seconds".format(hours, minutes, seconds),
                color = random.choice(self.bot.embed_colors),
                timestamp = datetime.datetime.now(datetime.timezone.utc)
            )
        else:
            embed = discord.Embed(
                title = ":alarm_clock: {} Uptime".format(self.bot.user.name),
                description = "{} Hours\n{} Minutes\n{} Seconds".format(hours, minutes, seconds),
                color = self.bot.embed_color
            )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer_text,
            icon_url = self.bot.footer_icon
        )
        await ctx.send(embed = embed)

    @commands.command(name='ping', aliases=['pong'], help = 'Gets the current latency of the bot.')
    async def ping(self, ctx):
        if self.bot.delete_commands:
            await ctx.message.delete()

        if self.bot.use_timestamp:
            embed = discord.Embed(
                title = ":ping_pong: Pong!",
                description = "Calculating ping time...",
                color = random.choice(self.bot.embed_colors),
                timestamp = datetime.datetime.now(datetime.timezone.utc)
            )
        else:
            embed = discord.Embed(
                title = ":ping_pong: Pong!",
                description = "Calculating ping time...",
                color = random.choice(self.bot.embed_colors)
            )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer_text,
            icon_url = self.bot.footer_icon
        )

        m = await ctx.send(embed = embed)
        if self.bot.use_timestamp:
            embed = discord.Embed(
                title = ":ping_pong: Pong!",
                description = "Message latency is {} ms\nDiscord API Latency is {} ms".format(trunc((m.created_at - ctx.message.created_at).total_seconds() * 1000), trunc(self.bot.latency * 1000)),
                color = random.choice(self.bot.embed_colors),
                timestamp = datetime.datetime.now(datetime.timezone.utc)
            )
        else:
            embed = discord.Embed(
                title = ":ping_pong: Pong!",
                description = "Message latency is {} ms\nDiscord API Latency is {} ms".format(trunc((m.created_at - ctx.message.created_at).total_seconds() * 1000), trunc(self.bot.latency * 1000)),
                color = random.choice(self.bot.embed_colors)
            )
        if self.bot.show_command_author:
            embed.set_author(
                name = ctx.author.name,
                icon_url = ctx.author.avatar_url
            )
        embed.set_footer(
            text = self.bot.footer_text,
            icon_url = self.bot.footer_icon
        )
        await m.edit(embed = embed)

def setup(bot):
    bot.add_cog(General(bot))
