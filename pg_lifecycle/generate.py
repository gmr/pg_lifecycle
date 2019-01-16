# coding=utf-8
"""
Generates Project Structure

"""
import logging
import os
from os import path
import pickle
import shutil
import subprocess
import tempfile
import toposort

from pgdumplib import directory, toc

from pg_lifecycle import common

LOGGER = logging.getLogger(__name__)


class Generate:
    """Generate Project Structure"""

    def __init__(self, args):
        self.args = args
        self.dump_path = path.join(
            tempfile.gettempdir(), 'pg-lifecycle-{}'.format(os.getpid()))
        self.dump_reader = None
        self.included = set({})
        self.project_path = path.abspath(args.dest[0])
        self.public_id = None

    def run(self):
        """Implement as core logic for generating the project"""
        if path.exists(self.project_path) and not self.args.force:
            common.exit_application(
                '{} already exists'.format(self.project_path), 3)
        LOGGER.info('Generating project in %s', self.project_path)
        self._dump_database()
        self._create_directories()

        self.dump_reader = directory.Reader(self.dump_path)
        self._generate_ddl()

        # self._cleanup_dump()
        LOGGER.info('DDL project generated in %s after processing %i objects',
                    self.args.dest[0], len(self.included))

    def _create_directories(self):
        LOGGER.debug('Creating %s', self.project_path)
        os.makedirs(self.project_path, exist_ok=self.args.force)
        for value in common.PATHS.values():
            subdir_path = path.join(self.project_path, value)
            try:
                os.makedirs(subdir_path, exist_ok=self.args.force)
            except FileExistsError:
                pass
            if self.args.gitkeep:
                gitkeep_path = path.join(subdir_path, '.gitkeep')
                open(gitkeep_path, 'w').close()

    def _cleanup_dump(self):
        """Remove the temp files used in creation"""
        LOGGER.debug('Removing dump from %s', self.dump_path)
        shutil.rmtree(self.dump_path)

    def _dump_database(self):
        """Return the pg_dump command to run to backup the database.

        :param argparse.namespace args: The CLI arguments

        """
        LOGGER.info('Dumping %s:%s/%s to %s',
                    self.args.host, self.args.port, self.args.dbname,
                    self.dump_path)
        try:
            subprocess.check_output(
                self._dump_command(), stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as error:
            output = error.stderr.decode('utf-8')
            LOGGER.error('Failed to dump %s:%s/%s (%r): %s',
                         self.args.host, self.args.port, self.args.dbname,
                         error.returncode, output.strip())
            raise

    def _dump_command(self):
        """Return the pg_dump command to run to backup the database.

        :rtype: list

        """
        command = [
            'pg_dump',
            '-U', self.args.username,
            '-h', self.args.host,
            '-p', str(self.args.port),
            '-d', self.args.dbname,
            '-f', self.dump_path,
            '-Fd', '--schema-only']
        for optional in {'no_owner',
                         'no_privileges',
                         'no_security_labels',
                         'no_tablespaces'}:
            if getattr(self.args, optional, False):
                command += ['--{}'.format(optional.replace('_', '-'))]
        if self.args.role:
            command += ['--role', self.args.role]
        LOGGER.debug('Dump command: %r', ' '.join(command))
        return command

    @staticmethod
    def _function_filename(tag, filenames):
        """Create a filename for a function file, using an auto-incrementing
        value for duplicate functions with different parameters.

        :param str tag: The entity tag
        :param set filenames: Already used filenames
        :rtype: str

        """
        base = tag.split('(')[0]
        parts = tag.count(',')
        filename = '{}-{}.sql'.format(base, parts)
        if filename not in filenames:
            return filename
        counter = 2
        while True:
            filename = '{}-{}_{}.sql'.format(base, parts, counter)
            if filename not in filenames:
                return filename
            counter += 1

    def _generate_ddl(self):
        """Top-level iterator for generating DDL files"""
        LOGGER.info('Generating DDL generated with pg_dump v%s/PostgreSQL v%s',
                    self.dump_reader.dump_version,
                    self.dump_reader.server_version)

        files = list([])
        for obj_type in [common.AGGREGATE,
                         common.CAST,
                         common.COLLATION,
                         common.CONVERSION,
                         common.DOMAIN,
                         common.EXTENSION,
                         common.FOREIGN_DATA_WRAPPER,
                         common.FUNCTION,
                         common.MATERIALIZED_VIEW,
                         common.PL,
                         common.PROCEDURE,
                         common.PUBLICATION,
                         common.RULE,
                         common.SCHEMA,
                         common.SEQUENCE,
                         common.SERVER,
                         common.SUBSCRIPTION,
                         common.TABLE,
                         common.TEXT_SEARCH_CONFIGURATION,
                         common.TEXT_SEARCH_DICTIONARY,
                         common.TYPE,
                         common.TRIGGER,
                         common.VIEW]:
            files += self._generate_common(obj_type)
        directives = self._generate_directives()
        if directives:
            files.append(directives)

        operators = self._generate_operators()
        if operators:
            files.append(operators)

        self._generate_manifest(files)

        if self.args.gitkeep:
            self._remove_unneeded_gitkeeps()
        if self.args.remove_empty_dirs:
            self._remove_empty_directories()

        for entry in self.dump_reader.toc.entries:
            if entry.dump_id not in self.included:
                if entry.desc == common.SHELL_TYPE:
                    LOGGER.warning('Ignoring shell type for %s', entry.tag)
                else:
                    LOGGER.warning('Unprocessed entry: %r', entry)

    def _generate_common(self, obj_type):
        """Generate the SQL files for the given object type, returning the list
        of files that were generated.

        :param str obj_type: The type of object to generate for

        :rtype: list([dump_id, filename])

        """
        LOGGER.debug('Generating DDL for %s', obj_type)
        ddl, files, filenames = {}, [], set({})
        for entry in self.dump_reader.toc.entries:
            if entry.desc == obj_type:
                self.included.add(entry.dump_id)
                if obj_type in (common.FUNCTION, common.TYPE):
                    base_name = self._function_filename(entry.tag, filenames)
                else:
                    base_name = '{}.sql'.format(entry.tag.replace(' ', '-'))
                filename = path.join(common.PATHS[obj_type], base_name)
                if entry.namespace:
                    filename = path.join(
                        common.PATHS[obj_type], entry.namespace,
                        base_name)
                filenames.add(base_name)
                ddl[entry.dump_id] = {
                    'filename': filename,
                    'dependencies': entry.dependencies,
                    'includes': [],
                    'entry': entry
                }
            elif entry.desc in [common.ACL, common.COMMENT] and \
                    entry.tag == 'SCHEMA public':
                # Special case for public schema, create not included in dump
                if entry.dependencies[0] not in self.included:
                    self.included.add(entry.dependencies[0])
                    ddl[entry.dependencies[0]] = {
                        'filename': path.join(
                            common.PATHS[common.SCHEMA], 'public.sql'),
                        'dependencies': [],
                        'includes': [],
                        'entry': toc.Entry(
                            entry.dependencies[0], None, None, None, entry.tag,
                            common.SCHEMA, None, '', None, None, None, None,
                            None, None, [])
                    }
                self._maybe_add_entity(ddl, entry, entry.desc)
            else:
                for child_type in common.CHILD_OBJ_TYPES:
                    if entry.desc == child_type:
                        self._maybe_add_entity(ddl, entry, child_type)
                        break
        return self._generate_files(ddl)

    def _generate_directives(self):
        """Generate the SQL files for the given object type, returning the list
        of files that were generated.

        :rtype: list([dump_id, filename])

        """
        filename = 'directives.sql'
        databases, output = [], []
        for entry in self.dump_reader.toc.entries:
            if (entry.desc in [common.ENCODING,
                               common.STDSTRINGS,
                               common.SEARCHPATH] and
                    entry.section == common.PRE_DATA):
                self.included.add(entry.dump_id)
                output.append(entry.defn)
            elif entry.desc == common.DATABASE:
                self.included.add(entry.dump_id)
                databases.append(entry.dump_id)
            elif entry.desc == common.COMMENT and \
                    any([d in databases for d in entry.dependencies]):
                self.included.add(entry.dump_id)
                output.append(entry.defn)
        if output:
            with open(path.join(self.project_path, filename), 'w') as handle:
                handle.write('-- Common Directives / Settings\n\n')
                handle.write(''.join(output))
            return DDLFile(-1, filename, set([]), set([]))

    def _generate_operators(self):
        """Generate the SQL file for operators which dont name so well in
        individual files

        :rtype: list([dump_id, filename])

        """
        filename = 'operators.sql'
        entries, dependencies, includes = {}, set({}), set([])
        for entry in self.dump_reader.toc.entries:
            if entry.desc.startswith(common.OPERATOR):
                self.included.add(entry.dump_id)
                entries[entry.dump_id] = entry
        if entries:
            values = {e.dump_id: set(e.dependencies) for e in entries.values()}
            includes = toposort.toposort_flatten(values)
            with open(path.join(self.project_path, filename), 'w') as handle:
                handle.write('-- Operators\n\n')
                for dump_id in includes:
                    if dump_id not in entries:
                        dependencies.add(dump_id)
                        continue
                    handle.write('{}\n'.format(entries[dump_id].defn))
                    dependencies.update(set(entries[dump_id].dependencies))
            return DDLFile(-1, filename, includes,
                           dependencies.difference(includes))

    def _generate_files(self, ddl):
        """Generic SQL file generation for building object specific SQL files.

        :param dict ddl: The DDL to generate files for
        :rtype: list([dump_id, filename])

        """
        files = []
        for dump_id, obj in ddl.items():
            files.append(
                DDLFile(dump_id, obj['filename'], set(obj['includes']),
                        set(obj['dependencies'])))
            file_path = path.join(self.project_path, obj['filename'])
            if not path.exists(path.dirname(file_path)):
                os.makedirs(path.dirname(file_path))
            if path.exists(file_path):
                raise ValueError('Path Already Exists: {}'.format(file_path))
            with open(file_path, 'w') as handle:
                tag = obj['entry'].tag if not obj['entry'].namespace \
                    else '{}.{}'.format(
                        obj['entry'].namespace, obj['entry'].tag)
                handle.write('-- DDL for {}\n\n'.format(tag))
                handle.write(obj['entry'].defn)
                for child_type in common.CHILD_OBJ_TYPES:
                    if obj.get(child_type):
                        handle.write('\n-- {}s for {}\n\n{}'.format(
                            child_type, tag, ''.join(obj[child_type])))
        return files

    def _generate_manifest(self, files):
        """Generate the manifest file for all of the DDL."""
        file_path = path.join(self.project_path, common.MANIFEST)
        with open(file_path, 'wb') as handle:
            pickle.dump(files, handle)

    def _maybe_add_entity(self, ddl, entry, object_type):
        """Maybe Add an entry to a list of entries for a parent entity
        if the dependency match is made.

        :param dict ddl: The collection of DDL to check for parents in
        :param pgdumplib.tog.Entry entry: The entry to examine
        :param object_type: The type of object being examined

        """
        if entry.desc == object_type:
            for parent in ddl.keys():
                if parent in entry.dependencies:
                    if object_type not in ddl[parent]:
                        ddl[parent][object_type] = list([])
                    ddl[parent]['includes'].append(entry.dump_id)
                    ddl[parent][object_type].append(entry.defn)
                    self.included.add(entry.dump_id)
                    for dependency in entry.dependencies:
                        if dependency not in entry.dependencies and \
                                dependency != parent:
                            ddl[parent]['dependencies'].append(dependency)

    def _remove_empty_directories(self):
        """Remove any empty directories"""
        for subdir in common.PATHS.values():
            dir_path = path.join(self.project_path, subdir)
            for root, dirs, files in os.walk(dir_path):
                if not len(dirs) and not len(files):
                    os.rmdir(root)

    def _remove_unneeded_gitkeeps(self):
        """Remove any .gitkeep files in directories with subdirectories or
        files in the directory.

        """
        for subdir in common.PATHS.values():
            dir_path = path.join(self.project_path, subdir)
            for root, dirs, files in os.walk(dir_path):
                if (len(dirs) or len(files) > 1) and '.gitkeep' in files:
                    file_path = path.join(root, '.gitkeep')
                    LOGGER.debug('Removing %s', file_path)
                    os.unlink(file_path)


class DDLFile:
    """Class used for managing dependencies in the manifest"""
    __slots__ = ['id', 'path', 'dependencies', 'includes']

    def __init__(self, id_value, path_value, includes, dependencies):
        self.id = id_value
        self.path = path_value
        self.includes = includes
        self.dependencies = dependencies

    def __repr__(self):
        return '<DDLFile {} path={} dependencies={}>'.format(
            self.id, self.path, self.dependencies)

    def __str__(self):
        return repr(self)
