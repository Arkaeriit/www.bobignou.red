#!/bin/sh
hexo clean &&
    hexo generate && 
    sudo /bin/rm -rv /srv/data/www/blog/* &&
    sudo cp -rv public/* /srv/data/www/blog/ &&
    echo Done
