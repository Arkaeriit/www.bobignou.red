#!/bin/sh

# Web
hexo clean &&
    hexo generate && 
    rm -v public/big_files/* &&
    ln -s $PWD/big_files/* $PWD/public/big_files/ &&
    sudo /bin/rm -rfv /srv/data/www/blog/* &&
    sudo cp -rv public/* /srv/data/www/blog/ &&
    echo Done

# Gemini
sudo /bin/rm -rfv /srv/data/gemini/content &&
    sudo mkdir -p /srv/data/gemini/content &&
    sudo cp -rv gemini /srv/data/gemini/content/bobignou.red &&
    sudo ln -s /srv/data/gemini/content/bobignou.red /srv/data/gemini/content/gemini.bobignou.red

