from traceback import format_exc
from contextlib import suppress
import shlex

from discord.errors import NotFound

from permissions import check_roles, check_scope
from commands.general import DeleteMsg, ChooseOption, Poll, ShowHelp, ShowUsage
from parser import CommandParsingError, CommandHelpError, CommandParser

COMMANDS = [
	DeleteMsg,
	ChooseOption,
	Poll,
	ShowHelp,
	ShowUsage,
]

COMMAND_PREFIX = "/"

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



