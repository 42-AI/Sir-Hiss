import json
import gspread
from os import path
from config import get_env
from oauth2client import crypt, GOOGLE_TOKEN_URI, GOOGLE_REVOKE_URI
from oauth2client.service_account import ServiceAccountCredentials


class GappsHelper:

	def __init__(self, bootcamp):
		# setup for google sheet - Google Drive API Instance
		self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		self.credentials = self.credentials_from_env(self.scope)
		self.client = gspread.authorize(self.credentials)
		self.bootcamp = bootcamp

	def credentials_from_env(self, scopes):
		keyfile_dict = {}
		keyfile_dict["token_uri"] = get_env('SC_TOKEN_URI')
		keyfile_dict["auth_uri"] = get_env('SC_AUTH_URI')
		# TODO: clean this part
		tmp = get_env('SC_PRIVATE_KEY').replace("\n", "\\n")
		buff = '{"a": "' + tmp + '"}'
		buff = json.loads(buff)
		keyfile_dict["private_key"] = buff['a']
		#######################
		signer = crypt.Signer.from_string(keyfile_dict["private_key"])
		credential = ServiceAccountCredentials(
			get_env('SC_CLIENT_EMAIL'),
			signer,
			scopes=scopes,
			private_key_id=get_env('SC_PRIVATE_KEY_ID'),
			client_id=get_env('SC_CLIENT_ID'),
			token_uri=keyfile_dict.get('token_uri', GOOGLE_TOKEN_URI),
            revoke_uri=keyfile_dict.get('revoke_uri', GOOGLE_REVOKE_URI),
		)
		credential._private_key_pkcs8_pem = keyfile_dict['private_key']
		return credential

	def open_sheet(self):
		if self.bootcamp == "PYTHON":
			sheet = self.client.open(get_env('GAPPS_SHEET_NAME')).worksheet('sheet1')
		elif self.bootcamp == "ML":
			sheet = self.client.open(get_env('GAPPS_SHEET_NAME')).worksheet('sheet2')
		return sheet