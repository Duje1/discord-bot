from argparse import ArgumentParser

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