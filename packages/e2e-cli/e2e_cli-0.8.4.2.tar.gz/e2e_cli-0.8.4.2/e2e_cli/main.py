import argparse

from e2e_cli.commands_routing import CommandsRouting


class Main:
    def __init__(self):
        pass

    def FormatUsage(self, parser, action):
        format_string = "e2e_cli" + " " + action + " [-h]" + " {add,delete,list} ... " + "alias"
        parser.usage = format_string

    def FormatUsageCommand(self, parser, action, command):
        format_string = "e2e_cli" + " " + action + " [-h] " + command + " alias"
        parser.usage = format_string

    def config(self, parser):
        config_sub_parser = parser.add_subparsers(title="Config Commands", dest="config_commands")
        config_add_sub_parser = config_sub_parser.add_parser("add", help="To add api key and auth token")
        config_delete_sub_parser = config_sub_parser.add_parser("delete", help="To delete api key and auth token")
        parser.add_argument("alias", type=str, help="The name of your API access credentials")
        self.FormatUsageCommand(config_add_sub_parser, "config", "add")
        self.FormatUsageCommand(config_delete_sub_parser, "config", "delete")

    def node(self, parser):
        node_sub_parser = parser.add_subparsers(title="node Commands", dest="node_commands")
        node_add_sub_parser = node_sub_parser.add_parser("add", help="To create a new node")
        node_delete_sub_parser = node_sub_parser.add_parser("delete", help="To delete a specific node")
        node_list_sub_parser = node_sub_parser.add_parser("list", help="To get a list of all nodes")
        node_get_sub_parser = node_sub_parser.add_parser("get", help="To get a list of all nodes")
        parser.add_argument("alias", type=str, help="The name of your API access credentials")
        self.FormatUsageCommand(node_add_sub_parser, "node", "add")
        self.FormatUsageCommand(node_delete_sub_parser, "node", "delete")
        self.FormatUsageCommand(node_list_sub_parser, "node", "list")
        self.FormatUsageCommand(node_get_sub_parser, "node", "get")

    def lb(self, parser):
        node_sub_parser = parser.add_subparsers(title="LB Commands", dest="lb_commands")
        node_add_sub_parser = node_sub_parser.add_parser("add", help="To create a new node")
        node_delete_sub_parser = node_sub_parser.add_parser("delete", help="To delete a specific node")
        node_list_sub_parser = node_sub_parser.add_parser("list", help="To get a list of all nodes")
        node_edit_sub_parser = node_sub_parser.add_parser("edit", help="To get a list of all nodes")
        parser.add_argument("alias", type=str, help="The name of your API access credentials")
        self.FormatUsageCommand(node_add_sub_parser, "node", "add")
        self.FormatUsageCommand(node_delete_sub_parser, "node", "delete")
        self.FormatUsageCommand(node_list_sub_parser, "node", "list")
        self.FormatUsageCommand(node_edit_sub_parser, "node", "edit")


def run_main_class():
    parser = argparse.ArgumentParser(description="E2E CLI")
    sub_parsers = parser.add_subparsers(title="Commands", dest="command")
    config_parser = sub_parsers.add_parser("config", help="To add or delete api key and auth token")
    node_parser = sub_parsers.add_parser("node", help="To apply crud operations over Nodes")
    lb_parser = sub_parsers.add_parser("lb", help="To apply operations over Load-Balancer")
    m = Main()
    m.config(config_parser)
    m.node(node_parser)
    m.lb(lb_parser)
    m.FormatUsage(config_parser, "config")
    m.FormatUsage(node_parser, "node")
    m.FormatUsage(lb_parser, "lb")
    args = parser.parse_args()
    commands_route = CommandsRouting(args)
    commands_route.route()
