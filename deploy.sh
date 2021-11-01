#!/bin/sh
hexo clean &&
    hexo generate && 
    sudo /bin/rm -rv /srv/www/* &&
    sudo cp -rv public/* /srv/www/ &&
    echo Done
