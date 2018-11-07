# coding=utf-8
"""
CLI Entry-point

"""
import argparse
import sys


def main():
    """Main entry-point to the pg_lifecycle application"""
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    sys.stderr.write('ERROR: Unimplemented CLI stub')
    sys.exit(1)
