from app.utils.gappshelper import GappsHelper
import time
from datetime import datetime, date, timedelta
from config import get_env


class Actions:
	def __init__(self, slackhelper, user_info=None):
		self.gappshelper = GappsHelper()
		self.sheet = self.gappshelper.open_sheet()
		self.user_info = user_info
		self.slackhelper = slackhelper

	def help(self):
		text_detail = (
			'Available commands:\\n'
			'	`/bootcamp_python register`\\n'
			'	`/bootcamp_python unregister`\\n'
			'	`/bootcamp_python subject day[xx]`\\n'
			'	`/bootcamp_python correction day[xx]`\\n'
			'	`/bootcamp_python correct`\\n'
			'	`/bootcamp_python students`\\n'
			'	`/bootcamp_python info`\\n'
			'	`/bootcamp_python help`\\n'
		)
		return text_detail

	def register(self):
		text_detail = "register"
		return text_detail

	def unregister(self):
		text_detail = "unregister"
		return text_detail

	def subject(self, *args):
		text_detail = "subject"
		return text_detail

	def notify_channel(self):
		text_detail = '*Task #TEST for cmaxime:*'
		self.slackhelper.post_message_to_channel(text_detail)