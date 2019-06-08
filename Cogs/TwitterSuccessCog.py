import discord
from discord.ext import commands
import datetime
import tweepy
import random

class General(commands.Cog, name = "Twitter Success Cog"):
    def __init__(self, bot):
        self.bot = bot
        print("Loaded Twitter Success Cog.")
        auth = tweepy.OAuthHandler(self.bot.twitter_api_key, self.bot.twitter_api_secret)
        auth.set_access_token(self.bot.twitter_access_token, self.bot.twitter_access_secret)
        self.bot.api = tweepy.API(auth)
        print(self.bot.api.me().screen_name)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in self.bot.success_channels:
            try:
                tweettext = self.bot.twitter_post_message.format(user = message.author.name)
            except:
                tweettext = self.bot.twitter_post_message
            images = message.attachments
            if len(images) > 0:
                for i in range(0,len(images)):
                    media_ids = []
                    if images[i].url.split(".")[-1].lower() in ['jpg', 'png']:
                        with open("./TempFiles/temp.png", 'wb') as file:
                            await images[i].save(file)
                        res = self.bot.api.media_upload("./TempFiles/temp.png")
                        media_ids.append(res.media_id)

                status = self.bot.api.update_status(status=tweettext, media_ids=media_ids)

                if self.bot.twitter_log_all:
                    if self.bot.use_timestamp:
                        embed = discord.Embed(
                            title = "New Twitter Post",
                            description = tweettext,
                            url = status.entities['media'][0]['expanded_url'],
                            color = random.choice(self.bot.embed_colors),
                            timestamp = datetime.datetime.now(datetime.timezone.utc)
                        )
                    else:
                        embed = discord.Embed(
                            title = "New Twitter Post",
                            description = tweettext,
                            url = "https://twitter.com/" + self.bot.api.me().screen_name,
                            color = random.choice(self.bot.embed_colors)
                        )
                    embed.set_image(
                        url = message.attachments[0].url
                    )
                    embed.set_footer(
                        text = self.bot.footer_text,
                        icon_url = self.bot.footer_icon
                    )

                    for log in self.bot.logs_channels:
                        channel = self.bot.get_channel(log)
                        await channel.send(content = None, embed = embed)

    @commands.command(name = 'twitter', help = "Shows info on a Twitter account based on either a mention of a twiter handle.")
    @commands.guild_only()
    async def twitter(self, ctx, *, twitter_to_search = None):
        if twitter_to_search == None:
            if self.bot.use_timestamp:
                embed = discord.Embed(
                    title = "Invalid Command",
                    description = "You must include a Twitter handle in the command.",
                    color = random.choice(self.bot.embed_colors),
                    timestamp = datetime.datetime.now(datetime.timezone.utc)
                )
            else:
                embed = discord.Embed(
                    title = "Invalid Command",
                    description = "You must include a Twitter handle in the command.",
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
            await ctx.send(embed = embed)
        else:
            results = self.bot.api.search_users(twitter_to_search, 1, 0)
            if len(results) == 0:
                if self.bot.use_timestamp:
                    embed = discord.Embed(
                        title = "Invalid Handle",
                        description = "No results were found for this Twitter handle, please try again.",
                        color = random.choice(self.bot.embed_colors),
                        timestamp = datetime.datetime.now(datetime.timezone.utc)
                    )
                else:
                    embed = discord.Embed(
                        title = "Invalid Handle",
                        description = "No results were found for this Twitter handle, please try again.",
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
                await ctx.send(embed = embed)
            else:
                result = results[0]
                if self.bot.use_timestamp:
                    embed = discord.Embed(
                        title = result.name,
                        description = result.description,
                        url = "https://twitter.com/" + result.screen_name,
                        color = random.choice(self.bot.embed_colors),
                        timestamp = datetime.datetime.now(datetime.timezone.utc)
                    )
                else:
                    embed = discord.Embed(
                        title = result.name,
                        description = result.description,
                        url = "https://twitter.com/" + result.screen_name,
                        color = random.choice(self.bot.embed_colors)
                    )
                if self.bot.show_command_author:
                    embed.set_author(
                        name = ctx.author.name,
                        icon_url = ctx.author.avatar_url
                    )
                embed.add_field(
                    name = "Private",
                    value = str(result.protected),
                    inline = True
                )
                embed.add_field(
                    name = "Followers",
                    value = result.followers_count,
                    inline = True
                )
                embed.add_field(
                    name = "Friends",
                    value = result.friends_count,
                    inline = True
                )
                embed.add_field(
                    name = "Posts",
                    value = result.statuses_count,
                    inline = True
                )
                embed.add_field(
                    name = "Language",
                    value = result.lang,
                    inline = True
                )
                embed.add_field(
                    name = "Created",
                    value = result.created_at.strftime("%B %d, %Y, %r"),
                    inline = False
                )
                try:
                    embed.set_thumbnail(
                        url = result.profile_image_url_https
                    )
                except:
                    pass

                embed.set_footer(
                    text = self.bot.footer_text,
                    icon_url = self.bot.footer_icon
                )

                await ctx.send(embed = embed)



def setup(bot):
    bot.add_cog(General(bot))
