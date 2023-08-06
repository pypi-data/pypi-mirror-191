import subprocess

from e2e_cli.node.node import NodeCrud

class NodeRouting:
    def __init__(self, arguments):
        self.arguments = arguments
        

    def route(self):
        if self.arguments.node_commands is None:
            subprocess.call(['e2e_cli', 'node', '-h'])

        elif self.arguments.node_commands == 'add':
            Node_operations = NodeCrud(alias=self.arguments.alias )
            if(Node_operations.possible):
                        try:
                           Node_operations.add_node()
                        except KeyboardInterrupt:
                            print("\n")   

        elif self.arguments.node_commands == 'delete':
            Node_operations = NodeCrud(alias=self.arguments.alias)
            if(Node_operations.possible):
                        try:
                           Node_operations.delete_node()
                        except KeyboardInterrupt:
                            print("\n")

        elif self.arguments.node_commands == 'get':
            Node_operations = NodeCrud(alias=self.arguments.alias)
            if(Node_operations.possible):
                        try:
                           Node_operations.get_node_by_id()
                        except:
                            print("\n")   
        
        elif self.arguments.node_commands == 'list':
            Node_operations = NodeCrud(alias=self.arguments.alias)
            if(Node_operations.possible):
                        try: 
                           Node_operations.list_node()
                        except KeyboardInterrupt:
                            print("\n")   


