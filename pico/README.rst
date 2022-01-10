================================================
Getting Started with Raspberry Pi Pico on Gentoo
================================================

Although this document is tailored towards Gentoo, it's applicable to just about
any system on the face of the Earth (and beyond, gotta be future-proof) given a
proper amount of finger grease.


Requirements
============

#. Raspberry Pi Pico (duh)
#. Gentoo
#. ``sys-devel/crossdev``
#. ... a bit of luck


Sanity check
============

The simplest way to program the Pico is by mounting it in mass-storage mode and
dropping a binary into it. For our sanity check, let's just see if we can mount
it at all. Grab the Pico, hold down the BOOTSEL button, and plug it into your
USB port.

::
    
    # lsblk
    NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
    sda           8:0    1   128M  0 disk 
    `-sda1        8:1    1   128M  0 part 
    # mount /dev/sda1 /mnt
    # ls -alF /mnt
    total 24
    drwxr-xr-x. 2 root root 16384 Dec 31  1969 ./
    drwxr-xr-x. 1 root root   142 Feb 26  2021 ../
    -r-xr-xr-x. 1 root root   241 Sep  5  2008 INDEX.HTM*
    -r-xr-xr-x. 1 root root    62 Sep  5  2008 INFO_UF2.TXT*

Success! Although it is strange that it shows up as a 128 MiB disk even though
it only has 2 MiB of flash according to the specs... Should be fine since the
contents are as expected.


Creating the toolchain
======================

The Pico uses an RP2040 which is an Arm Cortex-M0+ microcontroller. This means
we'll need a toolchain which supports the Armv6-M instruction set. We could just
snag a prebuilt one directly from Arm, but that's no fun. Besides, we're using
Gentoo so we'll do it ourselves! With the help of ``crossdev`` because fuck
creating a cross-compiler from scratch. I've done that before, and there's just
too many points of failure. Plus, it's less maintainable.


Creating an overlay
-------------------

**Note:** Going into detail on how Portage's repos work is beyond the scope of
this document. I might drop a link in resources_ if I remember.

The basic structure we need to create::
    
    /
    +- etc/
    |  +- portage/
    |     +- repos.conf/
    |        +- cross-armv-none-eabi.conf
    +- var/
       +- db/
          +- repos/
             +- cross-arm-none-eabi/
                +- metadata/
                |  +- layout.conf
                +- profiles/
                   +- repo_name

Then we need to fill the files with the necessary information.

``/etc/portage/repos.conf/cross-arm-none-eabi.conf``::
    
    [cross-arm-none-eabi]
    location = /var/db/repos/cross-arm-none-eabi
    priority = 10
    masters = gentoo
    auto-sync = no

``/var/db/repos/cross-arm-none-eabi/metadata/layout.conf``::
    
    masters = gentoo

``/var/db/repos/cross-arm-none-eabi/profiles/repo_name``::
    
    cross-arm-none-eabi

We still need to transfer ownership of the repo to Portage's user so our system
doesn't get mad when we actually get to building our shit::
    
    # chown -R portage:portage /var/db/repos/cross-arm-none-eabi

Now we just initialize everything...

::
    
    # crossdev  --target arm-none-eabi  \
                --init-target              

... and then fix some things. Let's start by linking the repo's temp directory
to ``/var/tmp``::
    
    # ln -s /var/tmp /usr/arm-none-eabi/tmp

We should also fix ``/usr/arm-none-eabi/etc/portage/make.conf`` to include the
following::
    
    CFLAGS="-O2 -pipe -fomit-frame-pointer -march=armv6-m -mtune=cortex-m0plus -mthumb"
    MAKEOPTS="-j16"
    FEATURES="-collision-protect candy ipc-sandbox network-sandbox noman noinfo nodoc parallel-fetch parallel-install preserve-libs sandbox userfetch userpriv usersandbox usersync"

The GCC architecture options were found by perusing the trusty `GCC docs`_. An
option that's worth pointing out is ``-mthumb``. The Cortex-M0+ only supports
Thumb mode. This options tells GCC to only spit out code using the Thumb
instruction set. Set ``-jN`` to a suitable value for your system. I have a
Ryzen 7 with 8c/16t. See `make.conf(5)`_ for a description of the ``FEATURES``.

Two other files to fix are ``/usr/arm-none-eabi/etc/portage/profile/make.defaults``
and ``/usr/arm-none-eabi/etc/portage/profile/use.force``. They contain obnoxious
kernel placeholders which break the build and which we need to remove.
``make.defaults`` should look something like this::
    
    ARCH="arm"
    KERNEL="-linux"
    ELIBC="newlib"

and ``use.force`` should look something like this::
    
    -kernel_linux


Building our shit
-----------------

The time has come. Let's create the toolchain. Thanks to the setup we did
above, it's as easy as::
    
    # crossdev  --target arm-none-eabi  \
                --stage4                \
                --portage -a --portage -v

Not a single ``./configure && make && make install`` was punched in. And Portage
will handle updating the toolchain automatically, wowza!

If you don't think you're up for doing all this by hand, then I've written up `a
script`_ which Works On My Machine (TM) and handles all of the heavy lifting. In
fact, I didn't write a single one of those commands into my Bash prompt -- just
tweaked the script as I went along.

Ok, ``crossdev`` does the heavy lifting...

Resources
=========

#. `Getting Started with Raspberry Pi Pico`_
#. `Raspberry Pi Pico C/C++ SDK`_
#. `Arm Cortex-M0+`_
#. `crossdev`_
#. `Portage repositories`_

.. _GCC docs:
    https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html

.. _make.conf(5):
    https://dev.gentoo.org/~zmedico/portage/doc/man/make.conf.5.html

.. _Getting Started with Raspberry Pi Pico:
    https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf

.. _Raspberry Pi Pico C/C++ SDK:
    https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-c-sdk.pdf

.. _Arm Cortex-M0+:
    https://developer.arm.com/ip-products/processors/cortex-m/cortex-m0-plus

.. _crossdev:
    https://wiki.gentoo.org/wiki/Crossdev

.. _Portage repositories:
    https://wiki.gentoo.org/wiki/Repository_format
