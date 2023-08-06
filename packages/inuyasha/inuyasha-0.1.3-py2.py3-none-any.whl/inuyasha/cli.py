from argparse import ArgumentParser
import sys

from inuyasha import __description__, __version__


def main():
    # 命令行处理程序入口
    arg_parser = ArgumentParser(description=__description__)
    arg_parser.add_argument("-V", "--version", dest="version", help="show version")
    subparsers = arg_parser.add_subparsers(help="sub-command help")
    args = arg_parser.parse_args()
    print(args.version)

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
        print(f"{__version__}")
        sys.exit(0)


if __name__ == '__main__':
    main()
