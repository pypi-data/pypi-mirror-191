import subprocess

from e2e_cli.loadbalancer.lb import LBClass


class LBRouting:
    def __init__(self, arguments):
        self.arguments = arguments

    def route(self):
        if self.arguments.lb_commands is None:
            subprocess.call(['e2e_cli', 'lb', '-h'])

        elif self.arguments.lb_commands == 'add':
            lb_class_object = LBClass(alias=self.arguments.alias)
            try:
               lb_class_object.create_lb()
            except KeyboardInterrupt:
                print("\n")
                pass

        elif self.arguments.lb_commands == 'list' or self.arguments.lb_commands == 'ls':
            lb_class_object = LBClass(alias=self.arguments.alias)
            try:
               lb_class_object.list_lb()
            except KeyboardInterrupt:
                print("\n")
                pass

        elif self.arguments.lb_commands == 'delete':
            lb_class_object = LBClass(alias=self.arguments.alias)
            try:
               lb_class_object.delete_lb()
            except KeyboardInterrupt:
                print("\n")
                pass

        elif self.arguments.lb_commands == 'edit':
            lb_class_object = LBClass(alias=self.arguments.alias)
            try:
               lb_class_object.edit_lb()
            except KeyboardInterrupt:
                print("\n")
                pass
