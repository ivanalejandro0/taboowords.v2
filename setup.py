#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
from distutils.core import setup, Command

cmdclass = {}


# thanks to: https://github.com/glue-viz/glue/pull/22
class BuildQt(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os
        import glob
        from pysideuic import compileUi

        for infile in glob.glob(os.path.join('ui', '*.ui')):
            directory, ui_filename = os.path.split(infile)
            py_filename = ui_filename.replace('.ui', '.py')
            outfile = os.path.join(directory, 'ui_' + py_filename)
            print("Compiling: %s -> %s" % (infile, outfile))
            compileUi(infile, open(outfile, 'wb'))


cmdclass['build_qt'] = BuildQt

setup(
    name='TabooWords',
    description='',
    version='0.1.0',
    cmdclass=cmdclass,
)
