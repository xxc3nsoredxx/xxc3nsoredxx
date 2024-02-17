# xxc3nsoredxx

So, you've found my GitHub page.
This can only mean one of two things:

 1. You already know me from somewhere. In that case, you probably got here through a link I shared and are at least somewhat familiar with what interests me.
 2. You've stumbled upon this page from somewhere else. In that case, do check stuff out. If you want. I can't _make you_ do that.

The bio field on the profile is quite short, so finding out I could make a profile README was great.
Also, I don't have other social media or blog or anything, so why not figure out how to turn my GitHub profile into a poor, hackish version of that?

## Education
I've got a BS in Computer Science, and a Master's in CS with a specialization in Information Assurance and Graduate Level Designation in Cyber Operations.

## Interests and whatnot
My main interests are cyber security, low level development, and Linux.
Bonus points for things that combine two of them together.
If it covers all three, then you've _really_ piqued my interest now!

I use Gentoo on my laptops because, other than LFS, I don't know of anything that starts you out with as bare of a slate and has you build up from there.
Even when installing programs you have a very minimal default set of features and have to explicitly instruct Portage to compile in more if you want more.
I absolutely love that.

## too short; want more
[A longer "about me"][about] for people who want more rambling in textual form.

## Gentoo overlay
It was only a matter of time until I came across some piece of software that wasn't available in the main Portage tree.

To add the repo, run:
```
eselect repository enable unc3nsored
emaint sync -r unc3nsored
```

[Link to overlay][unc3nsored]

## Random things I did
[Setting up Yubikey for Linux 2FA login][yubikey]
&mdash; See also: [Gentoo Wiki page][yubikey gentoo wiki] where I wrote up a more detailed set of instructions.

[An Absolutely Stupid Regex Benchmark][stupid benchmark]

[Getting Started with Raspberry Pi Pico on Gentoo][pico]

[A Useless GCC Benchmark][gcc benchmark]

## PGP
[Public key][pgp]


<!-- link refs -->
[about]: ABOUT.md
[unc3nsored]: https://github.com/xxc3nsoredxx/unc3nsored
[yubikey]: yubikey_linux_2fa/
[yubikey gentoo wiki]: https://wiki.gentoo.org/wiki/YubiKey
[stupid benchmark]: stupid_benchmark/
[pico]: pico/
[gcc benchmark]: gcc_benchmark/

<!-- public key links will stay at the end, raw download last -->
[pgp]: https://raw.githubusercontent.com/xxc3nsoredxx/xxc3nsoredxx/master/pubkey.asc
