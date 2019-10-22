from flask_api import FlaskAPI
from config.env import app_env
from app.utils.slackhelper import SlackHelper
from flask import request, jsonify
from app.actions import Actions
from re import match

'''
/sir help
'''
# client secret file


allowed_commands = [
		'help'
	]


def create_app(config_name):

	app = FlaskAPI(__name__, instance_relative_config=False)
	app.config.from_object(app_env[config_name])
	app.config.from_pyfile('../config/env.py')

	@app.route('/sir', methods=['POST'])
	def ranti_bot():
		command_text = request.data.get('text')
		if command_text != None:
			command_text = command_text.split(' ')
			slack_uid = request.data.get('user_id')
			slackhelper = SlackHelper()
			slack_user_info = slackhelper.user_info(slack_uid)
			actions = Actions(slackhelper, slack_user_info)

			if command_text[0] not in allowed_commands:
				response_body = {'text': 'Invalid Command Sent - `/sir help` for available commands'}

			if command_text[0] == 'help':
				response_body = actions.help()
		else:
			response_body = {'text': 'Invalid Command Sent - `/sir help` for available commands'}

		response = jsonify(response_body)
		response.status_code = 200
		return response

	return app