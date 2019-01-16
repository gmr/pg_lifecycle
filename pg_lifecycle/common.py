# coding=utf-8
"""Common constants and shared methods"""
import logging
import sys

LOGGER = logging.getLogger(__name__)

MANIFEST = 'MANIFEST.pgl'

ALTER = 'ALTER'
COMMENT = 'COMMENT'
CREATE = 'CREATE'
CREATE_OR_REPLACE = 'CREATE OR REPLACE'
GRANT = 'GRANT'
REVOKE = 'REVOKE'
SET = 'SET'

ACL = 'ACL'
CAST = 'CAST'
COLUMN = 'COLUMN'
CONSTRAINT = 'CONSTRAINT'
DATABASE = 'DATABASE'
DEFAULT = 'DEFAULT'
DIRECTIVE = 'DIRECTIVE'
DOMAIN = 'DOMAIN'
ENCODING = 'ENCODING'
EXTENSION = 'EXTENSION'
FDW = 'FOREIGN DATA WRAPPER'
FK_CONSTRAINT = 'FK CONSTRAINT'
FUNCTION = 'FUNCTION'
INDEX = 'INDEX'
OPERATOR = 'OPERATOR'
PRE_DATA = 'Pre-Data'
PL = 'PROCEDURAL LANGUAGE'
ROLE = 'ROLE'
RULE = 'RULE'
SEARCHPATH = 'SEARCHPATH'
SEQUENCE_OWNED_BY = 'SEQUENCE OWNED BY'
SCHEMA = 'SCHEMA'
SEQUENCE = 'SEQUENCE'
SERVER = 'SERVER'
SHELL_TYPE = 'SHELL TYPE'
STDSTRINGS = 'STDSTRINGS'
TABLE = 'TABLE'
TRIGGER = 'TRIGGER'
TYPE = 'TYPE'
USER_MAPPING = 'USER MAPPING'
VIEW = 'VIEW'

PATHS = {
    CAST: 'casts',
    CONSTRAINT: 'constraints',
    DOMAIN: 'domains',
    EXTENSION: 'extensions',
    FDW: 'fdws',
    FUNCTION: 'functions',
    OPERATOR: 'operators',
    PL: 'extensions',
    ROLE: 'roles',
    RULE: 'rules',
    SCHEMA: 'schemata',
    SEQUENCE: 'sequences',
    SERVER: 'servers',
    SHELL_TYPE: 'types',
    TABLE: 'tables',
    TRIGGER: 'triggers',
    TYPE: 'types',
    VIEW: 'views'
}


def exit_application(message=None, code=0):
    """Exit the application displaying the message to either INFO or ERROR
    based upon the exist code.

    :param str message: The exit message
    :param int code: The exit code (default: 0)

    """
    if message:
        log_method = LOGGER.info if not code else LOGGER.error
        log_method(message.strip())
    sys.exit(code)
