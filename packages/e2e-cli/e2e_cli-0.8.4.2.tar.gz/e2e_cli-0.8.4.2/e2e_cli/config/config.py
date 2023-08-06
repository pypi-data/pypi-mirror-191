import json
import os
import platform


class AuthConfig:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.home_directory = os.path.expanduser("~")

    def windows_file_check(self):
        pass

    def linux_file_check(self):
        if not os.path.isdir(self.home_directory + "/.E2E_CLI"):
            return -1
        elif not os.path.isfile(self.home_directory + "/.E2E_CLI/config.json"):
            return 0
        else:
            return 1

    def mac_file_check(self):
        pass

    def check_if_file_exist(self):
        if platform.system() == "Windows":
            return self.windows_file_check()
        elif platform.system() == "Linux":
            return self.linux_file_check()
        elif platform.system() == "Mac":
            return self.mac_file_check()

    def add_json_to_file(self):
        api_access_credentials_object = {"api_key": self.kwargs["api_key"],
                                         "api_auth_token": self.kwargs["api_auth_token"]}
        with open(self.home_directory + '/.E2E_CLI/config.json', 'r+') as file_reference:
            read_string = file_reference.read()
            if read_string == "":
                file_reference.write(json.dumps({self.kwargs["alias"]:
                                                     api_access_credentials_object}))
            else:
                api_access_credentials = json.loads(read_string)
                api_access_credentials.update({self.kwargs["alias"]:
                                                   api_access_credentials_object})
                file_reference.seek(0)
                file_reference.write(json.dumps(api_access_credentials))

    def add_to_config(self):
        file_exist_check_variable = self.check_if_file_exist()
        if file_exist_check_variable == -1:
            os.mkdir(self.home_directory + "/.E2E_CLI")
            self.add_json_to_file()
        elif file_exist_check_variable == 0:
            with open(self.home_directory + '/.E2E_CLI/config.json', 'x'):
                pass
            self.add_json_to_file()
        elif file_exist_check_variable == 1:
            self.add_json_to_file()

    def delete_from_config(self):
        file_exist_check_variable = self.check_if_file_exist()
        if file_exist_check_variable == -1 | file_exist_check_variable == 0:
            print(
                "You need to add your api access credentials using the add functionality\n"
                "To know more please write e2e_cli config add -h on your terminal")

        elif file_exist_check_variable == 1:
            with open(self.home_directory + '/.E2E_CLI/config.json', 'r+') as file_reference:
                file_contents_object = json.loads(file_reference.read())
                delete_output = file_contents_object.pop(self.kwargs["alias"], 'No key found')
                if delete_output == "No key found":
                    print("No such alias found. Please re-check and enter again")
                else:
                    file_reference.seek(0)
                    file_reference.write(json.dumps(file_contents_object))
                    file_reference.truncate()
