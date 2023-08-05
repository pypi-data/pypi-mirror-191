import sys

from SmartCI.manager import CliManager


def main():
    argv = sys.argv
    command = argv[1] if len(argv) >= 2 else ''
    CliManager().run(command, argv[2:])


if __name__ == '__main__':
    main()
