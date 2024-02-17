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

+-----------------+----------------------------------------+---------------------+
|                 | Build Time                             | Size                |
|                 +------------+--------------+------------+--------+------------+
| Build Target    | Real       | User         | Sys        | Human  | KiB / Raw  |
+=================+============+==============+============+========+============+
| Binutils        | 2m15.868s  | 14m11.359s   | 2m15.588s  | 28.9M  | 29598 KiB  |
+-----------------+------------+--------------+------------+--------+------------+
| Python          | 11m3.406s  | 59m54.846s   | 5m42.692s  | 177.0M | 181277 KiB |
+-----------------+------------+--------------+------------+--------+------------+
| Kernel          | 7m20.895s  | 96m58.291s   | 14m5.288s  | 69M    | 71427960   |
+-----+-----------+------------+--------------+------------+--------+------------+
|     | Plain     | 36m35.221s | 321m30.955s  | 33m26.296s | 295.9M | 303005 KiB |
|     +-----------+------------+--------------+------------+--------+------------+
|     | LTO       | 64m11.967s | 728m19.839s  | 45m34.880s | 302.2M | 309404 KiB |
| GCC +-----------+------------+--------------+------------+--------+------------+
|     | PGO       | 57m14.651s | 501m28.004s  | 52m38.481s | 282.7M | 289477 KiB |
|     +-----------+------------+--------------+------------+--------+------------+
|     | LTO + PGO | 96m57.870s | 1132m17.418s | 70m58.155s | 274.0M | 280601 KiB |
+-----+-----------+------------+--------------+------------+--------+------------+


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

    real    2m5.087s
    user    12m43.125s
    sys     2m12.778s

Size::

    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 28.9M
    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 29598 KiB


Python
------

Time to build::

    real    10m3.910s
    user    52m48.963s
    sys     5m9.485s

Size::

    dev-lang/python-3.11.6: 7209 files, 298 non-files, 177.0M
    dev-lang/python-3.11.6: 7209 files, 298 non-files, 181273 KiB


Kernel
------

Time to build::

    real    6m7.167s
    user    78m11.686s
    sys     13m9.938s

Size::

    -rwxr-xr-x. 1 oskari oskari 71450488 Dec 11 20:50 /tmp/temp_root/usr/src/linux-6.1.57-gentoo/vmlinux*
    -rwxr-xr-x. 1 oskari oskari 69M Dec 11 20:50 /tmp/temp_root/usr/src/linux-6.1.57-gentoo/vmlinux*


GCC
---

Time to build::

    real    35m24.509s
    user    307m14.042s
    sys     32m34.184s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 295.9M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 303005 KiB


GCC with LTO
------------

Time to build::

    real    59m15.142s
    user    659m9.472s
    sys     42m17.251s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 302.2M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 309404 KiB


GCC with PGO
------------

Time to build::

    real    51m3.463s
    user    417m20.812s
    sys     46m5.245s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 282.7M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 289477 KiB


GCC with LTO + PGO
------------------

Time to build::

    real    94m34.405s
    user    1086m57.790s
    sys     69m38.408s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 274.0M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 280577 KiB


Using GCC with LTO and PGO
==========================

Binutils
--------

Time to build::

    real    2m1.622s
    user    12m20.410s
    sys     2m11.943s

Size::

    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 28.9M
    sys-devel/binutils-2.40-r9: 414 files (413 unique), 92 non-files, 29598 KiB


Python
------

Time to build::

    real    9m55.507s
    user    52m40.004s
    sys     5m9.618s

Size::

    dev-lang/python-3.11.6: 7209 files, 298 non-files, 177.0M
    dev-lang/python-3.11.6: 7209 files, 298 non-files, 181277 KiB


Kernel
------

Time to build::

    real    6m1.686s
    user    76m34.250s
    sys     13m21.193s

Size::

    -rwxr-xr-x. 1 oskari oskari 71427992 Dec 13 20:20 /tmp/temp_root/usr/src/linux-6.1.57-gentoo/vmlinux*
    -rwxr-xr-x. 1 oskari oskari 69M Dec 13 20:20 /tmp/temp_root/usr/src/linux-6.1.57-gentoo/vmlinux*


GCC
---

Time to build::

    real    35m2.993s
    user    303m17.121s
    sys     32m20.105s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 295.9M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 303005 KiB


GCC with LTO
------------

Time to build::

    real    57m50.423s
    user    636m51.775s
    sys     41m26.439s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 302.2M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 309404 KiB


GCC with PGO
------------

Time to build::

    real    51m35.849s
    user    423m58.028s
    sys     46m29.406s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 282.7M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 289477 KiB


GCC with LTO + PGO
------------------

Time to build::

    real    88m3.736s
    user    1002m56.349s
    sys     65m5.550s

Size::

    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 274.0M
    sys-devel/gcc-13.2.1_p20230826: 1729 files (1725 unique), 152 non-files, 280593 KiB
