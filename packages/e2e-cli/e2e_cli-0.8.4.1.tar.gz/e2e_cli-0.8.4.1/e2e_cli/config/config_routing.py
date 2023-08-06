import subprocess

from e2e_cli.config.config import AuthConfig


class ConfigRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self):
        if self.arguments.config_commands is None:
            subprocess.call(['e2e_cli', 'config', '-h'])

        elif self.arguments.config_commands == 'add':
            try:
                api_key = input("Enter your api key: ")
                auth_token = input("Enter your auth token: ")
                auth_config_object = AuthConfig(alias=self.arguments.alias,
                                                api_key=api_key,
                                                api_auth_token=auth_token)
                auth_config_object.add_to_config()
            except KeyboardInterrupt:
                print("\n")
                pass

        elif self.arguments.config_commands == 'delete':
            confirmation =input("are you sure you want to delete press y for yes, else any other key : ")
            if(confirmation.lower()=='y'):
                auth_config_object = AuthConfig(alias=self.arguments.alias)
                try:
                    auth_config_object.delete_from_config()
                except:
                    print("\n")
                    pass  
