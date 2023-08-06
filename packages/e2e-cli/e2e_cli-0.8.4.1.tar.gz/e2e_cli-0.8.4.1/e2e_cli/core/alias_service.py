import json
import os

class AliasServices:
    def __init__(self, alias):
        self.alias = alias

    def get_api_credentials(self):
        file= os.path.expanduser("~") + '/.E2E_CLI/config.json'
        file_reference = open(file, "r")
        config_file_object = json.loads(file_reference.read())
        if self.alias in config_file_object:
            return {"api_credentials": config_file_object[self.alias],
                    "message": "Valid alias"}
        else:
            return {"message": "Invalid alias provided"}



def get_user_cred(name):
        
    file= os.path.expanduser("~") + '/.E2E_CLI/config.json'

    # Opening JSON file
    f = open(file)
    
    # returns JSON object as 
    # a dictionary
    data = json.load(f)
    
    # Closing file
    f.close()

    if(name in data):
        return[ data[name]['api_auth_token'], data[name]['api_key'] ]
    else:
        print("the given alias/credential doesn't exist")
        return None
