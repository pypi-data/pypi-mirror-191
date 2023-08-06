import argparse

from .version import __version__


def argparse_setup():
    parser = argparse.ArgumentParser(prog='pec', usage='pec ...')
    parser.add_argument('-v', '--version', help='returns module version', action='store_true')

    args = parser.parse_args()
    return args


def main():
    args = argparse_setup()

    # print verion and exit
    if args.version:
        print(f'v{__version__}')
        exit(0)


if __name__ == '__main__':
    main()
