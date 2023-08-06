from argparse import ArgumentParser
import sys

from inuyasha import __description__, __version__


def main():
    # 命令行处理程序入口
    arg_parser = ArgumentParser(description=__description__)
    arg_parser.add_argument("-V", "--version", dest="version", action="store_true", help="show version")
    subparsers = arg_parser.add_subparsers()
    sub_parser_scaffold = subparsers.add_parser("startproject", help="Create a new project with template structure.")
    sub_parser_scaffold.add_argument("project_name", type=str, nargs="?", help="Specify new project name.")
    args = arg_parser.parse_args()

    if sys.argv[1] in ["-V", "--version"]:
        print(f"{__version__}")
    elif sys.argv[1] in ["-h", "--help"]:
        arg_parser.print_help()
    else:
        print(f"Unknown command: {sys.argv[1]}")
        arg_parser.print_help()
        sys.exit(0)

    args = arg_parser.parse_args()

    if args.version:
        sys.exit(0)
