import time
import random
from datetime import datetime
from datetime import date
from datetime import timedelta

from config import get_env
from app.utils.gappshelper import GappsHelper
from app.utils.schedulehelper import ScheduleHelper

"""Actions class Explainations

This module list all the actions the Slack Bot can do related to the 
/bootcamp_python slash command, is can be tested using the worker.py, 
but the main purpose of the class Actions is to interact with a flask api 
described in __init__.py.

Actions functions:
    help() : return a helper with a list of all available commands 
    and a short description for each command.
        * @return (str)

    register() : register the user to the bootcamp python if it
    is not yet registered, and if authorized by the schedule.
    Check if the command has beed triggered by slack.
        * @gsheet (insert user row on top)
        * @return (str)

    unregister() : unregister the user to the bootcamp python if it
    is already registered, and if authorized by the schedule.
    Check if the command has beed triggered by slack.
        * @gsheet (remove user row)
        * @return (str)

    subject(args) : register a user to a day, if he is already
    registed to the bootcamp, and not yet registered to the day,
    and if authorized by the schedule.
    Send aso the PDF of the day to the user via a private message.
    Check if the command has beed triggered by slack.
        * @gsheet (put PDF in user row at the day column)
        * @return (str)
    
    correction(args) : register a user to a correction for a specific 
    day, if he is already registed to the bootcamp, and also registered
    to the day, but not yet registered for a correction on this day,
    and also not yet attributed for a correction on this day.
    Send aso the PDF of the day to the user via a private message.
    Check if the command has beed triggered by slack.
    It's also checkout if someone is also looking for a correction for the
    same day, if yes, then connect the 2 users to schedule a correction and
    add the user_login of each other to their day cell.
    Send a private message to the 2 users if a match occured.
        * @gsheet (put WAITING/user_login in user row at the day column)
        * @return (str)

    info() : return info about the current user related to the bootcamp_python
    Check if the command has beed triggered by slack.
        * @return (str)

Available utils wrappers:


Todo:
    * [ ]: help
    * [x]: register
    * [x]: unregister
    * [ ]: subject
    * [ ]: correction
    * [ ]: info

"""

HELPER_MSG = """Available commands:
> `/bootcamp_python register`
> `/bootcamp_python unregister`
> `/bootcamp_python subject day[xx]`
> `/bootcamp_python correction day[xx]`
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

    def mandatoryUserInfo(f):
        def wrapper(self, *args, **kwargs):
            if self.user_info is None:
                return "Error, no user logged"
            return f(self, *args, **kwargs)

        return wrapper

    def mandatoryRegistered(f):
        def wrapper(self, *args, **kwargs):
            for index, row in enumerate(self.sheet.get_all_records()):
                if row["user_id"] == self.user_id:
                    break
            else:
                return "Error, user not registered at the bootcamp python"
            return f(self, *args, **kwargs)

        return wrapper

    def correctDayArgument(f):
        def wrapper(self, *args, **kwargs):
            days = [
                'day00',
                'day01',
                'day02',
                'day03',
                'day04'
            ]
            command = args[0]
            if len(command) != 2:
                return "Incorrect number of arguments. Use one argument to indicate the day. E.g. day00"
            if command[1] not in days:
                return "Incorrect argument formatting. Here are the accepted day arguments: {}".format(days)
            return f(self, *args, **kwargs)
        
        return wrapper

    def help(self):
        text_detail = HELPER_MSG
        return text_detail

    @mandatoryUserInfo
    def register(self):
        # Check if the user is already registered
        for row in self.sheet.get_all_records():
            if row["user_id"] == self.user_id:
                return "Already registered"
        # Update with user info
        self.sheet.insert_row([self.user_name, self.user_id], 2)
        return "You are now registered to the bootcamp python"

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

    @mandatoryUserInfo
    @mandatoryRegistered
    def subject(self, args):
        if len(args) != 2:
            return "Error, bad args number"
        # if not self.schedule.can_fetchday(args[1]):
        # return "Not available now."
        self.slackhelper.send_pdf(
            'app/assets/AI42_RL_project.pdf',
            'AI42_RL_project.pdf',
            channel=self.user_id,
            title="RL Project",
        )
        return "There it is."

    @mandatoryUserInfo
    @mandatoryRegistered
    @correctDayArgument
    def correction(self, args):
        # see what is written in the day00 cell after pdf has been downloaded
        day = args[1]
        column = self.sheet.find(day).col
        row = self.sheet.find(self.user_id).row
        requester_cell = self.sheet.cell(row, column)

        def find_partner(column):
            waiting_cells = self.sheet.findall("WAITING")
            random.shuffle(waiting_cells)
            for cell in waiting_cells:
                if cell.col == column:
                    return cell
            return None

        if requester_cell.value == '':
            partner_cell = find_partner(column)
            if partner_cell is None:
                requester_cell.value = 'WAITING'
                self.sheet.update_cells([requester_cell])
                return "You are on the waitlist.\nYou will be matched with the next bootcamper who requests a correction."
            else:
                partner_user_name = self.sheet.cell(partner_cell.row, 1).value
                partner_cell.value = self.user_name
                requester_cell.value = partner_user_name
                self.sheet.update_cells([requester_cell, partner_cell])
                # Start conversation with both users ###########################################################

                return "You have been matched with {}. You can message each other to arrange a meeting and review each other's code!".format(partner_user_name)
        elif requester_cell.value == 'WAITING':
            return "You are already on the waiting list for corrections.\nYou will be matched with the next available corrector."
        else:
            return "You have already been matched with {} for your correction of {}".format(requester_cell.value, day)
        
       
#===================================================

    # @mandatoryRegistered
    # @mandatoryUserInfo
    # def mess_with_spreadsheet(self):
    #     day = 'day01'
    #     self.sheet.
    #     return "Cell ({},{}) contains {}.".format(row, column, requester_cell.value)


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


        