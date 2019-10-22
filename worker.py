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
   slackhelper = SlackHelper()
   actions = Actions(slackhelper, user_info=user_info)
   print(actions.register())
   print(actions.unregister())
   print(actions.unregister())
   # actions.notify_channel()

if __name__ == '__main__':
   main()