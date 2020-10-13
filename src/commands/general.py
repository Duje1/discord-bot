from random import choice

from command import Command
from server import ROLE_TESTROLE, CHANNEL_1, CATEGORY_TEST
from discord import Embed, Colour

NUMBERS_EMOJI = ['0\u20E3', '1\u20E3', '2️\u20E3', '3️\u20E3', '4️\u20E3', '5️\u20E3', '6️\u20E3', '7️\u20E3', '8️\u20E3', '9️\u20E3']

def max20(val):
	num = int(val)
	if 0 < num <= 20:
		return num
	raise ValueError("Bad Range")

class DeleteMsg(Command):
	name = "deletemsg"

	@classmethod
	def register_parameters(cls, prefix, subparsers):
		parser = cls.create_parser(prefix, subparsers)
		parser.add_argument('count', type=max20, help="Number of messages to delete")

	async def execute(self, args):
		async for message in self.msg.channel.history(limit=args.count+1):
			await message.delete()
		

class ChooseOption(Command):
	name = "choose"

	@classmethod
	def register_parameters(cls, prefix, subparsers):
		parser = cls.create_parser(prefix, subparsers)
		parser.add_argument('options', nargs='+', type=str, help="Space-separated options to randomly choose from")

	async def execute(self, args):
		option = choice(args.options)
		await self.msg.channel.send(f"Randomly selected: {option}")

class Poll(Command):
	name = "poll"

	@classmethod
	def register_parameters(cls, prefix, subparsers):
		parser = cls.create_parser(prefix, subparsers)
		parser.add_argument('question', type=str, help="Question inside quotation marks")
		parser.add_argument('options', nargs='*', type=str, help="Space-separated options", action="extend", default=None)

	async def show_yes_no(self, question):
		bot_message = await self.msg.channel.send(f'**{question}**')
		await bot_message.add_reaction(u"👍")
		await bot_message.add_reaction(u"👎")

	async def show_options(self, question, options):
		embed = Embed(title=question, colour=Colour.from_rgb(59,136,195))	

		for index, option in enumerate(options):
			embed.add_field(name=NUMBERS_EMOJI[index], value=option, inline=False)

		embed_message = await self.msg.channel.send('\n', embed=embed)

		for index, option in enumerate(options):
			await embed_message.add_reaction(NUMBERS_EMOJI[index])

	async def execute(self, args):
		options = args.options
		question = args.question

		if len(options) == 0:
			await self.show_yes_no(question)
		else:
			await self.show_options(question, options)

class ShowHelp(Command):
	name = "help"

	@classmethod
	def register_parameters(cls, prefix, subparsers):
		parser = cls.create_parser(prefix, subparsers)

	async def execute(self, args):
		text = self.dispatcher.parser.format_help()
		await self.msg.channel.send(text)

class ShowUsage(Command):
	name = "usage"

	@classmethod
	def register_parameters(cls, prefix, subparsers):
		parser = cls.create_parser(prefix, subparsers)

	async def execute(self, args):
		text = self.dispatcher.parser.format_usage()
		await self.msg.channel.send(text)
