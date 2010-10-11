'''
fuse_common.pxd

This file contains Cython definitions for fuse_common.h

Copyright (C) Nikolaus Rath <Nikolaus@rath.org>

This file is part of python-llfuse (http://python-llfuse.googlecode.com).
python-llfuse can be distributed under the terms of the GNU LGPL.
'''

from fuse_opt cimport *

# Based on fuse sources, revision tag fuse_2_8_3
cdef extern from * nogil: # fuse_common.h should not be included
    struct fuse_file_info:
        pass

    struct fuse_conn_info:
        pass

    struct fuse_session:
        pass

    struct fuse_chan:
       pass


    fuse_chan *fuse_mount(char *mountpoint, fuse_args *args)
    void fuse_unmount(char *mountpoint, fuse_chan *ch)
    int fuse_set_signal_handlers(fuse_session *se)
    void fuse_remove_signal_handlers(fuse_session *se)

