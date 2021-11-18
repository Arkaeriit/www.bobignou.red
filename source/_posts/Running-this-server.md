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
Write one of such configuration for each subdomain.

Then, you can start dd client with systemd through the commands `systemctl enable ddclient` and `systemctl start ddclient`. You can check that it works well in two ways.
* You can check the result of `systemctl status ddclient`.
* You can verify that your IP have been added in the column 'Value' in Namecheap's advanced DNS.

## SSL certificates
In order to use HTTPS, you need SSL certificates. Fortunately, a tool named certbot made by let's encrypt makes it really easy to get. You just need to install certbot that is probably in your distribution's repository. Before starting, you must make sure that using your domain name, one can reach your server (you must enable port forwarding in your router for ports 80 and 443) and that no program uses those ports on your server.

Then you just have to type the command `certbot certonly --standalone -d <your first domain name> -d <your second domain name> ...` and follow the steps.

## The Nginx web server
I Use Nginx as the web server. Each interface is in a `server` block. All those blocks are in a `http` block. I did not customized the `http` block, I kept the default one which work. The file for this blocks are in the folder `/srv/data/www/blog`. The layout of the file system is the same as the layout of the website.

### Basic HTTP server
On port 80, I present the site in HTTP, under the domain name `bobignou.red`. The configuration is the following:
```
server {
        listen 80;
        index index.html;
        server_name         bobignou.red;

        root /srv/data/www/blog;
        location / {
                try_files $uri $uri/ =404;
        }
}
```
The configuration is extremely simple because the layout of the file system is the same as the one of the website.

### HTTP proxy
As I also want to redirect `www.bobignou.red` to this website, I used a reverse proxy whose configuration is the following:
```
server {
        listen 80;
        server_name         www.bobignou.red;

        location / {
                proxy_pass http://bobignou.red; 
        }
}
```
Once again, it is very simple.

### HTTPS server
As we are in the 21st century, I wanted to also present a HTTPS server. Its configuration is the following:
```
server {
        listen              443 ssl;
        server_name         bobignou.red;
        ssl_certificate     /etc/letsencrypt/live/bobignou.red/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/bobignou.red/privkey.pem;
        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         HIGH:!aNULL:!MD5;
        index index.html;

        root /srv/data/www/blog;
        location / {
                try_files $uri $uri/ =404;
        }
}
```
The configuration is very similar to the one in the HTTP server but there is a lot of extra info needed to enable SSL. It is still very easy to do.

### HTTPS proxy
To acces `www.bobignou.red` with SSL, I used a reverse proxy that re-route the SSL-encripted trafic to the HTTP server at `bobignou.red`. Here is the configuration:
```
server {
        listen              443 ssl;
        server_name         www.bobignou.red;
        ssl_certificate     /etc/letsencrypt/live/bobignou.red/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/bobignou.red/privkey.pem;
        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         HIGH:!aNULL:!MD5;

        location / {
                proxy_pass http://bobignou.red:80;
        }
}
```

## Flask server
On this server, I also run `cyberland.bobignou.red` which is powered by Flask. Setting it up is a bit more tricky than the blog.

### Making a service
To ensure the Cyberland server is always on, I want it to start when the computer starts. To do so, I wrote a simple systemd service file:
```
[Unit]
Description=Starts the cyberland server
After=network.target

[Service]
Type=simple
# Another Type: forking
User=root
Group=root
WorkingDirectory=/srv/data/www/cyberland
ExecStart=/srv/data/www/cyberland/cyberland.py
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
I can then save it as `/etc/systemd/system/cyberland.service` and have it start with the computer thanks to the command `systemctl enable cyberland`.

### Accessing it from the outside
Linking the Flask server to the outside work is made with a Nginx reverse proxy. The configuration is the following:
```
# HTTP server for Cyberland
server {
        listen 80;
        server_name        cyberland.bobignou.red;

        location / {
                proxy_pass http://127.0.0.1:8901;
        }
}

# HTTPS server for Cyberland
server {
        listen              443 ssl;
        server_name         cyberland.bobignou.red;
        ssl_certificate     /etc/letsencrypt/live/bobignou.red/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/bobignou.red/privkey.pem;
        ssl_protocols       TLSv1 TLSv1.1 TLSv1.2;
        ssl_ciphers         HIGH:!aNULL:!MD5;

        location / {
                proxy_pass http://127.0.0.1:8901;
        }
}
```
It looks a lot like the configuration of the reverse proxy for the blog.

## Website generation
The pages in this we website are generated with [hexo](https://github.com/hexojs/hexo). I mostly used the default configuration by following the steps in the official documentation.

