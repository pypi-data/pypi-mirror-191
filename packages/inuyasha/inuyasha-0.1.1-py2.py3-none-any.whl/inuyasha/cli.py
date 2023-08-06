import argparse
import sys

from inuyasha import __description__, __version__


def main():
    # 命令行处理程序入口
    parser = argparse.ArgumentParser(description=__description__)
    parser.add_argument("-V", "--version", dest="version", help="show version")
    subparsers = parser.add_subparsers(help="sub-command help")

    if sys.argv[1] in ["-V", "--version"]:
        print(f"{__version__}")
    elif sys.argv[1] in ["-h", "--help"]:
        parser.print_help()
    else:
        print(f"Unknown command: {sys.argv[1]}")
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.version:
        print(f"{__version__}")
        sys.exit(0)


if __name__ == '__main__':
    main()
