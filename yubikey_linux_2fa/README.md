# Setting up Yubikey for Linux 2FA login
I got two Yubikeys so I wanted to figure out how to use them for logging in to my machine.
In my case, specifically for logging in as root.

## Requirements
 * [`pam-u2f` module][pam-u2f]
   * Gentoo: `sys-auth/pam_u2f`
 * Kernel options
   * `CONFIG_HIDRAW`
   * `CONFIG_USB_HIDDEV`

## Registering a key to a user
Add the user to the `plugdev` group (if it isn't already) by running (as root):
```bash
usermod -a -G plugdev user
```
Then log out and log back in.
This is obviously not needed for the root user.

The PAM module will look for a key mapping in `$XDG_CONFIG_HOME/Yubico/u2f_keys` or in `~/.config/Yubico/u2f_keys` (if the `XDG_CONFIG_HOME` environment variable isn't set).
To create the mapping for `user`, run:
```bash
mkdir -p ~/.config/Yubico
pamu2fcfg -uuser > ~/.config/Yubico/u2f_keys
```
Touch the Yubikey when it starts blinking.

## Setting up PAM for Yubikey
To require password + Yubikey, put the following in `/etc/pam.d/system-auth`:
```pam
auth    [success=1 default=ignore]  pam_unix.so     nullok try_first_pass
auth    [default=die]               pam_faillock.so authfail
auth    required                    pam_u2f.so      nouserok cue
```
The first two lines should already be present (may not be exact, but similar at least).
They're just there to give context for the third line (the one to add).
The `success=1` in the `pam_unix.so` line means that PAM will skip over the next module if password authentication succeeds (jumping to the `pam_u2f.so` line).
`nouserok` means that If a user doesn't have a key mapping, then the module will succeed instead of failing.
Authenticating should now require a password followed by touching the Yubikey.
An easy way to check is to simply log in at a new TTY.

Alternatively, to set up the Yubikey as an equivalent option to passwords, put:
```pam
auth    sufficient                  pam_u2f.so      cue
auth    [success=1 default=ignore]  pam_unix.so     nullok try_first_pass
```
Note that this time `pam_u2f.so` is before `pam_unix.so` and is `sufficient` instead of `required`.
Also, no `nouserok` because PAM should continue to the password auth if Yubikey fails.

***PRO TIP:***
A broken PAM will likely mean broken auths all around (good luck logging in).
Which will likely require either a live boot or dropping into single user mode to fix.
A rather sticky situation indeed.
Leave a spare root login open (such as in a TTY) when messing around with PAM.

See also: [Gentoo Wiki page][yubikey gentoo wiki] where I wrote up a more detailed set of instructions up to this point.

## Root logged in? Yubikey removed? LOCK!
Since my goal with this is to make a more secure root user, pulling out the Yubikey while root is logged in should instantly lock the machine.
Both when directly through login or through `su(1)`.
On the other hand, if root isn't logged in then plugging/unplugging shouldn't do anything.

The best way to do detect removal of the Yubikey is through `udev`.
Running `udevadm monitor -k -p`, followed by plugging in and removing it, gave this as the earliest uevent that could be used:
```
KERNEL[1683.664130] remove   /devices/pci0000:00/0000:00:08.1/0000:06:00.4/usb4/4-2/4-2:1.0/0003:1050:0407.0003/input/input16 (input)
ACTION=remove
DEVPATH=/devices/pci0000:00/0000:00:08.1/0000:06:00.4/usb4/4-2/4-2:1.0/0003:1050:0407.0003/input/input16
EV=120013
LED=1f
MSC=10
NAME="Yubico YubiKey OTP+FIDO+CCID"
PHYS="usb-0000:06:00.4-2/input0"
PRODUCT=3/1050/407/110
PROP=0
SEQNUM=3001
SUBSYSTEM=input
UNIQ=""
```
So the corresponding rule placed in `/etc/udev/rules.d/00-yubikey.rules` is:
```udev
# Lock system if root logged in and Yubikey removed
ACTION=="remove", SUBSYSTEM=="input", ENV{PRODUCT}=="*1050/407*", RUN+="/usr/local/bin/root_lock.sh"
```

Since there isn't a builtin method to test for who's logged in that covers both physical and `su(1)`, I had to create a script to handle that that.
The script should check if root is logged in.
Then lock and require the root password to unlock.
If root is not logged in the script should do nothing.
Additionally, if the machine is already locked it should do nothing.
That way repeatedly plugging/unplugging the Yubikey at the lock screen should not cause more and more of them to stack on top of each other.

You can find my script that does just this [here][root_lock.sh].

If root isn't already logged in, log in.
Install the script into `/usr/local/bin`.
Then unplug the Yubikey.
If all went well, the machine should lock and require the root password (and Yubikey) to unlock.

<h2><a href='https://github.com/xxc3nsoredxx'><code>return</code></a></h2>


<!-- link refs -->
[pam-u2f]: https://github.com/Yubico/pam-u2f
[yubikey gentoo wiki]: https://wiki.gentoo.org/wiki/YubiKey
[root_lock.sh]: https://github.com/xxc3nsoredxx/misc-utils/blob/master/root_lock/root_lock.sh
