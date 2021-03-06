# coding=utf-8
"""
CLI Entry-point

"""
import argparse
import logging
import os
from os import path
import pwd
import sys

from pg_lifecycle import build, common, deploy, generate, __version__

LOGGER = logging.getLogger(__name__)
LOGGING_FORMAT = '[%(asctime)-15s] %(levelname)-8s %(message)s'


def add_actions_to_parser(parser):
    """Add action CLI options to the parser.

    :param argparse.ArgumentParser parser: The parser to add the args to

    """
    sp = parser.add_subparsers(
        title='Action',
        description='The action or operation to perform',
        dest='action',
        required=True,
        metavar='ACTION')
    gen = sp.add_parser('generate-project', help='Generate a project')
    gen.add_argument(
        '-e',
        '--extract',
        action='store_true',
        help='Extract schema from an existing database')
    gen.add_argument(
        '--force',
        action='store_true',
        help='Write to destination path even if it already exists')
    gen.add_argument(
        '--gitkeep',
        action='store_true',
        help='Create a .gitkeep file in empty directories')
    gen.add_argument(
        '--remove-empty',
        action='store_true',
        help='Remove empty directories after generation')
    gen.add_argument(
        'dest',
        nargs=1,
        metavar='DEST',
        help='Destination directory for the new project')

    build = sp.add_parser('build', help='Build DDL for the project')
    build.add_argument(
        '--diff',
        action='store_true',
        help='Build DDL as changes to the current database')
    build.add_argument(
        'file',
        nargs='?',
        action='store',
        default='stdout',
        help='Output file (default: stdout)',
        metavar='FILE')

    deploy = sp.add_parser('deploy', help='Deploy DDL for the project')
    deploy.add_argument(
        '--diff',
        action='store_true',
        help='Deploy DDL changes to the current database')
    deploy.add_argument(
        '--dry-run',
        action='store_true',
        help='Perform a dry-run deployment without actually deploying')


def add_connection_options_to_parser(parser):
    """Add PostgreSQL connection CLI options to the parser.

    :param argparse.ArgumentParser parser: The parser to add the args to

    """
    conn = parser.add_argument_group('Connection Options')
    conn.add_argument(
        '-d',
        '--dbname',
        action='store',
        default=get_username(),
        help='database name to connect to')
    conn.add_argument(
        '-h',
        '--host',
        action='store',
        default='localhost',
        help='database server host or socket directory')
    conn.add_argument(
        '-p',
        '--port',
        action='store',
        type=int,
        default=5432,
        help='database server port number')
    conn.add_argument(
        '-U',
        '--username',
        action='store',
        default=get_username(),
        help='The PostgreSQL username to operate as')
    conn.add_argument(
        '-w',
        '--no-password',
        action='store_true',
        help='never prompt for password')
    conn.add_argument(
        '-W',
        '--password',
        action='store_true',
        help='force password prompt '
        '(should happen  automatically)')
    conn.add_argument(
        '--role',
        action='store',
        help='Role to assume when connecting to a database')


def add_ddl_options_to_parser(parser):
    """Add DDL creation options to the parser.

    :param argparse.ArgumentParser parser: The parser to add the args to

    """
    control = parser.add_argument_group('DDL Options')
    control.add_argument(
        '-O',
        '--no-owner',
        action='store_true',
        help='skip restoration of object ownership')
    control.add_argument(
        '-x',
        '--no-privileges',
        action='store_true',
        help='do not include privileges (grant/revoke)')
    control.add_argument(
        '--no-security-labels',
        action='store_true',
        help='do not include security label assignments')
    control.add_argument(
        '--no-tablespaces',
        action='store_true',
        help='do not include tablespace assignments')


def add_logging_options_to_parser(parser):
    """Add logging options to the parser.

    :param argparse.ArgumentParser parser: The parser to add the args to

    """
    group = parser.add_argument_group(title='Logging Options')
    group.add_argument(
        '-L',
        '--log-file',
        action='store',
        help='Log to the specified filename. If not specified, '
        'log output is sent to STDOUT')
    group.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='Increase output verbosity')
    group.add_argument(
        '--debug', action='store_true', help='Extra verbose debug logging')


def configure_logging(args):
    """Configure Python logging.

    :param argparse.namespace args: The parsed cli arguments

    """
    level = logging.WARNING
    if args.verbose:
        level = logging.INFO
    elif args.debug:
        level = logging.DEBUG
    filename = args.log_file if args.log_file else None
    if filename:
        filename = path.abspath(filename)
        if not path.exists(path.dirname(filename)):
            filename = None
    logging.basicConfig(level=level, filename=filename,
                        format=LOGGING_FORMAT)


def get_username():
    """Return the username of the current process.

    :rtype: str

    """
    return pwd.getpwuid(os.getuid())[0]


def parse_cli_arguments():
    """Create the CLI parser and parse the arguments.

    :return argparse.namespace args: The parsed cli arguments

    """
    parser = argparse.ArgumentParser(
        description='PostgreSQL Schema Management',
        conflict_handler='resolve',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    add_connection_options_to_parser(parser)
    add_ddl_options_to_parser(parser)
    add_logging_options_to_parser(parser)
    parser.add_argument(
        '-V',
        '--version',
        action='store_true',
        help='output version information, then exit')
    add_actions_to_parser(parser)
    return parser.parse_args()


def run():
    """Main entry-point to the pg_lifecycle application"""
    args = parse_cli_arguments()
    configure_logging(args)
    LOGGER.info('pg_lifecycle v%s starting %s', __version__, args.action)
    if args.action == 'build':
        build.Build(args).run()
    elif args.action == 'deploy':
        deploy.Deploy(args).run()
    elif args.action == 'generate-project':
        if args.gitkeep and args.remove_empty_dirs:
            common.exit_application(
                'Can not specify --gitkeep and --remove-empty-dirs', 2)
        generate.Generate(args).run()
    else:
        common.exit_application('Invalid action specified', 1)
