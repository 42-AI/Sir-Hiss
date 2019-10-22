from app.actions import Actions
from app.utils.slackhelper import SlackHelper


# Main function
def main():
   user_info = {
      'user': {
         'name': 'maxime', 
         'id': 'a0123456789',
         },
      }
   # user_info = None
   slackhelper = SlackHelper()
   actions = Actions(slackhelper, user_info=user_info)
   print(actions.register())
   print(actions.subject(["", "day00"]))
   print(actions.unregister())
   # actions.notify_channel()

if __name__ == '__main__':
   main()