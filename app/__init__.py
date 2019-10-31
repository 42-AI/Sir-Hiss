from flask_api import FlaskAPI
from config.env import app_env
from app.utils.slackhelper import SlackHelper
from flask import request, jsonify
from app.actions import Actions
from re import match

import sys
import logging


'''
/bootcamp_python register
/bootcamp_python unregister
/bootcamp_python subject day[xx]
/bootcamp_python correction day[xx]
/bootcamp_python correct
/bootcamp_python students
/bootcamp_python info
/bootcamp_python help
'''
# client secret file


allowed_commands = [
		'register',
		'unregister',
		'subject',
		'correction',
		'correct',
		'info',
		'help',
	]

HELPER = 'Invalid Command Sent - `/sir help` for available commands'

def create_app(config_name):

	app = FlaskAPI(__name__, instance_relative_config=False)
	app.config.from_object(app_env[config_name])
	app.config.from_pyfile('../config/env.py')

	app.logger.addHandler(logging.StreamHandler(sys.stdout))
	app.logger.setLevel(logging.ERROR)

	@app.route('/bootcamp_python', methods=['POST'])
	def sirhiss():
		command_text = request.data.get('text')
		if command_text is not None:
			
			command_text = command_text.split(' ')

			slack_uid = request.data.get('user_id')
			slackhelper = SlackHelper()
			slack_user_info = slackhelper.user_info(slack_uid)
			actions = Actions(slackhelper, slack_user_info)
			
			if command_text[0] not in allowed_commands:
				response_body = {'text': HELPER}

			if command_text[0] == 'register':
				response_body = {'text': actions.register()}

			if command_text[0] == 'unregister':
				response_body = {'text': actions.unregister()}

			if command_text[0] == 'subject':
				response_body = {'text': actions.subject(command_text)}
			
			if command_text[0] == 'correction':
				response_body = {'text': actions.correction(command_text)}
			
			if command_text[0] == 'info':
				response_body = {'text': actions.info()}

			if command_text[0] == 'help':
				response_body = {'text': actions.help()}
		else:
			response_body = {'text': HELPER}
		response = jsonify(response_body)
		response.status_code = 200
		return response

	return app