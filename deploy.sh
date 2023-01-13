#!/bin/sh

# Web
./renderer.py &&
    sudo /bin/rm -rfv /srv/data/www/blog/* &&
    sudo cp -rv public/* /srv/data/www/blog/ &&
    echo Done

# Gemini
sudo /bin/rm -rfv /srv/data/gemini/content &&
    sudo mkdir -p /srv/data/gemini/content &&
    sudo cp -rv gemini /srv/data/gemini/content/bobignou.red &&
    sudo ln -s /srv/data/gemini/content/bobignou.red /srv/data/gemini/content/gemini.bobignou.red

# Gemini atom and post list
sed 's|https://|gemini://|g; s:\.html:.gmi:g; s:html:text:g;' < public/atom.xml | sudo tee  /srv/data/gemini/content/bobignou.red/atom.xml
printf '# Posts\n\n' | sudo tee /srv/data/gemini/content/bobignou.red/posts/index.gmi
grep "=> posts" < gemini/index.gmi | sed 's:=> posts/:=> :' | sudo tee -a /srv/data/gemini/content/bobignou.red/posts/index.gmi

