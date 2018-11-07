# coding=utf-8
"""
Builds DDL

"""


class Build:
    """Builds DDL for the project"""

    def __init__(self, args):
        self.args = args

    def run(self):
        """Implement as core logic for building DDL"""
        raise NotImplementedError
