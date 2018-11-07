from os import path
import setuptools

from pg_lifecycle import __version__


def read_requirements(name):
    """Read in the requirements file returning the packages as a list, ignoring
    comments and handling included requirements.

    :param str name: The requirements file name
    :rtype: list

    """
    requirements = []
    try:
        with open(path.join('requires', name)) as req_file:
            for line in req_file:
                if '#' in line:
                    line = line[:line.index('#')]
                line = line.strip()
                if line.startswith('-r'):
                    requirements.extend(read_requirements(line[2:].strip()))
                elif line and not line.startswith('-'):
                    requirements.append(line)
    except IOError:
        pass
    return requirements


setuptools.setup(
    name='pg_lifecycle',
    version=__version__,
    description='A PostgreSQL schema management tool',
    long_description=open('README.rst').read(),
    author='Gavin M. Roy',
    author_email='gavinmroy@gmail.com',
    url='https://github.com/gmr/pg_lifecycle',
    license='BSD',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Database'],
    entry_points={'console_scripts': ['pg_lifecycle=pg_lifecycle.cli:run']},
    include_package_data=True,
    install_requires=read_requirements('installation.txt'),
    packages=['pg_lifecycle'],
    package_data={'': ['LICENSE', 'README.rst']},
    tests_require=read_requirements('testing.txt'),
    test_suite='nose.collector',
    zip_safe=True)
