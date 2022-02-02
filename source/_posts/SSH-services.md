---
title: SSH services
date: 2022-02-02 08:56:44
tags:
---
SSH is a nice technology. Not only can it be used to securely access another computer, but it can be used for other encrypted communication. Indeed, running a custom-made SSH server can be a way to expose nice services to the outside world. I want to give here some examples.

## Charm

The organization [Charm](https://charm.sh/) made a lot of interesting services such [Soft Serve](https://github.com/charmbracelet/soft-serve) that I presented in another blog post. Another very interesting project they made is the [Charm Cloud](https://github.com/charmbracelet/charm). On a host machine, you run an instance of this server and it can be used to sync your data between different machines. For example, I use it with [Skate](https://github.com/charmbracelet/skate) to create todo-lists that are synced between my different machines.

If you don't want to set up your own instance of Charm Cloud, a public version exists. As the data are encrypted with your SSH key, you can expect them to stay safe.

![Todo-list synced over multiple machines](skate_montage.png)

## Devzat

Charm Cloud and Soft Serve are nice as services you self-host for your personal use but some other projects are meant to be used by everyone in a more centralized manner. For example, [Devzat](https://github.com/quackduck/devzat) is a chatroom running over SSH. You can access it by running the command `ssh <your nick>@devzat.hackclub.com` with any ssh client such as the OpenSSH client.

This nice open-source project is written in Go and open to contributors.

Furthermore a [machine on Hack The Box](https://app.hackthebox.com/machines/398) have been made being inspired by devzat.

![A picture of the chatroom](devzat.png)

## Analog City

[Analog City](https://github.com/analogcity/analogcity) is a text-board running over SSH. If you want to join the other _Pagans_, you can do so with the command `ssh lowlife@45.79.250.220`. There is no domain name but some ways to keep track of the IP without using DNS are being worked on as I write this post.

![A picture of the text-board](analog_city.png)

## Snek

```
ssh -p 2244 snake@bobignou.red 
```

![Playing Snek](snek.png)

