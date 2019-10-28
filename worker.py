from app.actions import Actions
from app.utils.slackhelper import SlackHelper


# Main function
def main():
   user_info = {
      'user': {
         'name': 'atrudel', 
         'id': 'U4E9E7PU6',
         },
      }
   # user_info = None
   slackhelper = SlackHelper()
   actions = Actions(slackhelper, user_info=user_info)
   # print(actions.register())
   # print(actions.subject(["", "day01"]))
   # print(actions.unregister())
   # # actions.notify_channel()
   # print(actions.mess_with_spreadsheet())
   # print(actions.correction(["", "day04"]))
   print(actions.info())
   print(actions.help())

if __name__ == '__main__':
   main()