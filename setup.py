#!/usr/bin/env python
# encoding: utf-8
from __future__ import print_function
from distutils.core import setup
from utils.buildqt import BuildQt

cmdclass = {}
BuildQt.base_path = 'src'
cmdclass['build_qt'] = BuildQt

setup(
    name='TabooWords',
    description='',
    version='0.1.0',
    cmdclass=cmdclass,
)
