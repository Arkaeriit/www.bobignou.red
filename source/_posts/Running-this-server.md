---
title: Running this server
date: 2021-11-18 09:20:27
tags:
---
Multiples tools and components are used in this server to make it run and accessible from the internet. I want to describe them here in order to help me reconfigure a similar server in the future if needed. It might also be useful to anyone searching to run a similar web server themselves.

## Domain name
In order to easily access the server for the outside, a domain name is very handy I purchased bobignou.red at [Namecheap](https://www.namecheap.com/). There is a lot of other alternative but I am telling that I used them as I use some of their other services.

## Dynamic DNS
As I don't have a static IP address, linking the domain name to my IP address is not trivial. I have to rely on dynamic DNS.

Tc do so, I use a combination of Namecheap's advanced DNS and DDclient.

### Namecheap's advanced DNS
On the page to manage a domain name in Namecheap website, there is an 'Advanced DNS' page. At the bottom of this page, there is a 'Dynamic DNS' category. Firstly, you should enable it with the little oval button. You are given a Dynamic DNS Password, write it down. Lastly, you must add a record for each subdomain you want to use. To do so, press the 'add new record' button. Under the 'Host' column, you can can write the name of the subdomain (for example, `@` for `bobignou.red` or `www` for `www.bobignou.red`) and you should write a dummy IP in the 'Value' column.

### DDclient
On the server, install DDclient. You configure it with the configuration file `/etc/ddclient.conf`. To configure a subdomain, write the following configuration:
```
use=web, web=dynamicdns.park-your-domain.com/getip
protocol=namecheap
server=dynamicdns.park-your-domain.com
login=<domain name>
password='<Dynamic DNS Password>'
<Host>
```
Write one of such config for each subdomain.

Then, you can start dd client with systemd through the commands `systemctl enable ddclient` and `systemctl start ddclient`. You can check that it works well in two ways.
* You can check the result of `systemctl status ddclient`.
* You can verify that your IP have been added in the column 'Value' in Namecheap's advanced DNS.


