#!/bin/sh

HEXO='./node_modules/hexo/bin/hexo'

# Web
./renderer.py &&
    sudo /bin/rm -rfv /srv/data/www/blog/* &&
    sudo cp -rv public/* /srv/data/www/blog/ &&
    echo Done

# Gemini atom
sed 's|https://|gemini://|g; s:\.html:.gmi:g; s:html:text:g;' < public/atom.xml > gemini/atom.xml

# Gemini
sudo /bin/rm -rfv /srv/data/gemini/content &&
    sudo mkdir -p /srv/data/gemini/content &&
    sudo cp -rv gemini /srv/data/gemini/content/bobignou.red &&
    sudo ln -s /srv/data/gemini/content/bobignou.red /srv/data/gemini/content/gemini.bobignou.red

