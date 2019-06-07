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

def setup(bot):
    bot.add_cog(General(bot))
