#!/usr/bin/env python3

import markdown
import shutil
import yaml
import os

# ------------------------------- Documentation ------------------------------ #

"""
Markdown files should either be standard markdown files or a file starting with
`---` which indicates the start of metadata. Those metadata will end with `---`.

The result will be put in a dictionary where the `body` key contains the text
of the markdown body and the `metadata` key contains a dictionary with all the
metadatas.
"""

# --------------------------------- Constants -------------------------------- #

HTLM_STYLE = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans&display=swap" rel="stylesheet"> 
<link rel="stylesheet" href='/static/style.css' />
"""

STATIC_DIR = "static"
SOURCE_DIR = "source"
TARGET_DIR = "public"

WEBSITE = "bobignou.red"
AUTHOR_NAME = "Maxime Bouillot"

# --------------------------------- Renderer --------------------------------- #

def render_body(md):
    "Renders the body of a markdown file into the body of an HTML file"
    ret = f'<h1>{md["metadata"]["title"]}</h1>\n'
    ret += markdown.markdown(md["body"], extensions=["tables", "extra"])
    return ret

def render_head(md):
    """Generates the HTML header of a markdown document."""
    ret = '<meta charset="utf-8">\n'
    ret += HTLM_STYLE
    title = md["metadata"]["title"]
    ret += "<title>" + title + "</title>\n"
    desc = f'<meta name="description" content="{md["body"][0:50]}">'
    return ret

def render_page(md):
    """Render the whole HTML page from a markdown document."""
    ret = "<!DOCTYPE html>\n<html>\n<head>\n"
    ret += render_head(md)
    ret += "</head>\n<body>\n"
    ret += render_body(md)
    ret += "</body>\n</html>\n"
    return ret

def extract_md(filename):
    """Gets the body and the metadata of a markdown document based on its
    file name."""
    with open(filename, "r") as f:
        txt = f.read()
        if len(txt) > 6:
            if txt[0:3] == "---":
                end_metadata = txt.find("---", 3)
                meta = txt[3:end_metadata]
                return {
                        "metadata": yaml.safe_load(meta),
                        "body": txt[end_metadata+3:]
                    }
        return {
                "metadata": {},
                "body": txt
            }

# ------------------------------ Managing posts ------------------------------ #

def list_posts():
    """List all the names of posts. Put them in a dictionary with their date
    and name"""
    ret = []
    for path in os.listdir(f"{SOURCE_DIR}/posts"):
        if path[-3:] == ".md":
            name = path[:-3]
            md = extract_md(f"{SOURCE_DIR}/posts/{path}")
            date = md["metadata"]["date"]
            ret.append({
                "name": name,
                "date": date,
                "path": f"{SOURCE_DIR}/posts/{path}",
                })
    return ret

def sort_post(posts):
    """Sort by date the list of posts."""
    def k(p):
        return p["date"]
    posts.sort(key=k)

def make_post_table(posts):
    """From the list of posts, makes a HTML div table with all of them."""
    sort_post(posts)
    posts.reverse()
    # md
    md = "| | |\n|-|-|\n"
    for post in posts:
        md += f"|[{str(post['date']).split(' ')[0]}](posts/{post['name']}.html)|[{post['name'].replace('-', ' ')}](posts/{post['name']}.html)|\n"
    # HTML
    ret = '<div class="post_list">\n'
    ret += markdown.markdown(md, extensions=["tables", "extra"])
    ret += '</div>\n'
    return ret

def fix_internals_path(html_txt, prefix):
    """On all path not prefixed found in the input HTML, add the given
    prefix."""
    all_slices = html_txt.split(' src="')
    ret = all_slices[0]
    for i in range(1, len(all_slices)):
        ret += ' src="'
        slice = all_slices[i]
        link = slice.split('"')[0]
        if link.find("/") < 0: # Not a full link
            ret += prefix
        ret += slice
    return ret

# --------------------------------- Atom feed -------------------------------- #

def make_atom_entry(md):
    """From a post dictionary, makes the atom entry."""
    summary = ""
    for line in md["body"].split("\n"):
        if len(line) > 1 and line[0] != "#":
            summary = line
            break
    link = f"https://{WEBSITE}/posts/{md['metadata']['title']}.html".replace(" ", "-")
    ret = "<entry>\n"
    ret += f'<id>{link}</id>\n'
    ret += f'<link href="{link}"/>\n'
    ret += f'<title>{md["metadata"]["title"]}</title>\n'
    ret += f'<updated>{str(md["metadata"]["date"]).replace(" ", "T")}</updated>\n'
    ret += f'<dc:date>{str(md["metadata"]["date"]).replace(" ", "T")}</dc:date>\n'
    ret += f'<summary type="html">{summary}</summary>\n'
    ret += f'</entry>\n'
    return ret

def make_atom_feed():
    """Make the whole atom feed.""" 
    posts = list_posts()
    sort_post(posts)
    posts.reverse()

    ret =  '''<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
xmlns:dc="http://purl.org/dc/elements/1.1/">\n'''
    ret += f'<title>{WEBSITE}</title>\n'
    ret += f'<author><name>{AUTHOR_NAME}</name></author>\n'
    ret += f'<id>https://{WEBSITE}/atom.xml</id>\n'
    ret += f'<updated>{str(posts[0]["date"]).replace(" ", "T")}</updated>\n'
    ret += f'<dc:date>{str(posts[0]["date"]).replace(" ", "T")}</dc:date>\n'
    for post in posts:
        md = extract_md(post['path'])
        ret += make_atom_entry(md)
    ret += f'</feed>\n'
    return ret

# ----------------------------------- Main ----------------------------------- #

def make_website():
    """Renders the whole website."""
    try:
        shutil.rmtree(TARGET_DIR)
    except FileNotFoundError:
        pass
    os.mkdir(TARGET_DIR)
    try:
        shutil.copyfile(f"{STATIC_DIR}/favicon.ico", f"{TARGET_DIR}/favicon.ico")
    except FileNotFoundError:
        pass
    shutil.copytree(STATIC_DIR, f"{TARGET_DIR}/static")
    index = extract_md(f"{SOURCE_DIR}/index.md")
    index["body"] = make_post_table(list_posts()) + index["body"]
    with open(f"{TARGET_DIR}/index.html", "w") as f:
        f.write(render_page(index))
    os.mkdir(f"{TARGET_DIR}/posts")
    for post in list_posts():
        with open(f"{TARGET_DIR}/posts/{post['name']}.html", "w") as f:
            md = extract_md(post['path'])
            md['body'] += "[Back to homepage](/)\n"
            f.write(fix_internals_path(render_page(md), f"/posts/{post['name']}/"))
        try:
            shutil.copytree(f"{SOURCE_DIR}/posts/{post['name']}", f"{TARGET_DIR}/posts/{post['name']}")
        except FileNotFoundError:
            pass
    with open(f"{TARGET_DIR}/atom.xml", "w") as f:
        f.write(make_atom_feed())

if __name__ == "__main__":
    make_website()

