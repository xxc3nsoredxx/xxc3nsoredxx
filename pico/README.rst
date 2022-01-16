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
#. ``>sys-devel/crossdev-20211121``

   - Versions ``20211121`` and earlier may require `this patch`_. See `#831165`_
     for more details.

#. ``app-eselect/eselect-repository``
#. ``net-dialup/minicom``
#. USB UART (3.3V)
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


Installing the SDK
==================

The next step is to install the Pico SDK. The official guide has you clone the
repo. But I've written an ebuild to install the SDK onto the system. So let's
use that instead, shall we?


Adding my overlay
-----------------

The ebuild is hosted in the unc3nsored_ overlay. If it's not already added (and
let's be real, who'd've added it up until this point), do the following to add
and sync the ebuilds::
    
    # eselect repository enable unc3nsored
    # emaint sync -r unc3nsored


Installing the SDK (for real this time)
---------------------------------------

With the overlay added, installation is as simple as adding the package into
your ``package.accept_keywords/`` and running::
    
    # emerge --ask dev-libs/pico-sdk

Like with ``crossdev``, this has the nice benefit of Portage handling keeping
things up to date. Although now the burden is on me to tell Portage when an
update exists...


Setting up for serial I/O
=========================

Because serial I/O is cool as *heck*.


Hardware prep
-------------

The Pico's default pins are:

- Pin 1 - UART0 TX (top left)
- Pin 2 - UART0 RX
- Pin 3 - GND

This means that the TX pin on the USB UART should connect to Pin 2 on the Pico,
the RX pin to Pin 1, and the ground pin to Pin 3. Soldering the headers onto the
Pico and placing it onto a breadboard may make this easier.


Local machine prep
------------------

(At least) the following kernel options need to be set. Depending your UART
device, you may need to set additional options.

- ``CONFIG_USB_SERIAL``
- ``CONFIG_USB_SERIAL_CONSOLE``
- ``CONFIG_USB_SERIAL_GENERIC``
- ``CONFIG_USB_SERIAL_SIMPLE``

::
    
    Device Drivers  --->
       [*] USB support  --->
          <M>   USB Serial Converter support  --->
             --- USB Serial Converter support
             [*]   USB Serial Console device support
             [*]   USB Generic Serial Driver
             <M>   USB Serial Simple Driver

Unless you always want to run as root, your user needs to be in the ``dialout``
group to access the serial lines::
    
    # usermod -aG dialout user

If you had to rebuild your kernel, reboot. If you only had to add your user to
``dialout``, log out and log back in for it to take effect.


Code examples
=============

Now that all of that is out of the way, we can mostly follow the official
guide from here on out. There are still a few important deviations, but those
will be pointed out where appropriate. This section assumes you're in the
``examples/`` directory (or local equivalent).


Setting up the build environment
--------------------------------

The upstream repo contains the following towards the top of the project root
``CMakeLists.txt``:

.. code:: CMake

    # Pull in SDK (must be before project)
    include(pico_sdk_import.cmake)

This assumes that the upstream repo has been cloned into the project root or
that ``PICO_SDK_PATH`` has been defined as an environment variable. Since we
installed the SDK system-wide, this has been changed to:

.. code:: CMake

    # Pull in SDK (must be before project)
    find_package(pico-sdk CONFIG)

Now we can create the build environment::
    
    $ mkdir build
    $ cd build
    $ cmake ..

The benefits of an out-of-tree build are that it doesn't clutter the source
tree with build files. If you want to reset, you can just delete ``build/`` and
recreate it as above.


Blinking an LED in C
--------------------

This is the pre-Hello World example which just binks the onboard LED in the
pico. Nothing fancy, but a great sanity check for the toolchain.

.. code:: C
   :number-lines:

    /**
     * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
     *
     * SPDX-License-Identifier: BSD-3-Clause
     */
    
    #include "pico/stdlib.h"
    
    int main() {
    #ifndef PICO_DEFAULT_LED_PIN
    #warning blink example requires a board with a regular LED
    #else
        const uint LED_PIN = PICO_DEFAULT_LED_PIN;
        gpio_init(LED_PIN);
        gpio_set_dir(LED_PIN, GPIO_OUT);
        while (true) {
            gpio_put(LED_PIN, 1);
            sleep_ms(250);
            gpio_put(LED_PIN, 0);
            sleep_ms(250);
        }
    #endif
    }


Building and running blink
--------------------------

You may notice that CMake has pulled the required SDK files into ``build/``. To
build ``blink`` just do the following::
    
    $ cd build/blink
    $ make -j16

This will build not just ``blink.c``, but also the necessary tooling to create
a bootable image. Just like when setting the ``MAKEOPTS`` for the
``cross-arm-none-eabi`` overlay, use a value for the number of ``make`` jobs
that is appropriate for your system.

To install the image onto the Pico, mount it in mass-storage mode just like when
doing the initial sanity check and just copy it over.

::
    
    # lsblk
    NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINTS
    sda           8:0    1   128M  0 disk 
    `-sda1        8:1    1   128M  0 part 
    # mount /dev/sda1 /mnt
    # cp blink.uf2 /mnt
    # umount /mnt

Copying ``blink.uf2`` onto the Pico will automatically detach it from the USB
port and reboot. When it's booted, the onboard LED should be blinking on and
off every 1/4 second. Since it's detached, unmounting won't do anything beyond
cleaning up after the old mount. This is a good thing to do though.


Hello World (serial)
--------------------

A "proper" Hello World example. This code prints "Hello, world!" onto serial out
every second.

.. code:: C
   :number-lines:

    /**
     * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
     *
     * SPDX-License-Identifier: BSD-3-Clause
     */
    
    #include <stdio.h>
    #include "pico/stdlib.h"
    
    int main() {
        stdio_init_all();
        while (true) {
            printf("Hello, world!\n");
            sleep_ms(1000);
        }
        return 0;
    }


Building and running hello_serial
---------------------------------

Building and running ``hello_serial`` is basically the same as ``blink``::
    
    $ cd build/hello_world/serial
    $ make -j16

Installing is also basically the same::
    
    # mount /dev/sda1 /mnt
    # cp hello_serial.uf2 /mnt
    # umount /mnt

To see the output, plug in the USB UART as well. If your machine is configured
correctly, you should find ``/dev/ttyUSB0``. This is the serial line we need to
connect to::
    
    $ minicom -b 115200 -D /dev/ttyUSB0
    Hello, world!
    Hello, world!
    Hello, world!
    ...

To exit, hit ``Ctrl-A X``.


License
=======

All of the Raspberry Pi Pico example code is Copyright by Raspberry Pi
(Trading) Ltd. and released under the BSD 3 clause license.


Resources
=========

#. `Getting Started with Raspberry Pi Pico`_
#. `Raspberry Pi Pico datasheet`_
#. `Raspberry Pi Pico C/C++ SDK`_
#. `Raspberry Pi Pico examples`_
#. `Arm Cortex-M0+`_
#. `crossdev`_
#. `Portage repositories`_

.. _This patch:
.. _crossdev bug fix:
    0001-crossdev-use-package.use.-mask-force-for-pie-ssp.patch

.. _#831165:
    https://bugs.gentoo.org/831165

.. _GCC docs:
    https://gcc.gnu.org/onlinedocs/gcc/ARM-Options.html

.. _make.conf(5):
    https://dev.gentoo.org/~zmedico/portage/doc/man/make.conf.5.html

.. _unc3nsored:
    https://github.com/xxc3nsoredxx/unc3nsored

.. _Getting Started with Raspberry Pi Pico:
    https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf

.. _Raspberry Pi Pico datasheet:
    https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf

.. _Raspberry Pi Pico C/C++ SDK:
    https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-c-sdk.pdf

.. _Raspberry Pi Pico examples:
    https://github.com/raspberrypi/pico-examples

.. _Arm Cortex-M0+:
    https://developer.arm.com/ip-products/processors/cortex-m/cortex-m0-plus

.. _crossdev:
    https://wiki.gentoo.org/wiki/Crossdev

.. _Portage repositories:
    https://wiki.gentoo.org/wiki/Repository_format
