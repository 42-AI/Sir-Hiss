from app.utils.gappshelper import GappsHelper
import time
from datetime import datetime, date, timedelta
from config import get_env

HELPER_MSG = """Available commands:
	`/bootcamp_python register`
	`/bootcamp_python unregister`
	`/bootcamp_python subject day[xx]`
	`/bootcamp_python correction day[xx]`
	`/bootcamp_python students`
	`/bootcamp_python info`
	`/bootcamp_python help`
"""

class Actions:
	def __init__(self, slackhelper, user_info=None):
		self.gappshelper = GappsHelper()
		self.sheet = self.gappshelper.open_sheet()
		self.user_info = user_info
		self.slackhelper = slackhelper
		# TODO: clean this part
		self.user_name = None
		self.user_id = None
		if user_info is not None:
			tmp = self.user_info.get('user')
			if tmp is not None:
				self.user_name = tmp.get('name')
				self.user_id = tmp.get('id')
		########################

	""" Check if action has logged user_info """
	def mandatoryUserInfo(f):
		def wrapper(self, *args, **kwargs):
			if self.user_info is None:
				return "Error, no user logged"
			return f(self, *args, **kwargs)
		return wrapper

	""" Check if the user is registered at the bootcamp """
	def mandatoryRegistered(f):
		def wrapper(self, *args, **kwargs):
			for index, row in enumerate(self.sheet.get_all_records()):
				if row['user_id'] == self.user_id:
					break
			else:
				return "Error, user not registered at the bootcamp python"
			return f(self, *args, **kwargs)
		return wrapper

	def help(self):
		text_detail = HELPER_MSG
		return text_detail

	""" Register a user if he is not yet registered to the bootcamp """
	@mandatoryUserInfo
	def register(self):
		# Check if the user is already registered
		for row in self.sheet.get_all_records():
			if row['user_id'] == self.user_id:
				return "Already registered"
		# Update with user info
		self.sheet.insert_row([self.user_name, self.user_id], 2)
		return "You are now registered to the bootcamp python"

	""" Unregister a user if he is registered to the bootcamp """
	@mandatoryUserInfo
	@mandatoryRegistered
	def unregister(self):
		for index, row in enumerate(self.sheet.get_all_records()):
			if row['user_id'] == self.user_id:
				break
		else:
			return "You are not registered"
		index += 2
		self.sheet.delete_row(index)
		return "You have been unregistered form the bootcamp python"

	@mandatoryUserInfo
	@mandatoryRegistered
	def subject(self, *args):
		text_detail = "subject"
		return text_detail

	@mandatoryUserInfo
	@mandatoryRegistered
	def info(self):
		text_detail = "info about : {} with id:[{}]".format(
				self.user_name,
				self.user_id,
			)
		return text_detail

	def notify_channel(self):
		text_detail = '*Task #TEST for cmaxime:*'
		self.slackhelper.post_message_to_channel(text_detail)