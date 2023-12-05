========================
Useless Benchmark of GCC
========================

Build binutils::

    $ FEATURES='-jobserver' ROOT=/tmp/temp_root emerge -1O -j1 sys-devel/binutils

``-O`` means ``--nodeps``.

Time for binutils::

    $ qlop -vH sys-devel/binutils

Size for binutils::

    $ ROOT=/tmp/temp_root qsize -v sys-devel/binutils
    $ ROOT=/tmp/temp_root qsize -kv sys-devel/binutils

Build Python::

    $ FEATURES='-jobserver' ROOT=/tmp/temp_root emerge -1O -j1 python:3.11

Time for Python::

    $ qlop -vH python-3.11.6

Size for Python::

    $ ROOT=/tmp/temp_root qsize -v python
    $ ROOT=/tmp/temp_root qsize -kv python

Build (and time) kernel::

    $ ROOT=/tmp/temp_root ebuild $(equery w gentoo-sources:6.1.57) clean install
    $ cd /var/tmp/.../src/linux/linux-6.1.57-gentoo
    $ cp /tmp/.config .
    $ time make -j16

Sizes for kernel::

    /var/tmp/.../src/linux-6.1.57-gentoo/ $ du -d 0 -ach
    /var/tmp/.../src/linux-6.1.57-gentoo/ $ du -d 0 -ach -BK
    /var/tmp/.../src/linux-6.1.57-gentoo/ $ ls -alF vmlinux
    /var/tmp/.../src/linux-6.1.57-gentoo/ $ ls -ahlF vmlinux

Build GCC (intermediate steps)::

    $ FEATURES='-jobserver' ROOT=/tmp/temp_root USE='lto pgo' emerge -1O -j1 sys-devel/gcc

Time for GCC (intermediate steps)::

    $ qlop -vH sys-devel/gcc

Size for GCC (intermediate steps)::

    $ ROOT=/tmp/temp_root qsize -v gcc
    $ ROOT=/tmp/temp_root qsize -kv gcc

Build GCC (non-intermediate)::

    # FEATURES='-jobserver' USE='lto pgo' emerge -1 -j1 sys-devel/gcc

Time for GCC (non-intermediate)::

    $ qlop -vH sys-devel/gcc

Size for GCC (non-intermediate)::

    $ qsize -v gcc
    $ qsize -kv gcc

.. NOTE::
   Binutils and Python both have ``lto`` and ``pgo`` USE flags enabled.


Using GCC without LTO or PGO
============================

Binutils
--------

Time to build::

    2023-12-03T15:11:05 >>> sys-devel/binutils-2.40-r9: 2 minutes, 37 seconds

Size::

    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 28.9M 
    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 29598 KiB


Python
------

Time to build::

    2023-12-03T15:25:47 >>> dev-lang/python-3.11.6: 12 minutes, 57 seconds

Size::

    dev-lang/python-3.11.6: 7209 files, 298 non-files, 177.0M 
    dev-lang/python-3.11.6: 7209 files, 298 non-files, 181261 KiB


Kernel
------

Time to build::

    real    6m48.553s
    user    89m16.004s
    sys     13m7.479s

Size::

    2.1G    total
    2198160K    total
    -rwxr-xr-x. 1 oskari oskari 71426752 Dec  3 15:52 /var/tmp/portage/sys-kernel/gentoo-sources-6.1.57/image/usr/src/linux-6.1.57-gentoo/vmlinux*
    -rwxr-xr-x. 1 oskari oskari 69M Dec  3 15:52 /var/tmp/portage/sys-kernel/gentoo-sources-6.1.57/image/usr/src/linux-6.1.57-gentoo/vmlinux*


GCC
---

Time to build::

    2023-12-03T16:11:00 >>> sys-devel/gcc-13.2.1_p20230826: 38 minutes, 39 seconds

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 295.9M 
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 303005 KiB


GCC with PGO
------------

Time to build::

    2023-12-03T16:52:56 >>> sys-devel/gcc-13.2.1_p20230826: 59 minutes, 29 seconds

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 282.7M 
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 289477 KiB


GCC with LTO + PGO
------------------

Time to build::

    2023-12-03T18:03:09 >>> sys-devel/gcc-13.2.1_p20230826: 1 hour, 41 minutes, 44 seconds

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 274.0M 
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 280593 KiB


GCC with LTO
------------

Time to build::

    2023-12-03T19:52:43 >>> sys-devel/gcc-13.2.1_p20230826: 1 hour, 7 minutes, 29 seconds

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 302.2M 
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 309404 KiB


Using GCC with LTO
==================

Binutils
--------

Time to build::

    2023-12-03T23:01:00 >>> sys-devel/binutils-2.40-r9: 2 minutes, 37 seconds

Size::

    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 28.9M 
    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 29598 KiB


Python
------

Time to build::

    2023-12-03T23:13:57 >>> dev-lang/python-3.11.6: 11 minutes, 35 seconds

Size::

    dev-lang/python-3.11.6: 7209 files, 298 non-files, 177.0M 
    dev-lang/python-3.11.6: 7209 files, 298 non-files, 181277 KiB


Kernel
------

Time to build::

    real    6m51.348s
    user    89m26.257s
    sys     13m37.117s

Size::

    2.1G    total
    2198084K    total
    -rwxr-xr-x. 1 oskari oskari 71427448 Dec  3 23:43 /var/tmp/portage/sys-kernel/gentoo-sources-6.1.57/image/usr/src/linux-6.1.57-gentoo/vmlinux*
    -rwxr-xr-x. 1 oskari oskari 69M Dec  3 23:43 /var/tmp/portage/sys-kernel/gentoo-sources-6.1.57/image/usr/src/linux-6.1.57-gentoo/vmlinux*


GCC
---

Time to build::

    2023-12-03T23:50:20 >>> sys-devel/gcc-13.2.1_p20230826: 39 minutes, 46 seconds

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 295.9M 
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 303005 KiB


GCC with LTO
------------

Time to build::


Size::



GCC with LTO + PGO
------------------

Time to build::


Size::



GCC with PGO
------------

Time to build::


Size::

