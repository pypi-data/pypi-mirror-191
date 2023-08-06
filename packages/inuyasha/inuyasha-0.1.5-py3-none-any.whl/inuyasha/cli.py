from argparse import ArgumentParser
import sys

from inuyasha import __description__, __version__
from inuyasha.scaffold import main_scaffold


def main():
    # 命令行处理程序入口
    arg_parser = ArgumentParser(description=__description__)
    arg_parser.add_argument("-V", "--version", dest="version", action="store_true", help="show version")
    subparsers = arg_parser.add_subparsers(help="sub-command help")
    sub_parser_scaffold = subparsers.add_parser("project", help="Create an inuyasha test project")
    sub_parser_scaffold = subparsers.add_parser("P", help="Create an inuyasha test project")
    sub_parser_scaffold.add_argument("project_name", type=str, nargs="?", help="Specify new project name.")
    args = arg_parser.parse_args()

    if sys.argv[1] in ["-V", "--version"]:
        print(f"{__version__}")
    elif sys.argv[1] in ["-h", "--help"]:
        arg_parser.print_help()
    elif sys.argv[1] in ["P", "project"]:
        sub_parser_scaffold.print_help()
        main_scaffold(args)
    else:
        print(f"Unknown command: {sys.argv[1]}")
        arg_parser.print_help()
        sys.exit(0)
