# coding=utf-8
import os
from os import path

ALTER = 'ALTER'
COMMENT = 'COMMENT'
CREATE = 'CREATE'
CREATE_OR_REPLACE = 'CREATE OR REPLACE'
GRANT = 'GRANT'
REVOKE = 'REVOKE'
SET = 'SET'

COLUMN = 'COLUMN'
CONSTRAINT = 'CONSTRAINT'
DOMAIN = 'DOMAIN'
FUNCTION = 'FUNCTION'
INDEX = 'INDEX'
ROLE = 'ROLE'
RULE = 'RULE'
SCHEMA = 'SCHEMA'
SEQUENCE = 'SEQUENCE'
TABLE = 'TABLE'
TRIGGER = 'TRIGGER'
TYPE = 'TYPE'
VIEW = 'VIEW'

PATHS = {
    CONSTRAINT: 'constraints',
    DOMAIN: 'domains',
    FUNCTION: 'functions',
    INDEX: 'indexes',
    RULE: 'rules',
    SCHEMA: 'schemata',
    SEQUENCE: 'sequences',
    TABLE: 'tables',
    TRIGGER: 'triggers',
    TYPE: 'types',
    VIEW: 'views'
}


def ensure_directory(filename):
    """Ensures that the directory exists for the specified file.

    :param str filename: The file to ensure the directory exists for

    """
    dir_path = path.dirname(filename)
    if not path.exists(dir_path):
        os.makedirs(dir_path)
