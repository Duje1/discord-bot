from discord import Client
import os

TOKEN = os.getenv('TEST_BOT_TOKEN')
USERNAME = "<Your Name Here>" # <<<< Change This!!

CHANNEL1_ID = 762378622622236682

class CustomClient(Client):
	async def on_ready(self):
		print(f'{self.user.name} now connected.')
		channel = self.get_channel(CHANNEL1_ID)
		await channel.send(f"Hello everyone. {USERNAME} has given me life!")

client = CustomClient()
client.run(TOKEN)
