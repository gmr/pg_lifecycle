pg_lifecycle
============

A PostgreSQL schema management tool.

Usage
-----

.. code-block::

    usage: pg_lifecycle [--help] [-d DBNAME] [-h HOST] [-p PORT] [-U USERNAME]
                        [-w] [-W] [--role ROLE] [-O] [-x] [--no-security-labels]
                        [--no-tablespaces] [-L LOG_FILE] [-v] [--debug] [-V]
                        ACTION ...

    PostgreSQL Schema Management

    optional arguments:
      --help                show this help message and exit
      -V, --version         output version information, then exit (default: False)

    Connection Options:
      -d DBNAME, --dbname DBNAME
                            database name to connect to (default: gavinr)
      -h HOST, --host HOST  database server host or socket directory (default:
                            localhost)
      -p PORT, --port PORT  database server port number (default: 5432)
      -U USERNAME, --username USERNAME
                            The PostgreSQL username to operate as (default:
                            gavinr)
      -w, --no-password     never prompt for password (default: False)
      -W, --password        force password prompt (should happen automatically)
                            (default: False)
      --role ROLE           Role to assume when connecting to a database (default:
                            None)

    DDL Options:
      -O, --no-owner        skip restoration of object ownership (default: False)
      -x, --no-privileges   do not include privileges (grant/revoke) (default:
                            False)
      --no-security-labels  do not include security label assignments (default:
                            False)
      --no-tablespaces      do not include tablespace assignments (default: False)

    Logging Options:
      -L LOG_FILE, --log-file LOG_FILE
                            Log to the specified filename. If not specified, log
                            output is sent to STDOUT (default: None)
      -v, --verbose         Increase output verbosity (default: False)
      --debug               Extra verbose debug logging (default: False)

    Action:
      The action or operation to perform

      ACTION
        generate-project    Generate a project
        build               Build DDL for the project
        deploy              Deploy DDL for the project

Generate Project Usage
~~~~~~~~~~~~~~~~~~~~~~

.. code-block::

    usage: pg_lifecycle generate-project [-h] [-e] DEST

    positional arguments:
      DEST           Destination directory for the new project

    optional arguments:
      -h, --help     show this help message and exit
      -e, --extract  Extract schema from an existing database
      --force        Write to destination path even if it already exists
      --gitkeep      Create a .gitkeep file in empty directories
      --remove-empty Remove empty directories after generation

Build Usage
~~~~~~~~~~~

.. code-block::

    usage: pg_lifecycle build [-h] [--diff] [FILE]

    positional arguments:
      FILE        Output file (default: stdout)

    optional arguments:
      -h, --help  show this help message and exit
      --diff      Build DDL as changes to the current database


Deploy Usage
~~~~~~~~~~~~

.. code-block::

    usage: pg_lifecycle deploy [-h] [--diff] [--dry-run]

    optional arguments:
      -h, --help  show this help message and exit
      --diff      Deploy DDL changes to the current database
      --dry-run   Perform a dry-run deployment without actually deploying to the
                  database
