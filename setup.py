#!/usr/bin/env python
'''
setup.py

Installation script for python-llfuse.

Copyright (C) Nikolaus Rath <Nikolaus@rath.org>

This file is part of python-llfuse (http://python-llfuse.googlecode.com).
python-llfuse can be distributed under the terms of the GNU LGPL.
'''

from __future__ import division, print_function, absolute_import

import sys
import os
import subprocess

# Import distribute
basedir = os.path.abspath(os.path.dirname(sys.argv[0]))
sys.path.insert(0, os.path.join(basedir, 'src'))
from distribute_setup import use_setuptools
use_setuptools(version='0.6.2', download_delay=5)
import setuptools
import setuptools.command.test as setuptools_test
from setuptools import Extension

def main():
    
    with open(os.path.join(basedir, 'README.txt'), 'r') as fh:
        long_desc = fh.read()

    compile_args = [ '-Werror' ]
    fuse_compile_args = pkg_config('fuse', cflags=True, ldflags=False, min_ver='2.8.0')
    fuse_compile_args.append('-DFUSE_USE_VERSION=28')
    fuse_link_args = pkg_config('fuse', cflags=False, ldflags=True, min_ver='2.8.0')

    setuptools.setup(
          name='llfuse',
          zip_safe=True,
          version='0.9.1',
          description='Python bindings for the low-level FUSE API',
          long_description=long_desc,
          author='Nikolaus Rath',
          author_email='Nikolaus@rath.org',
          url='http://python-llfuse.googlecode.com/',
          download_url='http://code.google.com/p/python-llfuse/downloads/list',
          license='LGPL',
          classifiers=['Development Status :: 4 - Beta',
                       'Intended Audience :: Developers',
                       'Programming Language :: Python',
                       'Topic :: Software Development :: Libraries :: Python Modules',
                       'Topic :: System :: Filesystems',
                       'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                       'Operating System :: POSIX' ],
          platforms=[ 'POSIX', 'UNIX', 'Linux' ],
          keywords=['FUSE', 'python' ],
          package_dir={'': 'src'},
          packages=setuptools.find_packages('src'),
          provides=['llfuse'],
          ext_modules=[ Extension('llfuse.lock', ['src/llfuse/lock.c'],
                                  extra_compile_args=compile_args), 
                        Extension('llfuse.util', ['src/llfuse/util.c'], 
                                  extra_compile_args=compile_args), 
                        Extension('llfuse.main', ['src/llfuse/main.c'], 
                                  extra_compile_args=compile_args + fuse_compile_args,
                                  extra_link_args=fuse_link_args)],
          cmdclass={'build_cython': build_cython,
                    'upload_docs': upload_docs }
         )


def pkg_config(pkg, cflags=True, ldflags=False, min_ver=None):
    '''Frontend to ``pkg-config``'''

    if min_ver:
        cmd = ['pkg-config', pkg, '--atleast-version', min_ver ]
        
        if subprocess.call(cmd) != 0:
            cmd = ['pkg-config', '--modversion', pkg ]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            version = proc.communicate()[0].strip()
            raise SystemExit('%s version too old (found: %s, required: %s)' 
                             % (pkg, version, min_ver), file=sys.stderr)
    
    cmd = ['pkg-config', pkg ]
    if cflags:
        cmd.append('--cflags')
    if ldflags:
        cmd.append('--libs')

    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    cflags = proc.stdout.readline().rstrip()
    proc.stdout.close()
    if proc.wait() != 0:
        raise SystemExit('Failed to execute pkg-config. Exit code: %d.\n'
                         'Check that the %s development package been installed properly.'
                         % (proc.returncode, pkg), file=sys.stderr)

    return cflags.decode('us-ascii').split()

        
class build_cython(setuptools.Command):
    user_options = []
    boolean_options = []
    description = "Compile .pyx to .c"

    def initialize_options(self):
        pass

    def finalize_options(self):
        self.extensions = self.distribution.ext_modules

    def run(self):
        try:
            from Cython.Compiler.Main import compile
        except ImportError:
            raise SystemExit('Cython needs to be installed for this command')

        # TODO: Turn on timestamps once Cython supports them
        options = { 'include_path': [ os.path.join(basedir, 'Include') ],
                    'recursive': False, 'verbose': True,
                    'timestamps': False }
        
        for extension in self.extensions:
            for file in extension.sources:
                (file, ext) = os.path.splitext(file)
                path = os.path.join(basedir, file)
                if ext != '.c':
                    continue 
                if os.path.exists(path + '.pyx'):
                    print('compiling %s to %s' % (file + '.pyx', file + ext))
                    res = compile(path + '.pyx', full_module_name=extension.name,
                                  **options)
                    if res.num_errors != 0:
                        raise SystemExit('Cython encountered errors.')
                else:
                    print('%s is up to date' % (file + ext,))

        
class upload_docs(setuptools.Command):
    user_options = []
    boolean_options = []
    description = "Upload documentation"

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        subprocess.check_call(['rsync', '-aHv', '--del', os.path.join(basedir, 'doc', 'html') + '/',
                               'ebox.rath.org:/var/www/llfuse-docs/'])

if __name__ == '__main__':
    main()