# coding=utf-8
"""
CLI Entry-point

"""
import argparse
import os
import pwd
import sys


def add_actions_to_parser(parser):
    """Add action CLI options to the parser.

    :param argparse.ArgumentParser parser: The parser to add the args to

    """
    sp = parser.add_subparsers(title='pg_lifecycle Action',
                               description='The action to take when running '
                                           'the pg_lifecycle application.',
                               dest='action', required=True, metavar='ACTION')
    gen = sp.add_parser('generate-project', help='Generate a project')
    gen.add_argument('-e', '--extract', action='store_true',
                     help='Extract schema from an existing database')

    build = sp.add_parser('build', help='Build DDL for the project')
    build.add_argument('--diff', action='store_true',
                       help='Build DDL as changes to the current database')
    build.add_argument('file', nargs='?', action='store', default='stdout',
                       help='Output file (default: stdout)', metavar='FILE')

    deploy = sp.add_parser('deploy', help='Deploy DDL for the project')
    deploy.add_argument('--diff', action='store_true',
                        help='Deploy DDL changes to the current database')
    deploy.add_argument('--dry-run', action='store_true',
                        help='Perform a dry-run deployment without '
                             'actually deploying to the database')


def add_connection_options_to_parser(parser):
    """Add PostgreSQL connection CLI options to the parser.

    :param argparse.ArgumentParser parser: The parser to add the args to

    """
    conn = parser.add_argument_group('Connection Options')
    conn.add_argument('-d', '--dbname', action='store', default=get_username(),
                      help='database name to connect to')
    conn.add_argument('-h', '--host', action='store', default='localhost',
                      help='database server host or socket directory')
    conn.add_argument('-p', '--port', action='store', type=int,
                      default=5432, help='database server port number')
    conn.add_argument('-U', '--username', action='store',
                      default=get_username(),
                      help='The PostgreSQL username to operate as')
    conn.add_argument('-w', '--no-password', action='store_true',
                      help='never prompt for password')
    conn.add_argument('-W', '--password', action='store_true',
                      help='force password prompt '
                           '(should happen  automatically)')
    conn.add_argument('--role', action='store',
                      help='Role to assume when connecting to a database')


def add_ddl_options_to_parser(parser):
    """Add DDL creation options to the parser.

    :param argparse.ArgumentParser parser: The parser to add the args to

    """
    control = parser.add_argument_group('DDL Options')
    control.add_argument('-O', '--no-owner', action='store_true',
                         help='skip restoration of object ownership')
    control.add_argument('-x', '--no-privileges', action='store_true',
                         help='do not include privileges (grant/revoke)')
    control.add_argument('--no-security-labels', action='store_true',
                         help='do not include security label assignments')
    control.add_argument('--no-tablespaces', action='store_true',
                         help='do not include tablespace assignments')


def add_logging_options_to_parser(parser):
    """Add logging options to the parser.

    :param argparse.ArgumentParser parser: The parser to add the args to

    """
    group = parser.add_argument_group(title='Logging Options')
    group.add_argument('-L', '--log-file', action='store',
                       help='Log to the specified filename. If not specified, '
                            'log output is sent to STDOUT')
    group.add_argument('-v', '--verbose', action='store_true',
                       help='Increase output verbosity')
    group.add_argument('--debug', action='store_true',
                       help='Extra verbose debug logging')


def get_username():
    """Return the username of the current process.

    :rtype: str

    """
    return pwd.getpwuid(os.getuid())[0]


def main():
    """Main entry-point to the pg_lifecycle application"""
    parser = argparse.ArgumentParser(
        description='PostgreSQL Schema Management',
        conflict_handler='resolve',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    add_connection_options_to_parser(parser)
    add_ddl_options_to_parser(parser)
    add_logging_options_to_parser(parser)
    parser.add_argument('-V', '--version', action='store_true',
                        help='output version information, then exit')
    add_actions_to_parser(parser)
    args = parser.parse_args()

    import pprint
    pprint.pprint(args)

    sys.stderr.write('ERROR: Unimplemented CLI stub')
    sys.exit(1)
