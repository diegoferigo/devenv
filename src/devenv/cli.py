import argparse


def parse_commandline():
    parser = argparse.ArgumentParser()

    # subparsers = parser.add_subparsers()

    # Parse the commands
    # TODO:
    # start_parser = subparsers.add_parser('start')
    # stop_parser = subparsers.add_parser('stop')

    parser.add_argument('-f', '--file',
                        default='devenv.yml',
                        help='the configuration file (default: devenv.yml)')
    parser.add_argument('-G', '--generate',
                        action='store_true',
                        help='generate output compose file and exit, do not run docker-compose')
    parser.add_argument('-o', '--output',
                        type=argparse.FileType('w'),
                        default='devenv-docker-compose.yml',
                        help='specify an alternate output compose file (default: devenv-docker-compose.yml)')

    (args, extras) = parser.parse_known_args()
    return (args, extras)
