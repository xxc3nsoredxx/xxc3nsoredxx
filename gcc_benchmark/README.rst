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



Using GCC with LTO
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

