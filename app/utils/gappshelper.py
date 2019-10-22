import gspread
from os import path
from config import get_env
from oauth2client import crypt, GOOGLE_TOKEN_URI, GOOGLE_REVOKE_URI
from oauth2client.service_account import ServiceAccountCredentials


class GappsHelper:

	def __init__(self):
		# setup for google sheet - Google Drive API Instance
		self.scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
		self.credentials = self.credentials_from_env(self.scope)
		self.client = gspread.authorize(self.credentials)

	def credentials_from_env(self, scopes):
		keyfile_dict = {}
		try:
			keyfile_dict['private_key'] = get_env('SC_PRIVATE_KEY')
		except Exception:
			raise Exception('spam', 'SC_PRIVATE_KEY')
		try:
			keyfile_dict["auth_uri"] = get_env('SC_AUTH_URI')
		except Exception:
			raise Exception('spam', 'SC_AUTH_URI')
		try:
			keyfile_dict["token_uri"] = get_env('SC_TOKEN_URI')
		except Exception:
			raise Exception('spam', 'SC_TOKEN_URI')
		try:
			keyfile_dict["client_email"] = get_env('SC_CLIENT_EMAIL')
		except Exception:
			raise Exception('spam', 'SC_CLIENT_EMAIL')
		try:
			keyfile_dict["private_key_id"] = get_env('SC_PRIVATE_KEY_ID')
		except Exception:
			raise Exception('spam', 'SC_PRIVATE_KEY_ID')
		try:
			keyfile_dict["client_id"] = get_env('SC_CLIENT_ID')
		except Exception:
			raise Exception('spam', 'SC_CLIENT_ID')
		try:
			signer = crypt.Signer.from_string(keyfile_dict['private_key'])
		except Exception:
			raise Exception('spam', 'Signer')
		try:
			credential = ServiceAccountCredentials(
				keyfile_dict["client_email"],
				signer,
				scopes=scopes,
				private_key_id=keyfile_dict["private_key_id"],
				client_id=keyfile_dict["client_id"],
				token_uri=keyfile_dict.get('token_uri', GOOGLE_TOKEN_URI),
				revoke_uri=keyfile_dict.get('revoke_uri', GOOGLE_REVOKE_URI),
			)
		except Exception:
			raise Exception('spam', 'ServiceAccountCredentials')
		try:
			credential._private_key_pkcs8_pem = keyfile_dict['private_key']
		except Exception:
			raise Exception('spam', 'private_key')
		return credential

	def open_sheet(self):
		sheet = self.client.open(get_env('GAPPS_SHEET_NAME')).sheet1
		return sheet