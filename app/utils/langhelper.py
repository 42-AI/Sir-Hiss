from config import get_env
import os
import json

class LangHelper:
    def __init__(self, lang='en', bootcamp=""):
        path = open(get_env('SETTING_FILE')).rsplit('/', 1)
        filename = os.path.join(path[0], bootcamp, path[1])

        with open(filename) as f:
            data = json.load(f)["lang"][lang]
        self.helper = data["helper"]
        self.err_nbarg = data["err_nbarg"]
        self.err_fmtarg = data["err_fmtarg"]
        self.not_logged = data["not_logged"]
        self.not_registered = data["not_registered"]
        self.allready_registered = data["allready_registered"]
        self.registration_success = data["registration_success"]
        self.unregistration_success = data["unregistration_success"]
        self.not_available = data["not_available"]
        self.subject_success = data["subject_success"]
        self.notdwl_subject = data["notdwl_subject"]
        self.already_inpool = data["already_inpool"]
        self.correctionmatch_success = data["correctionmatch_success"]
        self.already_matched = data["already_matched"]
        self.info = data["info"]
        self.match_message = data["match_message"]
        
        