from random import choice
from argparse import Action
import re
import os

import yaml

from command import Command
from server import ROLES, CHANNELS, CATEGORIES, NUMBERS_EMOJI
from discord import Embed, Colour
from parser import CommandParsingError

def max20(val):
	num = int(val)
	if 0 < num <= 20:
		return num
	raise ValueError("Bad Range")

# required_length from Stack Overflow
# https://stackoverflow.com/questions/4194948/python-argparse-is-there-a-way-to-specify-a-range-in-nargs/
# courtesy of unutbu
# unutbu profile https://stackoverflow.com/users/190597/unutbu
def required_length(nmin, nmax):
	class RequiredLength(Action):
		def __call__(self, parser, args, values, option_string=None):
			if not nmin <= len(values) <= nmax:
				msg='argument "{f}" requires between {nmin} and {nmax} arguments'.format(
					f=self.dest, nmin=nmin, nmax=nmax)
				#raise argparse.ArgumentTypeError(msg)
				raise CommandParsingError(msg)
			setattr(args, self.dest, values)
	return RequiredLength

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
	multiline = True
	delete_msg = True

	@classmethod
	def register_parameters(cls, prefix, subparsers):
		parser = cls.create_parser(prefix, subparsers)
		parser.add_argument('question', type=str, help="Question inside quotation marks")
		parser.add_argument('options', nargs='*', type=str, help="Space-separated options", action=required_length(0,10), default=None)

	async def show_yes_no(self, question):
		bot_message = await self.msg.channel.send(f'**{question}**')
		await bot_message.add_reaction("\U0001F44D")
		await bot_message.add_reaction("\U0001F44E")

	async def show_options(self, question, options):
		embed = Embed(title=question, colour=Colour.from_rgb(59,136,195))	

		for index, option in enumerate(options):
			embed.add_field(name=NUMBERS_EMOJI[index], value=option, inline=False)

		embed_message = await self.msg.channel.send('\n', embed=embed)

		for index in range(len(options)):
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

class SendWelcomeMsg(Command):
	name = "start"
	delete_msg = True
	roles = [ROLES.get("ADMIN")]
	# channels = [CHANNELS.get("WLCM")]

	@classmethod
	def register_parameters(cls,prefix,subparsers):
		parser = cls.create_parser(prefix, subparsers)
	
	async def execute(self, args):
		guild_name = self.msg.guild.name
		invite_link = "https://discord.gg/NhhXgtM"
		
		with open("welcome.yaml", 'r') as f:
			welcome_info = yaml.load(f, Loader=yaml.FullLoader)

		output = []
		for topic, body in welcome_info.items():
			text = str(body)
			text = re.sub(r"\$SERVER_NAME(?!\w)", guild_name, text)
			text = re.sub(r"\$INVITE_LINK(?!\w)", invite_link, text)
			output.append(text)

		await self.msg.channel.send("\n".join(output))

   
