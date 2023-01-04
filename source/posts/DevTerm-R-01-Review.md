---
title: DevTerm R-01 Review
date: 2022-10-18 11:49:04
tags:
---

## Introduction

I have been interested in RISC-V for a while. I played a bit with RISC-V cores on FPGA but it is quite hard to find RISC-V cores on general-purpose computers.  Fortunately, the company ClockworkPi is making the [DevTerm R-01](https://www.clockworkpi.com/product-page/devterm-kit-r01), a handheld computer with a RISC-V processor. The DevTerm R1 is a handheld computer featuring an RV64IMAFDCVU
 single core RISC-V processor.

## Hardware

![The DevTerm in its box](DevTerm_in_box.jpg)

The DEvTerm is sold as a kit that needs to be put together by the user. A lot of thought has been put into making the assembly process as easy as possible. All the process is well documented in an instruction booklet. The tolerances are made so that the DevTerm seems sturdy but is still easy to assemble. The only issue I had was the absence of a supposedly included screwdriver used for screws that secure the SODIMM processor module to the _motherboard_. Fortunately, those screws are optional as the SODIMM module stays in place in its bracket.

![The DevTerm during assembly](DevTerm_in_progress.jpg)

The final product has a great look and feel,  the design is quite well thought out. The screen and keyboard are both ways better than expected. The screen is __very__ wide and quite crisp. The keyboard is not perfect but good enough to type on. The computer is a bit too wide to comfortably type while being held and a bit too small to type fast while resting on a surface but it offers a better experience than typing on a smartphone and it is way easier to carry and take out than a full-blown laptop.

![The DevTerm up and running](DevTerm_assembled.jpg)

The DevTerm also has some more exotic features. A thermal printer is included, I did not try it yet but it could be a fun experience. Another neat feature is the removable battery. The DevTerm uses standard 18650
cells that can easily be purchased. If you were to buy extra, you can use them to extend the product's usable time.

One of the weaker points of the hardware is the anemic CPU. Even installing packages takes a very long time. Basic text editing is not too painful but anything more demanding stops being fluid. On the plus side, that CPU only sips power, resulting in acceptable battery life.

The pointing device included is a trackball on top of the keyboard with buttons just below the space bar. This does not feel great to use so I installed DWM to use it as little as possible.

## Software

As far as software goes, Clockwork Pi provides an image of Ubuntu for RISC-V which works well enough. It uses by default TWM as the window manager, which I replaced with DWM. I was was pleasantly surprised to see that all the headers to compile DWM are included by default.

Command line utilities and text editors work well, or as well as the weak CPU let them. Basic GUI programs perform decently as well. Unfortunately, heavier software struggles. For example, in GIMP, the streak of paint follows the brush with a bit of latency.

The main weakness as far as software go is web browsers. Firefox is not available. Qutebrowser is installed but it is compiled against an old WebKit version that crashes on some websites such as GitHub. The best way I found to browse the web on this machine is to SSH to my desktop PC and run [Browsh](https://www.brow.sh/) there.  This results in a pixelated but smooth experience.

## Conclusion

The DevTerm R1 is a device with quite a bit of flaws but its form factor and battery life make it a great device to write while commuting, which is the reason I purchased it. Furthermore, the RISC-V processor really helps its cool factor.

