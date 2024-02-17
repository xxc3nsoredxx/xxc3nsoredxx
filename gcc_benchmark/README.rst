========================
Useless Benchmark of GCC
========================

This is a Highly Scientific (TM) benchmark of GCC, comparing "plain" GCC, GCC
built with LTO, GCC built with PGO, and GCC built with both LTO and PGO. These
are the steps I took, repeated for each "version" of GCC:

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
   Binutils and Python both have ``lto`` and ``pgo`` USE flags enabled in order
   to have them be built with LTO and PGO. Although, these flags seem to be
   disappearing from the packages and will need to be enabled in ``CFLAGS`` in
   the future (curse you for making me change my workflow).


The data
========

Here's my Highly Scientific (TM) data. Feast your eyes upon the tables.


.. _the first table:

Using GCC without LTO or PGO
----------------------------

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


.. _the second table:

Using GCC with LTO
------------------

+-----------------+----------------------------------------+---------------------+
|                 | Build Time                             | Size                |
|                 +------------+--------------+------------+--------+------------+
| Build Target    | Real       | User         | Sys        | Human  | KiB / Raw  |
+=================+============+==============+============+========+============+
| Binutils        | 2m13.873s  | 13m52.968s   | 2m17.245s  | 28.9M  | 29598 KiB  |
+-----------------+------------+--------------+------------+--------+------------+
| Python          | 10m32.894s | 54m48.605s   | 5m17.111s  | 177.0M | 181269 KiB |
+-----------------+------------+--------------+------------+--------+------------+
| Kernel          | 6m49.982s  | 89m10.503s   | 13m38.702s | 69M    | 71427808   |
+-----+-----------+------------+--------------+------------+--------+------------+
|     | Plain     | 37m29.356s | 332m14.181s  | 34m12.848s | 295.9M | 303005 KiB |
|     +-----------+------------+--------------+------------+--------+------------+
|     | LTO       | 61m44.211s | 693m57.711s  | 43m58.570s | 302.2M | 309404 KiB |
| GCC +-----------+------------+--------------+------------+--------+------------+
|     | PGO       | 52m38.653s | 434m35.927s  | 47m30.270s | 282.7M | 289477 KiB |
|     +-----------+------------+--------------+------------+--------+------------+
|     | LTO + PGO | 93m58.675s | 1083m32.239s | 69m26.225s | 274.0M | 280597 KiB |
+-----+-----------+------------+--------------+------------+--------+------------+


.. _the third table:

Using GCC with PGO
------------------

+-----------------+----------------------------------------+---------------------+
|                 | Build Time                             | Size                |
|                 +------------+--------------+------------+--------+------------+
| Build Target    | Real       | User         | Sys        | Human  | KiB / Raw  |
+=================+============+==============+============+========+============+
| Binutils        | 2m5.087s   | 12m43.125s   | 2m12.778s  | 28.9M  | 29598 KiB  |
+-----------------+------------+--------------+------------+--------+------------+
| Python          | 10m3.910s  | 52m48.963s   | 5m9.485s   | 177.0M | 181273 KiB |
+-----------------+------------+--------------+------------+--------+------------+
| Kernel          | 6m7.167s   | 78m11.686s   | 13m9.938s  | 69M    | 71450488   |
+-----+-----------+------------+--------------+------------+--------+------------+
|     | Plain     | 35m24.509s | 307m14.042s  | 32m34.184s | 295.9M | 303005 KiB |
|     +-----------+------------+--------------+------------+--------+------------+
|     | LTO       | 59m15.142s | 659m9.472s   | 42m17.251s | 302.2M | 309404 KiB |
| GCC +-----------+------------+--------------+------------+--------+------------+
|     | PGO       | 51m3.463s  | 417m20.812s  | 46m5.245s  | 282.7M | 289477 KiB |
|     +-----------+------------+--------------+------------+--------+------------+
|     | LTO + PGO | 94m34.405s | 1086m57.790s | 69m38.408s | 274.0M | 280577 KiB |
+-----+-----------+------------+--------------+------------+--------+------------+


.. _the fourth table:

Using GCC with LTO and PGO
--------------------------

+-----------------+----------------------------------------+---------------------+
|                 | Build Time                             | Size                |
|                 +------------+--------------+------------+--------+------------+
| Build Target    | Real       | User         | Sys        | Human  | KiB / Raw  |
+=================+============+==============+============+========+============+
| Binutils        | 2m1.622s   | 12m20.410s   | 2m11.943s  | 28.9M  | 29598 KiB  |
+-----------------+------------+--------------+------------+--------+------------+
| Python          | 9m55.507s  | 52m40.004s   | 5m9.618s   | 177.0M | 181277 KiB |
+-----------------+------------+--------------+------------+--------+------------+
| Kernel          | 6m1.686s   | 76m34.250s   | 13m21.193s | 69M    | 71427992   |
+-----+-----------+------------+--------------+------------+--------+------------+
|     | Plain     | 35m2.993s  | 303m17.121s  | 32m20.105s | 295.9M | 303005 KiB |
|     +-----------+------------+--------------+------------+--------+------------+
|     | LTO       | 57m50.423s | 636m51.775s  | 41m26.439s | 302.2M | 309404 KiB |
| GCC +-----------+------------+--------------+------------+--------+------------+
|     | PGO       | 51m35.849s | 423m58.028s  | 46m29.406s | 282.7M | 289477 KiB |
|     +-----------+------------+--------------+------------+--------+------------+
|     | LTO + PGO | 88m3.736s  | 1002m56.349s | 65m5.550s  | 274.0M | 280593 KiB |
+-----+-----------+------------+--------------+------------+--------+------------+


That thing where you analyze
============================

No good scientific work is complete without this section. So here's my Highly
Scientific (TM) analysis.

`The first table`_ is just the baseline stats. It's using a boring/plain GCC.
This doesn't mean it's devoid of anything interesting. On the contrary, here
are some things which surprised me:

- Building GCC with LTO took longer than building it with PGO.
- GCC with LTO had the largest size. I expected it to be smaller than the plain
  GCC. Whereas PGO was smaller than plain, and LTO + PGO was the smallest!

`The second table`_, using an LTO'd GCC, hopefully sets a trend for the future
runs, although I'm not sure if all of these are real differences vs just how
things happen to get scheduled:

- Binutils built about 2s faster, with the "user" time being about 20s less.
- Python built about 30s faster, with the "user" time being about 5min less.
- The kernel also built about 30s faster, but here the "user" time was about
  8min less.
- Interestingly, the plain GCC took longer here by about 1min for both "real"
  and "user" time.

  - GCC with LTO was about 2min 30s faster, with "user" time being about 35min
    less.
  - GCC with PGO was about 5min faster, "user" time was almost 70min less.
  - GCC with both was only about 3min faster, "user" time about 50min less.

`The third table`_, with a PGO'd GCC, should hopefully be even better.
Otherwise my life has been a lie:

- Binutils was about 9s faster than LTO, and "user" time was about 1min 10s
  less.
- Python was almost 30s faster, and "user" time was about 2min less.
- The kernel built about 43s faster, and "user" time was about 11min less.
- Finally GCC was also faster

  - Plain GCC was about 2min faster, and "user" time was about 25min less.
  - GCC with LTO was about 2min 30s faster, "user" time about 45min less.
  - GCC with PGO was about 1min 30s faster, "user" time about 17min less.
  - Except GCC with LTO and PGO was slower now. About 30s slower, and "user"
    time was about 3min 20s more.

Last, and hopefully least, we have `the fourth table`_ with and LTO'd and PGO'd
GCC:

- Binutils was about 4s faster than PGO, and "user" time about 23s less.
- Python took like 8s less, for both "real" and "user" times.
- The kernel was like 5s faster, and "user" time was like 1min 40s less.
- Finally GCC was also faster (for real this time?)

  - Plain GCC built like 21s faster and "user" time was like 4min less.
  - GCC with LTO took 1min 25s less and "user" time was like 22min less.
  - Dammit, GCC with PGO took like 32s more and "user" time was like 6min 30s
    higher.
  - GCC with LTO and PGO was faster by like 6min 30s and "user" time was like
    84min less.


Build time differences
----------------------

In case you don't want to read all that, then here's a nice table summarizing
the above in order to see the difference between using plain GCC and GCC with
both LTO and PGO. You just have to trust me that I got my mental time math
correct (I know I don't trust me). They're also just approximates. I've left
out the "sys" time since it's not as interesting (time spent in "system mode"
according to one of my favorite man pages -- ``bash(1)``).

+-----------------+-------------------------+
|                 | Build Time              |
|                 +-----------+-------------+
| Build Target    | Real      | User        |
+=================+===========+=============+
| Binutils        | -15s      | -1min 53s   |
+-----------------+-----------+-------------+
| Python          | -1min 8s  | -7min 8s    |
+-----------------+-----------+-------------+
| Kernel          | -1min 18s | -20min 40s  |
+-----+-----------+-----------+-------------+
|     | Plain     | -1min 21s | -28min      |
|     +-----------+-----------+-------------+
|     | LTO       | -6min 25s | -102min     |
| GCC +-----------+-----------+-------------+
|     | PGO       | -5min 58s | -80min 30s  |
|     +-----------+-----------+-------------+
|     | LTO + PGO | -9min     | -130min 40s |
+-----+-----------+-----------+-------------+


Final remarks
-------------

Now, the whole point of this was to see if it makes sense to build GCC with LTO
and PGO enabled:

- Plain GCC building itself: ~37 minutes
- GCC with LTO and PGO building itself: ~88 minutes

Is the extra ~51 minutes for GCC worth it? According to my Highly Scientific
(TM) extrapolation of the data, as long as you build a few hundred packages
between each GCC update then it is. Of course, there might be packages that see
slightly bigger speedups, which brings that number down.

Machine specs matter too. Lower end machines will take longer to LTO + PGO GCC.
These tests were run on my Thinkpad T14 (gen 1) with Ryzen 7 PRO 4750U and 32
GiB of RAM. So, for me, I think it's worth it.
