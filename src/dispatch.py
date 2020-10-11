from argparse import ArgumentParser
from traceback import format_exc
from contextlib import suppress
import shlex

from discord.errors import NotFound

from permissions import check_roles, check_scope
from commands.general import DeleteMsg, ChooseOption, Poll, ShowHelp, ShowUsage

COMMANDS = [
	DeleteMsg,
	ChooseOption,
	Poll,
	ShowHelp,
	ShowUsage,
]

COMMAND_PREFIX = "/"

class CommandParsingError(Exception):
	def __init__(self, message):
		self.message = message

class CommandHelpError(Exception):
	def __init__(self, message):
		self.message = message

class CommandParser(ArgumentParser):
	def error(self, message):
		raise CommandParsingError(message)

	def exit(self, status=0, message=None):
		raise CommandParsingError(message)

	def print_help(self, file=None):
		message = self.format_help()
		raise CommandHelpError(message)

	def print_usage(self, file=None):
		message = self.format_usage()
		raise CommandHelpError(message)

class Dispatcher(object):
	def __init__(self, client):
		self.client = client
		self.parser = CommandParser(prog="", allow_abbrev=False)
		subparsers = self.parser.add_subparsers()

		for command in COMMANDS:
			command.register_parameters(COMMAND_PREFIX, subparsers)

	async def dispatch(self, msg):
		first_line = msg.content.split('\n', 1)[0]
		subcommand = shlex.split(first_line)[0]
		if not subcommand.startswith(COMMAND_PREFIX):
			return
		
		text = first_line
		for command in COMMANDS:
			if COMMAND_PREFIX + command.name == subcommand:
				if command.multiline:
					text = msg.content
				break

		try:
			args = self.parser.parse_args(shlex.split(text))
			
			if not check_scope(msg, args.cls.channels, args.cls.categories):
				return

			if not check_roles(msg, args.cls.roles):
				await msg.channel.send("You do not have permission for this command")
				return

			command = args.cls(self.client, msg, self)
			await command.execute(args)
		except CommandParsingError as error:
			await msg.channel.send(error.message)
			await msg.add_reaction(u"\u274C")
			return
		except CommandHelpError as error:
			await msg.channel.send(error.message)
			await msg.add_reaction(u"\u2705")
			return
		except Exception as error:
			error_message = format_exc()
			await msg.add_reaction(u"\u274C")
			await msg.channel.send(error_message)
			raise error

		with suppress(NotFound):
			await msg.add_reaction(u"\u2705")
			if args.cls.delete_msg:
				await msg.delete(delay=3)



