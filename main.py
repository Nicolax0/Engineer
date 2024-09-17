import discord
import os


TOKEN = os.getenv("DISCORD_KEY")

# Create a subclass of Client to encapsulate bot behavior
class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}')

    async def on_message(self, message):
        # Avoid responding to the bot's own messages
        if message.author == self.user:
            return

        if message.content.lower() == 'ping':
            await message.channel.send('pong!')

# Create an instance of MyClient
client = MyClient(intents=discord.Intents.default())

# Run the bot with the token
client.run(TOKEN)