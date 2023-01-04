---
title: Gemini
date: 2022-01-08 15:16:24
tags:
---

## Gemini protocol

[Gemini](https://gemini.circumlunar.space/) is a nice alternative to the web. It is lighter than the web and very simple to host so I decided to host a copy of this blog as a Gemini server.

## Making Gemini pages

Instead of HTML, Gemini clients and servers expect to handle pages written in Gemtext, a markup language made for the protocol.

Gemtext looks a lot like Markdown and is quite easy to write by hand. One of the biggest differences is that the links are not presented in the same way and can not be inlined in the text. This means that I can't reuse the markdown text I use to generate this blog.

Fortunately, a tool exists to easily convert markdown to Gemtext, [md2gemini](https://github.com/makeworld-the-better-one/md2gemini). I use it to make the bulk of the conversion and then, I polish by hand the generated Gemtext file.

## Hosting a Gemini server

To host a Gemini page (also known as "capsule"), a lot of software has been written. Those programs are not as feature-full as Apache or Nginx for the web but they are enough to host a simple blog (or maybe the proper term would be gem-log?). I choose to use [Agate](https://github.com/mbrubeck/agate) because it is very easy to use.

## Accessing the Geminispace

Once your Gemini capsule is live, you need a browser to access it. I really like [Amfora](https://github.com/makeworld-the-better-one/amfora) because I feel like it is a very good balance between simplicity and good features.

You can then use it to go read this blog on the Geminispace with the command:
```
amfora bobignou.red
```

