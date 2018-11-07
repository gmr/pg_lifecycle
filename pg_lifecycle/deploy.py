# coding=utf-8
"""
Deploys DDL

"""

from pg_lifecycle import build


class Deploy:
    """Deploy DDL for the project"""

    def __init__(self, args):
        self.args = args
        self.build = build.Build(args)

    def run(self):
        """Implement as core logic for deploying DDL"""
        raise NotImplementedError
