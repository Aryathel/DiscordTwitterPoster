import discord
from discord.ext import commands
import datetime
import yaml
import os
import sys
import random
import tweepy

with open("./Config.yml", 'r') as file:
    config = yaml.load(file, Loader = yaml.Loader)

bot = commands.AutoShardedBot(command_prefix=config['Prefix'], description="Heroicos_HM's Twitter Success Poster", case_insensitive = True)
bot.remove_command('help')

#Main Config
bot.TOKEN = config['TOKEN']
bot.prefix = config['Prefix']
bot.logs_channels = config['Log Channels']
bot.embed_colors = config['Embed Colors']
bot.footer_icon = config['Footer Icon URL']
bot.footer_text = config['Footer Text']

#Options
bot.use_timestamp = config['Options']['Embed Timestamp']
bot.delete_commands = config['Options']['Delete Commands']
bot.show_command_author = config['Options']['Show Author']
bot.show_game_status = config['Options']['Game Status']['Active']
bot.game_to_show = config['Options']['Game Status']['Game']

#Twitter Login
bot.twitter_api_key = config['Twitter Info']['API Key']
bot.twitter_api_secret = config['Twitter Info']['API Secret']
bot.twitter_access_token = config['Twitter Info']['Access Token']
bot.twitter_access_secret = config['Twitter Info']['Access Secret']

#Twitter Data
bot.success_channels = config['Twitter Info']['Success Channel IDs']
bot.twitter_post_message = config['Twitter Info']['Twitter Post Message']
bot.twitter_log_all = config['Twitter Info']['Log All Posts']

extensions = [
    'Cogs.General',
    'Cogs.TwitterSuccessCog'
]

for extension in extensions:
    bot.load_extension(extension)

@bot.event
async def on_ready():
    print('Logged in as {0} and connected to Discord! (ID: {0.id})\nConnected to Twitter with user {1}!'.format(bot.user, bot.api.me().name))
    if bot.show_game_status:
        game = discord.Game(name = bot.game_to_show)
        await bot.change_presence(activity = game)
    if bot.use_timestamp:
        embed = discord.Embed(
            title = "Online!".format(bot.user.name),
            color = random.choice(bot.embed_colors),
            timestamp = datetime.datetime.now(datetime.timezone.utc)
        )
    else:
        embed = discord.Embed(
            title = "Online!".format(bot.user.name),
            color = random.choice(bot.embed_colors)
        )
    embed.set_footer(
        text = bot.footer_text,
        icon_url = bot.footer_icon
    )
    for log in bot.logs_channels:
        channel = bot.get_channel(log)
        await channel.send(content = None, embed = embed)

    bot.start_time = datetime.datetime.now(datetime.timezone.utc)

@bot.command(name='help')
@commands.guild_only()
async def dfs_help(ctx):
    if bot.delete_commands:
        await ctx.message.delete()
    if bot.use_timestamp:
        embed = discord.Embed(
            title = ":newspaper: Help",
            color = random.choice(bot.embed_colors),
            timestamp = datetime.datetime.now(datetime.timezone.utc)
        )
    else:
        embed = discord.Embed(
            title = ":newspaper: Help",
            color = random.choice(bot.embed_colors)
        )
    if bot.show_command_author:
        embed.set_author(
            name = ctx.author.name,
            icon_url = ctx.author.avatar_url
        )
    embed.add_field(
        name = bot.prefix + "uptime",
        value = "Returns the amount of time that the bot has been online.",
        inline = False
    )
    embed.add_field(
        name = bot.prefix + "ping",
        value = "Gets the ping times from the bot to the discord servers and back.",
        inline = False
    )
    embed.set_footer(
        text = bot.footer_text,
        icon_url = bot.footer_icon
    )

    await ctx.send(embed = embed)

bot.run(bot.TOKEN, bot = True, reconnect = True)
