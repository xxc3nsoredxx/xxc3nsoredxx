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
    |        +- cross-arm-none-eabi.conf
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

The ebuilds are hosted in the unc3nsored_ overlay. If it's not already added
(and let's be real, who'd've added it up until this point), do the following to
add and sync the ebuilds::
    
    # eselect repository enable unc3nsored
    # emaint sync -r unc3nsored

Specifically, there's two packages which are relevant:

#. ``dev-libs/pico-sdk``
#. ``dev-libs/tinyusb``

   - Automatically pulled in as a dependency when the ``usb`` USE flag is
     enabled on the above (enabled by default).


Installing the SDK (for real this time)
---------------------------------------

With the overlay added, installation is as simple as adding the package(s) into
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

(At least) the following kernel options should be set. Depending your USB UART
device, you may need to set additional options:

- ``CONFIG_USB_ACM``
- ``CONFIG_USB_SERIAL``
- ``CONFIG_USB_SERIAL_CONSOLE``
- ``CONFIG_USB_SERIAL_GENERIC``
- ``CONFIG_USB_SERIAL_SIMPLE``

::
    
    Device Drivers  --->
       [*] USB support  --->
          <M>   USB Modem (CDC ACM) support
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
Pico. Nothing fancy, but a great sanity check for the toolchain.

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


Hello World (UART)
------------------

A "proper" Hello World example. This code prints "Hello, world!" onto UART once
every second. This is ``hello_serial`` in the upstream repo.

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


Building and running hello_uart
-------------------------------

Building and running ``hello_uart`` is basically the same as ``blink``::
    
    $ cd build/hello_world/uart
    $ make -j16

Installing is also basically the same::
    
    # mount /dev/sda1 /mnt
    # cp hello_uart.uf2 /mnt
    # umount /mnt

To see the output, plug in the USB UART as well. If your machine is configured
correctly, you should find a brand new ``/dev/ttyUSB0``. This is the serial line
we need to connect to::
    
    $ minicom -b 115200 -D /dev/ttyUSB0
    Hello, world!
    Hello, world!
    Hello, world!
    ...

To exit, hit ``Ctrl-A X``.


Hello World (USB)
-----------------

Another "proper" Hello World, but this time we're using the Pico's USB serial
output instead of the UART.

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

The astute among you may notice some similarities with the previous example. If
you didn't catch it, they're the same code. This is because the output can be
directed to either UART or USB (or possibly both) at compile time. UART is the
default. This is the relevant part of the ``CMakeLists.txt``:

.. code:: CMake

    # enable usb output, disable uart output
    pico_enable_stdio_usb(hello_usb 1)
    pico_enable_stdio_uart(hello_usb 0)


Building and running hello_usb
------------------------------

This is so similar to the above that I won't even bother writing the build
instructions. The only part that's different is getting the output. It is most
likely going to be on ``/dev/ttyACM0``, unless you happen to have something else
on that serial line::
    
    $ minicom -b 115200 -D /dev/ttyACM0
    Hello, world!
    Hello, world!
    Hello, world!
    ...


Dual USB mass storage
---------------------

This is a much more interesting bit of code which comes from TinyUSB's own set
of examples. It emulates *two* mass storage class devices using the Pico. If you
don't know what that is by name alone think flash drives, external hard drives,
anything that is bulk storage and is connected via USB.

The code is also much longer than the previous examples, so I'm not going to
copypasta it here. The source files can be found in `the examples directory`_,
and I recommend you check them out:

- ``main.c`` -- contains the main loop and code for blinking the LED
- ``msc_disk_dual.c`` -- contains the binary blobs representing the disks and
  the code to handle the required USB protocol
- ``tusb_config.h`` -- contains some constants used by TinyUSB
- ``usb_descriptors.c`` -- contains the structures used to describe the USB
  device and the code to handle device description requests

I made a few small changes to the upstream example:

- Made the contents of the files a bit more clear as to which device they're on
- Replaced DOS with Unix line endings and added a terminating newline
- Made the ``CMakeLists.txt`` work with our Pico SDK setup


Local machine prep (optional, but recommended)
----------------------------------------------

This example emulates two MBR disks with FAT12 formatted file systems. In order
to get the most out of it, the following kernel options should be set:

- ``CONFIG_BLOCK``
- ``CONFIG_MSDOS_FS``
- ``CONFIG_MSDOS_PARTITION``
- ``CONFIG_PARTITION_ADVANCED``
- ``CONFIG_VFAT_FS``

::
    
    [*] Enable the block layer  --->
           Partition Types  --->
              [*] Advanced partition selection
              [*]   PC BIOS (MSDOS partition tables) support
        File systems  --->
           DOS/FAT/EXFAT/NT Filesystems  --->
              <M> MSDOS fs support
              <M> VFAT (Windows-95) fs support

Rebuild the kernel and reboot if needed.


Building and running msc_dual_lun
---------------------------------

Building ``msc_dual_lun`` is basically the same as all the others::
    
    $ cd build/msc_dual_lun
    $ make -j16

This time when installing we want to be quick about cleaning up the mounts::
    
    # mount /dev/sda1 /mnt && cp msc_dual_lun.uf2 /mnt && umount /mnt

While the Pico reboots, you should see something similar to this appear in
``dmesg``:

.. code:: dmesg

    kern  :info  : [Jan22 18:35] usb 2-2: USB disconnect, device number 6
    kern  :info  : [  +0.292318] usb 2-2: new full-speed USB device number 7 using xhci_hcd
    kern  :info  : [  +0.155334] usb 2-2: New USB device found, idVendor=cafe, idProduct=4002, bcdDevice= 1.00
    kern  :info  : [  +0.000013] usb 2-2: New USB device strings: Mfr=1, Product=2, SerialNumber=3
    kern  :info  : [  +0.000004] usb 2-2: Product: TinyUSB Device
    kern  :info  : [  +0.000003] usb 2-2: Manufacturer: TinyUSB
    kern  :info  : [  +0.000003] usb 2-2: SerialNumber: 123456789012
    kern  :info  : [  +0.001786] usb-storage 2-2:1.0: USB Mass Storage device detected
    kern  :info  : [  +0.000770] scsi host0: usb-storage 2-2:1.0
    kern  :info  : [  +1.024797] scsi host0: scsi scan: INQUIRY result too short (5), using 36
    kern  :notice: [  +0.000019] scsi 0:0:0:0: Direct-Access     TinyUSB  Mass Storage     1.0  PQ: 0 ANSI: 2
    kern  :notice: [  +0.000556] scsi 0:0:0:1: Direct-Access     TinyUSB  Mass Storage     1.0  PQ: 0 ANSI: 2
    kern  :notice: [  +0.000836] sd 0:0:0:0: [sda] 16 512-byte logical blocks: (8.19 kB/8.00 KiB)
    kern  :notice: [  +0.000299] sd 0:0:0:1: [sdb] 16 512-byte logical blocks: (8.19 kB/8.00 KiB)
    kern  :notice: [  +0.000651] sd 0:0:0:0: [sda] Write Protect is off
    kern  :debug : [  +0.000005] sd 0:0:0:0: [sda] Mode Sense: 03 00 00 00
    kern  :err   : [  +0.001990] sd 0:0:0:0: [sda] No Caching mode page found
    kern  :err   : [  +0.000006] sd 0:0:0:0: [sda] Assuming drive cache: write through
    kern  :notice: [  +0.002010] sd 0:0:0:1: [sdb] Write Protect is off
    kern  :debug : [  +0.000010] sd 0:0:0:1: [sdb] Mode Sense: 03 00 00 00
    kern  :err   : [  +0.001999] sd 0:0:0:1: [sdb] No Caching mode page found
    kern  :err   : [  +0.000004] sd 0:0:0:1: [sdb] Assuming drive cache: write through
    kern  :info  : [  +0.008501]  sda:
    kern  :notice: [  +0.006497] sd 0:0:0:0: [sda] Attached SCSI removable disk
    kern  :info  : [  +0.003955]  sdb:
    kern  :notice: [  +0.004031] sd 0:0:0:1: [sdb] Attached SCSI removable disk

To view the contents of one of them, run::
    
    # mount /dev/sda /mnt
    # ls -alF /mnt
    total 1
    drwxr-xr-x. 2 root root 512 Dec 31  1969 ./
    drwxr-xr-x. 1 root root 142 Feb 26  2021 ../
    -rwxr-xr-x. 1 root root 168 Nov  5  2013 README0.TXT*
    # cat /mnt/README0.TXT
    LUN0: This is the first mass storage device in tinyusb's MSC demo.
    
    If you find any bugs or get any questions, feel free to file an issue
    at github.com/hathach/tinyusb
    # umount /mnt

**Note:** Even if they don't show as having any partitions, mounting the raw
disk itself should work just fine.

If you opted to not set up MBR and FAT support in your kernel, you can still
view the contents by running::
    
    # dd if=/dev/sda bs=512 count=4 status=none | hexdump -C
    00000000  eb 3c 90 4d 53 44 4f 53  35 2e 30 00 02 01 01 00  |.<.MSDOS5.0.....|
    00000010  01 10 00 10 00 f8 01 00  01 00 01 00 00 00 00 00  |................|
    00000020  00 00 00 00 80 00 29 34  12 00 00 54 69 6e 79 55  |......)4...TinyU|
    00000030  53 42 20 30 20 20 46 41  54 31 32 20 20 20 00 00  |SB 0  FAT12   ..|
    00000040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    000001f0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 55 aa  |..............U.|
    00000200  f8 ff ff ff 0f 00 00 00  00 00 00 00 00 00 00 00  |................|
    00000210  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    00000400  54 69 6e 79 55 53 42 20  30 20 20 08 00 00 00 00  |TinyUSB 0  .....|
    00000410  00 00 00 00 00 00 4f 6d  65 43 00 00 00 00 00 00  |......OmeC......|
    00000420  52 45 41 44 4d 45 30 20  54 58 54 20 00 c6 52 6d  |README0 TXT ..Rm|
    00000430  65 43 65 43 00 00 88 6d  65 43 02 00 a8 00 00 00  |eCeC...meC......|
    00000440  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    00000600  4c 55 4e 30 3a 20 54 68  69 73 20 69 73 20 74 68  |LUN0: This is th|
    00000610  65 20 66 69 72 73 74 20  6d 61 73 73 20 73 74 6f  |e first mass sto|
    00000620  72 61 67 65 20 64 65 76  69 63 65 20 69 6e 20 74  |rage device in t|
    00000630  69 6e 79 75 73 62 27 73  20 4d 53 43 20 64 65 6d  |inyusb's MSC dem|
    00000640  6f 2e 0a 0a 49 66 20 79  6f 75 20 66 69 6e 64 20  |o...If you find |
    00000650  61 6e 79 20 62 75 67 73  20 6f 72 20 67 65 74 20  |any bugs or get |
    00000660  61 6e 79 20 71 75 65 73  74 69 6f 6e 73 2c 20 66  |any questions, f|
    00000670  65 65 6c 20 66 72 65 65  20 74 6f 20 66 69 6c 65  |eel free to file|
    00000680  20 61 6e 20 69 73 73 75  65 0a 61 74 20 67 69 74  | an issue.at git|
    00000690  68 75 62 2e 63 6f 6d 2f  68 61 74 68 61 63 68 2f  |hub.com/hathach/|
    000006a0  74 69 6e 79 75 73 62 0a  00 00 00 00 00 00 00 00  |tinyusb.........|
    000006b0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    00000800

Viewing the other one is left as an exercise to the reader.


SWD
===

This guide doesn't cover using SWD to debug or flash the Pico. Mainly because
the pins are at the bottom, which is a rather unfortunate location since I can't
pull them out without either a clip or soldering wires to them. Maybe in the
future, but this is currently an indefinite TODO.

The following chapters in the official "Getting Started" guide are relevant:

- Chapter 5: Flash Programming with SWD
- Chapter 6: Debugging with SWD
- Appendix A: Using Picoprobe

  - Instructions on using a second Pico as a debug probe.


License
=======

The example code in ``blink/`` and ``hello_world/`` is Copyright by Raspberry
Pi (Trading) Ltd. and released under the BSD 3 clause license. The example code
in ``msc_dual_lun/`` is Copyright by Ha Thach (tinyusb.org) and released under
the MIT license.


Resources
=========

#. `Getting Started with Raspberry Pi Pico`_
#. `Raspberry Pi Pico datasheet`_
#. `Raspberry Pi Pico C/C++ SDK`_
#. `Raspberry Pi Pico examples`_
#. `TinyUSB examples`_
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

.. _the examples directory:
.. _dual MSC example directory:
    examples/msc_dual_lun

.. _Getting Started with Raspberry Pi Pico:
    https://datasheets.raspberrypi.com/pico/getting-started-with-pico.pdf

.. _Raspberry Pi Pico datasheet:
    https://datasheets.raspberrypi.com/pico/pico-datasheet.pdf

.. _Raspberry Pi Pico C/C++ SDK:
    https://datasheets.raspberrypi.com/pico/raspberry-pi-pico-c-sdk.pdf

.. _Raspberry Pi Pico examples:
    https://github.com/raspberrypi/pico-examples

.. _TinyUSB examples:
    https://github.com/hathach/tinyusb/tree/master/examples

.. _Arm Cortex-M0+:
    https://developer.arm.com/ip-products/processors/cortex-m/cortex-m0-plus

.. _crossdev:
    https://wiki.gentoo.org/wiki/Crossdev

.. _Portage repositories:
    https://wiki.gentoo.org/wiki/Repository_format
