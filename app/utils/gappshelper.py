import gspread
from os import path
from config import get_env
import oauth2client
from oauth2client import crypt
from oauth2client.service_account import ServiceAccountCredentials


class GappsHelper:

	def __init__(self):
		# setup for google sheet - Google Drive API Instance
		self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		self.credentials = self.credentials_from_env(self.scope)
		self.client = gspread.authorize(self.credentials)

	def credentials_from_env(self, scopes):
		keyfile_dict = {}
		keyfile_dict['private_key'] = get_env('SC_PRIVATE_KEY')
		keyfile_dict["auth_uri"] = get_env('SC_AUTH_URI')
		keyfile_dict["token_uri"] = get_env('SC_TOKEN_URI')
		signer = crypt.Signer.from_string(keyfile_dict['private_key'])
		credential = ServiceAccountCredentials(
			get_env('SC_CLIENT_EMAIL'),
			signer,
			scopes=scopes,
			private_key_id=get_env('SC_PRIVATE_KEY_ID'),
			client_id=get_env('SC_CLIENT_ID'),
			token_uri=keyfile_dict.get('token_uri', oauth2client.GOOGLE_TOKEN_URI),
            revoke_uri=keyfile_dict.get('revoke_uri', oauth2client.GOOGLE_REVOKE_URI),
		)
		credential._private_key_pkcs8_pem = keyfile_dict['private_key']
		return credential

	def open_sheet(self):
		sheet = self.client.open(get_env('GAPPS_SHEET_NAME')).sheet1
		return sheet.get_all_records(empty2zero=False, head=1, default_blank='')