# coding=utf-8
"""Common constants and shared methods"""
import logging
import sys

LOGGER = logging.getLogger(__name__)

MANIFEST = 'MANIFEST.pgl'

PRE_DATA = 'Pre-Data'
DATA = 'Data'
POST_DATA = 'Post-Data'

ALTER = 'ALTER'
COMMENT = 'COMMENT'
CREATE = 'CREATE'
CREATE_OR_REPLACE = 'CREATE OR REPLACE'
GRANT = 'GRANT'
REVOKE = 'REVOKE'
SET = 'SET'

AGGREGATE = 'AGGREGATE'
ACL = 'ACL'
CAST = 'CAST'
CHECK_CONSTRAINT = 'CHECK CONSTRAINT'
COLUMN = 'COLUMN'
COLLATION = 'COLLATION'
CONSTRAINT = 'CONSTRAINT'
CONVERSION = 'CONVERSION'
DATABASE = 'DATABASE'
DEFAULT = 'DEFAULT'
DIRECTIVE = 'DIRECTIVE'
DOMAIN = 'DOMAIN'
ENCODING = 'ENCODING'
EVENT_TRIGGER = 'EVENT TRIGGER'
EXTENSION = 'EXTENSION'
FOREIGN_DATA_WRAPPER = 'FOREIGN DATA WRAPPER'
FOREIGN_TABLE = 'FOREIGN TABLE'
FK_CONSTRAINT = 'FK CONSTRAINT'
FUNCTION = 'FUNCTION'
INDEX = 'INDEX'
MATERIALIZED_VIEW = 'MATERIALIZED VIEW'
OPERATOR = 'OPERATOR'
POLICY = 'POLICY'
PL = 'PROCEDURAL LANGUAGE'
PROCEDURE = 'PROCEDURE'
PUBLICATION = 'PUBLICATION'
PUBLICATION_TABLE = 'PUBLICATION TABLE'
ROLE = 'ROLE'
RULE = 'RULE'
SEARCHPATH = 'SEARCHPATH'
SEQUENCE_OWNED_BY = 'SEQUENCE OWNED BY'
SCHEMA = 'SCHEMA'
SECURITY_LABEL = 'SECURITY LABEL'
SEQUENCE = 'SEQUENCE'
SERVER = 'SERVER'
SHELL_TYPE = 'SHELL TYPE'
STDSTRINGS = 'STDSTRINGS'
SUBSCRIPTION = 'SUBSCRIPTION'
TABLE = 'TABLE'
TABLESPACE = 'TABLESPACE'
TEXT_SEARCH_DICTIONARY = 'TEXT SEARCH DICTIONARY'
TEXT_SEARCH_CONFIGURATION = 'TEXT SEARCH CONFIGURATION'
TRIGGER = 'TRIGGER'
TYPE = 'TYPE'
USER_MAPPING = 'USER MAPPING'
VIEW = 'VIEW'

CHILD_OBJ_TYPES = [
    DEFAULT,
    COMMENT,
    POLICY,
    CHECK_CONSTRAINT,
    CONSTRAINT,
    FK_CONSTRAINT,
    INDEX,
    ACL,
    SECURITY_LABEL,
    SEQUENCE_OWNED_BY,
    SERVER,
    FOREIGN_TABLE,
    USER_MAPPING,
    PUBLICATION_TABLE
]

PATHS = {
    AGGREGATE: 'functions',
    CAST: 'casts',
    COLLATION: 'collations',
    CONVERSION: 'conversions',
    DOMAIN: 'domains',
    EVENT_TRIGGER: 'event_triggers',
    EXTENSION: 'extensions',
    FOREIGN_DATA_WRAPPER: 'foreign_data_wrappers',
    FUNCTION: 'functions',
    MATERIALIZED_VIEW: 'materialized_views',
    OPERATOR: 'operators',
    PL: 'extensions',
    PROCEDURE: 'procedures',
    PUBLICATION: 'publications',
    ROLE: 'roles',
    RULE: 'rules',
    SCHEMA: 'schemata',
    SEQUENCE: 'sequences',
    SERVER: 'servers',
    SHELL_TYPE: 'types',
    SUBSCRIPTION: 'subscriptions',
    TABLE: 'tables',
    TABLESPACE: 'tablespaces',
    TEXT_SEARCH_CONFIGURATION: 'text_search',
    TEXT_SEARCH_DICTIONARY: 'text_search',
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
