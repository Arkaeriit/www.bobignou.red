---
title: Git server
date: 2021-12-09 14:45:32
tags:
---
I recently found a very nice Git server named [Soft Serve](https://github.com/charmbracelet/soft-serve). This software offers both a git server to store repositories and a nice TUI front-end to list the stored repositories.

This is quite a recent software so there is not a lot of documentation on how to install it. Thus, I want to talk here about how to configure and use it.

![A tasteful TUI](soft-serve.png)

## Setup

### Port forwarding
As we want to access our Git server from the outside, the first step is to enable port forwarding. I have chosen to use the default port for Soft Serve which is 23231 so I enabled port forwarding for port 23231 of the internet to port 23231 of my machine on my LAN.

Soft Serve uses SSH for communication with the external world so there is no need to mess with Nginx proxies or whatnot.

### Download and installation
On the Github page of Soft Serve there are [releases](https://github.com/charmbracelet/soft-serve/releases/) for a lot of different platforms. But you can also compile the software for source if you have go 1.16.1 installed. Once compiled, you just have to copy the binary `soft` in the folder you want (I put it in `/usr/local/bin/soft`) and it should work.

### Systemd service
First, I had to create a folder (`/srv/data/soft-serve`) where Soft Serve could store its configuration and the repositories. Once this was done, I wrote the following systemd service:
```
[Unit]
Description=Starts the soft-serve git server
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/srv/data/soft-serve
ExecStart=/usr/local/bin/soft
Restart=on-failure

[Install]
WantedBy=multi-user.target
```

The fields `WorkingDirectory` and `ExecStart` will change depending on where you stored the `soft` executable and where you want to store Soft Serve data.

I stored the service file at the path `/etc/systemd/system/soft-serve.service`. Then I simply had to type `systemctl enable soft-serve && systemctl start soft-serve` to launch the server.

### First configuration
Once the server is launched you can test it with the command `ssh localhost -p 23231`. You should be greeted by a tasteful TUI. Here, you can copy the command `git clone ssh://localhost:23231/config` which will be used to configure Soft Serve. Use this command to clone the configuration repository. In this repository, edit the file `config.yaml` configure the server.

As I want to open the git server to the world but only let me and a few other people edit the code in the repositories, there are multiple fields in the configuration I need to change.
* host: As I want to log to the git server with an URL, I must change the host to match this URL. Thus, I set it to `git.bobignou.red`.
* anon-access: As I want to only let a small set of users edit repositories but II also want to let anyone read them I set the field anon-access to `read-only`.
* allow-keyless: This field must stay to false because I don't want anyone to be able to freely use the Git server.
* users: To choose which users are allowed to edit the repositories, I must fill in the list of users, and copy-paste their public keys for them to be identified. Here is a dummy example of a dummy user:
```
users:
  - name: me
    admin: true
    public-keys:
      - ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDNtawiMooAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEGgl2I+ypjHnoGl9cZ6dr59zAgMFSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAlbP7vRSaMYNzCcQ4TZOSEaqbgnAT0LAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAzttUgAfXyX7yktWgo/2F6YLsGY/8CPhlM8WY5GvYeJrsHMl8aDYQQ8XyON1M5FN5PFX4g6G9D70HRIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADOh9bdJj3nbJ5Da9BxCTtkY7H me@mycomputer
```

Then I just have to do `git add config.yaml && got commit -m 'Config for public use' && git push origin master` and the configuration is uploaded.

### Adding some flair
As of now, there is not much to customize the look and feel of the TUI. We can still edit the `name` field of `config.yaml` and the file `README.md` to change the title and the text of the _homepage_ of the TUI.

## Usage
Once the setup is finished, most of the work is done. From here, the information on the project's GitHub `README.md` is enough to use the server but I still want to detail them.

### Pushing a new repository on Soft Serve
Pushing a new repository on the server is trivial. On your local machine, simply do `git remote add <remote name> ssh://<server's URL>:<server's port>/<repo name>`. For example, to push the repository `reflet`, I typed `git remote add soft ssh://git.bobignou.red:23231/reflet` from the repository's folder on my local machine. Then, you can push the branch you want to the server.
:w

### Using the TUI
To browse the repositories on Soft Serve, the TUI is very convenient. By typing `ssh -p 23231 git.bobignou.red` I can easily see all the repository I pushed and their `README.md`. The command used to clone the repository is written in the right box which is really neat.

In the comments of the file `config.yaml` it is written that only the repositories listed in the configuration file are shown in the TUI. In the version of Soft Serve that I use (`0.1.0`) this is not the case, all the pushed repositories are displayed in the TUI.

### Using the local repository
Once all of this is done, you can use the remote just as any other remote Git server such as GitHub, GitLab, or Gitolite.

## Web interface
By default, Soft Serve only presents an SSH interface. It is a very nice SSH interface but it is a bit of a shame that there is no web interface. To fix this, I made [Soft Serve Monitor](https://github.com/Arkaeriit/Soft-Serve_Monitor). This is a Flask server that presents a web page with a list of all the repositories on the Soft Serve sever.

I host the web interface under the URL [git.bobignou.red](https://git.bobignou.red).

