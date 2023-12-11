========================
Useless Benchmark of GCC
========================

Build and time binutils::

    $ FEATURES='-jobserver' ROOT=/tmp/temp_root ebuild "$(equery w sys-devel/binutils)" clean prepare
    $ time FEATURES='-jobserver' ROOT=/tmp/temp_root ebuild "$(equery w sys-devel/binutils)" compile

Size for binutils::

    $ FEATURES='-jobserver' ROOT=/tmp/temp_root ebuild "$(equery w sys-devel/binutils)" merge
    $ ROOT=/tmp/temp_root qsize -v sys-devel/binutils
    $ ROOT=/tmp/temp_root qsize -kv sys-devel/binutils

Build and time Python::

    $ FEATURES='-jobserver' ROOT=/tmp/temp_root ebuild "$(equery w dev-lang/python:3.11)" clean prepare
    $ time FEATURES='-jobserver' ROOT=/tmp/temp_root ebuild "$(equery w dev-lang/python:3.11)" compile

Size for Python::

    $ FEATURES='-jobserver' ROOT=/tmp/temp_root ebuild "$(equery w dev-lang/python:3.11)" merge
    $ ROOT=/tmp/temp_root qsize -v dev-lang/python
    $ ROOT=/tmp/temp_root qsize -kv dev-lang/python

Build and time kernel::

    $ rm -rf /tmp/temp_root/usr/src/linux*
    $ ROOT=/tmp/temp_root ebuild $(equery w sys-kernel/gentoo-sources:6.1.57) clean merge
    $ cd /tmp/temp_root/usr/src/linux-6.1.57-gentoo
    $ cp /tmp/.config .
    $ time make -j16

Sizes for kernel::

    /tmp/temp_root/usr/src/linux-6.1.57-gentoo/ $ du -d 0 -ach
    /tmp/temp_root/usr/src/linux-6.1.57-gentoo/ $ du -d 0 -ach -BK
    /tmp/temp_root/usr/src/linux-6.1.57-gentoo/ $ ls -alF vmlinux
    /tmp/temp_root/usr/src/linux-6.1.57-gentoo/ $ ls -ahlF vmlinux

Build and time GCC::

    $ FEATURES='-jobserver' ROOT=/tmp/temp_root USE='lto pgo' ebuild "$(equery w sys-devel/gcc)" clean prepare
    $ time FEATURES='-jobserver' ROOT=/tmp/temp_root USE='lto pgo' ebuild "$(equery w sys-devel/gcc)" compile

Size for GCC::

    $ FEATURES='-jobserver' ROOT=/tmp/temp_root USE='lto pgo' ebuild "$(equery w sys-devel/gcc)" merge
    $ ROOT=/tmp/temp_root qsize -v sys-devel/gcc
    $ ROOT=/tmp/temp_root qsize -kv sys-devel/gcc

.. NOTE::
   Binutils and Python both have ``lto`` and ``pgo`` USE flags enabled.


Using GCC without LTO or PGO
============================

Binutils
--------

Time to build::

    real    2m15.868s
    user    14m11.359s
    sys     2m15.588s

Size::

    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 28.9M
    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 29598 KiB


Python
------

Time to build::

    real    11m3.406s
    user    59m54.846s
    sys     5m42.692s

Size::

    dev-lang/python-3.11.6: 7209 files, 298 non-files, 177.0M
    dev-lang/python-3.11.6: 7209 files, 298 non-files, 181277 KiB


Kernel
------

Time to build::

    real    7m20.895s
    user    96m58.291s
    sys     14m5.288s

Size::

    2.1G        /tmp/temp_root/usr/src/linux-6.1.57-gentoo/
    2198064K    /tmp/temp_root/usr/src/linux-6.1.57-gentoo/
    -rwxr-xr-x. 1 oskari oskari 71427960 Dec  9 00:26 /tmp/temp_root/usr/src/linux-6.1.57-gentoo/vmlinux*
    -rwxr-xr-x. 1 oskari oskari 69M Dec  9 00:26 /tmp/temp_root/usr/src/linux-6.1.57-gentoo/vmlinux*


GCC
---

Time to build::

    real    36m35.221s
    user    321m30.955s
    sys     33m26.296s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 295.9M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 303005 KiB


GCC with LTO
------------

Time to build::

    real    64m11.967s
    user    728m19.839s
    sys     45m34.880s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 302.2M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 309404 KiB


GCC with PGO
------------

Time to build::

    real    57m14.651s
    user    501m28.004s
    sys     52m38.481s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 282.7M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 289477 KiB


GCC with LTO + PGO
------------------

Time to build::

    real    96m57.870s
    user    1132m17.418s
    sys     70m58.155s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 274.0M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 280601 KiB


Using GCC with LTO
==================

Binutils
--------

Time to build::

    real    2m13.873s
    user    13m52.968s
    sys     2m17.245s

Size::

    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 28.9M
    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 29598 KiB


Python
------

Time to build::

    real    10m32.894s
    user    54m48.605s
    sys     5m17.111s

Size::

    dev-lang/python-3.11.6: 7209 files, 298 non-files, 177.0M
    dev-lang/python-3.11.6: 7209 files, 298 non-files, 181269 KiB


Kernel
------

Time to build::

    real    6m49.982s
    user    89m10.503s
    sys     13m38.702s

Size::

    2.1G        /tmp/temp_root/usr/src/linux-6.1.57-gentoo/
    2198052K    /tmp/temp_root/usr/src/linux-6.1.57-gentoo/
    -rwxr-xr-x. 1 oskari oskari 71427808 Dec 10 15:04 /tmp/temp_root/usr/src/linux-6.1.57-gentoo/vmlinux*
    -rwxr-xr-x. 1 oskari oskari 69M Dec 10 15:04 /tmp/temp_root/usr/src/linux-6.1.57-gentoo/vmlinux*


GCC
---

Time to build::

    real    37m29.356s
    user    332m14.181s
    sys     34m12.848s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 295.9M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 303005 KiB


GCC with LTO
------------

Time to build::

    real    61m44.211s
    user    693m57.711s
    sys     43m58.570s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 302.2M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 309404 KiB


GCC with PGO
------------

Time to build::

    real    52m38.653s
    user    434m35.927s
    sys     47m30.270s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 282.7M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 289477 KiB


GCC with LTO + PGO
------------------

Time to build::

    real    93m58.675s
    user    1083m32.239s
    sys     69m26.225s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 274.0M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 280597 KiB


Using GCC with PGO
==================

Binutils
--------

Time to build::

    real    
    user    
    sys     

Size::



Python
------

Time to build::

    real    
    user    
    sys     

Size::



Kernel
------

Time to build::

    real    
    user    
    sys     

Size::



GCC
---

Time to build::

    real    
    user    
    sys     

Size::



GCC with LTO
------------

Time to build::

    real    
    user    
    sys     

Size::



GCC with PGO
------------

Time to build::

    real    
    user    
    sys     

Size::



GCC with LTO + PGO
------------------

Time to build::

    real    
    user    
    sys     

Size::



Using GCC with LTO and PGO
==========================

Binutils
--------

Time to build::

    real    
    user    
    sys     

Size::



Python
------

Time to build::

    real    
    user    
    sys     

Size::



Kernel
------

Time to build::

    real    
    user    
    sys     

Size::



GCC
---

Time to build::

    real    
    user    
    sys     

Size::



GCC with LTO
------------

Time to build::

    real    
    user    
    sys     

Size::



GCC with PGO
------------

Time to build::

    real    
    user    
    sys     

Size::



GCC with LTO + PGO
------------------

Time to build::

    real    
    user    
    sys     

Size::

