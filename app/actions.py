from app.utils.gappshelper import GappsHelper
import time
from datetime import datetime, date, timedelta
from config import get_env

HELPER_MSG = """Available commands:
-> `/bootcamp_python register`
-> `/bootcamp_python unregister`
-> `/bootcamp_python subject day[xx]`
-> `/bootcamp_python correction day[xx]`
-> `/bootcamp_python students`
-> `/bootcamp_python info`
-> `/bootcamp_python help`
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

	def help(self):
		text_detail = HELPER_MSG
		return text_detail

	def register(self):
		text_detail = "register"
		return text_detail

	def unregister(self):
		text_detail = "unregister"
		return text_detail

	def subject(self, *args):
		text_detail = "subject" #+ str(self.sheet.get_all_records())
		return text_detail

	def info(self):
		text_detail = "info about : {} with id:[{}]".format(
				self.user_name,
				self.user_id,
			)
		return text_detail

	def notify_channel(self):
		text_detail = '*Task #TEST for cmaxime:*'
		self.slackhelper.post_message_to_channel(text_detail)