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
		print('Helper called')
		text_detail = (
			'*Task #TEST for cmaxime:* \n\n'
			'Helper should print on /sir help'
		)
		return text_detail

	def notify_channel(self):
		print('Worker is running...')
		while True:
			text_detail = '*Task #TEST for cmaxime:* \n\n'

			self.slackhelper.post_message_to_channel(text_detail)
			time.sleep(200)