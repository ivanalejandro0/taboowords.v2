# Borrowed from: https://github.com/glue-viz/glue/blob/master/setup.py
# Copyright (c) 2013, Glue developers

import os
import subprocess
import sys

from glob import glob
from setuptools import Command


class BuildQt(Command):
    """
    Defines a command for setup.py that compiles the *.ui and *.qrc files
    into python files.

    It looks for *.ui files in the `ui/` subfolder.
    It looks for *.qrc files in the `resources/` subfolder.
    """

    # I don't think setuptools uses these options
    user_options = [
        ('rcc=', 'r', "Custom rcc command (usually pyside-rcc or pyrcc4)"),
        ('uic=', 'u', 'Custom uic command (usually pyside-uic or pyuic4)')
    ]

    # custom path to start the uri of 'ui' and 'resources'
    base_path = ''

    def initialize_options(self):
        """
        Sets the proper command names for the compiling tools.
        """
        self.pyrcc = 'pyside-rcc'
        self.pyuic = 'pyside-uic'

    def finalize_options(self):
        pass

    def _compile_ui(self, infile, outfile):
        try:
            subprocess.call([self.pyuic, infile, '-o', outfile])
        except OSError:
            print("uic command failed - make sure that pyside-uic "
                  "is in your $PATH")

    def _build_rcc(self, infile, outfile):
        if sys.version_info[0] == 2:
            option = '-py2'
        else:
            option = '-py3'
        try:
            subprocess.call([self.pyrcc, option, infile, '-o', outfile])
        except OSError:
            print("rcc command failed - make sure that "
                  "pyside-rcc is in your $PATH, or specify "
                  "a custom command with --rcc=command")

    def run(self):
        # compile ui files
        for infile in glob(os.path.join(self.base_path, 'ui', '*.ui')):
            directory, ui_filename = os.path.split(infile)
            py_filename = ui_filename.replace('.ui', '.py')
            outfile = os.path.join(directory, 'ui_' + py_filename)
            print("Compiling: {0} -> {1}".format(infile, outfile))
            self._compile_ui(infile, outfile)

        # build qt resource files
        for infile in glob(os.path.join(self.base_path, 'resources', '*.qrc')):
            directory, rc_filename = os.path.split(infile)
            py_filename = ui_filename.replace('.qrc', '_rc.py')
            outfile = os.path.join('ui', py_filename)
            print("Compiling: {0} -> {1}".format(infile, outfile))
            self._build_rcc(infile, outfile)
