from app.utils.gappshelper import GappsHelper
from app.utils.schedulehelper import ScheduleHelper
import time
from datetime import datetime, date, timedelta
from config import get_env

HELPER_MSG = """Available commands:
> `/bootcamp_python register`
> `/bootcamp_python unregister`
> `/bootcamp_python subject day[xx]`
> `/bootcamp_python correction day[xx]`
> `/bootcamp_python students`
> `/bootcamp_python info`
> `/bootcamp_python help`
"""


class Actions:
    def __init__(self, slackhelper, user_info=None):
        self.gappshelper = GappsHelper()
        self.schedule = ScheduleHelper()
        self.sheet = self.gappshelper.open_sheet()
        self.user_info = user_info
        self.slackhelper = slackhelper
        self.user_name = (
            user_info["user"]["name"]
            if user_info is not None
            and user_info.get("user") is not None
            and user_info["user"].get("name") is not None
            else None
        )
        self.user_id = (
            user_info["user"]["id"]
            if user_info is not None
            and user_info.get("user") is not None
            and user_info["user"].get("id") is not None
            else None
        )

    """ Check if action has logged user_info
	"""

    def mandatoryUserInfo(f):
        def wrapper(self, *args, **kwargs):
            if self.user_info is None:
                return "Error, no user logged"
            return f(self, *args, **kwargs)

        return wrapper

    """ Check if the user is registered at the bootcamp
	"""

    def mandatoryRegistered(f):
        def wrapper(self, *args, **kwargs):
            for index, row in enumerate(self.sheet.get_all_records()):
                if row["user_id"] == self.user_id:
                    break
            else:
                return "Error, user not registered at the bootcamp python"
            return f(self, *args, **kwargs)

        return wrapper

    def help(self):
        text_detail = HELPER_MSG
        return text_detail

    """ Register a user if he is not yet registered to the bootcamp
	"""

    @mandatoryUserInfo
    def register(self):
        # Check if the user is already registered
        for row in self.sheet.get_all_records():
            if row["user_id"] == self.user_id:
                return "Already registered"
        # Update with user info
        self.sheet.insert_row([self.user_name, self.user_id], 2)
        return "You are now registered to the bootcamp python"

    """ Unregister a user if he is registered to the bootcamp
	"""

    @mandatoryUserInfo
    @mandatoryRegistered
    def unregister(self):
        for index, row in enumerate(self.sheet.get_all_records()):
            if row["user_id"] == self.user_id:
                break
        else:
            return "You are not registered"
        index += 2
        self.sheet.delete_row(index)
        return "You have been unregistered form the bootcamp python"

    # my_file = {
    #     'file' : ('/tmp/myfile.pdf', open('/tmp/myfile.pdf', 'rb'), 'pdf')
    # }
    # payload={
    #     "filename":"myfile.pdf", 
    #     "token":token, 
    #     "channels":['#random'], 
    # }
    # r = requests.post("https://slack.com/api/files.upload", params=payload, files=my_file)

    # file_upload(self, file_content, file_name, file_type, title=None, )

    @mandatoryUserInfo
    @mandatoryRegistered
    def subject(self, args):
        if len(args) != 2:
            return "Error, bad args number"
        # if not self.schedule.can_fetchday(args[1]):
            # return "Not available now."
        # self.slackhelper.file_upload(
        #     open('app/assets/AI42_RL_project.pdf', 'rb'),
        #     'AI42_RL_project.pdf',
        #     'pdf',
        #     channel=self.user_id,
        #     title="Test Post PDF",
        # )
        return "There it is."

    @mandatoryUserInfo
    @mandatoryRegistered
    def info(self):
        text_detail = "info about : {} with id:[{}]".format(
            self.user_name, self.user_id
        )
        return text_detail

    def notify_channel(self):
        text_detail = "*Task #TEST for cmaxime:*"
        self.slackhelper.post_message_to_channel(text_detail)
