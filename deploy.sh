#!/bin/sh
hexo clean &&
    hexo generate && 
    rm -v public/big_files/* &&
    ln -s $PWD/big_files/* $PWD/public/big_files/ &&
    sudo /bin/rm -rv /srv/data/www/blog/* &&
    sudo cp -rv public/* /srv/data/www/blog/ &&
    echo Done

