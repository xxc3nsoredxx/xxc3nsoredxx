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
    
    ARCH="arm"
    CFLAGS="-O2 -pipe -fomit-frame-pointer -march=armv6-m -mtune=cortex-m0plus -mthumb"
    MAKEOPTS="-j16"
    FEATURES="-collision-protect candy ipc-sandbox network-sandbox noman noinfo nodoc parallel-fetch parallel-install preserve-libs sandbox userfetch userpriv usersandbox usersync"

The GCC architecture options were found by perusing the trusty `GCC docs`_. An
option that's worth pointing out is ``-mthumb``. The Cortex-M0+ only supports
Thumb mode. This options tells GCC to only spit out code using the Thumb
instruction set. Set ``-jN`` to a suitable value for your system. I have a
Ryzen 7 with 8c/16t. See `make.conf(5)`_ for a description of the ``FEATURES``.


Building our shit
-----------------

The time has come. Let's create the toolchain. Thanks to the setup we did
above, it's as easy as::
    
    # crossdev  --target arm-none-eabi  \
                --stage3                \
                --portage -a --portage -v

Not a single ``./configure && make && make install`` was punched in, wowza!



If you don't think you're up for doing all this by hand, then I've written up `a
script`_ which Works On My Machine (TM) and handles all of the heavy lifting. In
fact, I didn't write a single one of those commands into my Bash prompt -- just
tweaked the script as I went along.

Ok, ``crossdev`` does the heavy lifting...

Resources
=========

#. `Getting Started with Raspberry Pi Pico`_
#. `crossdev`_
#. `Portage repositories`_

.. _Getting Started with Raspberry Pi Pico:
   https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf
