#!/usr/bin/env python3

import markdown
import yaml

HTLM_STYLE = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans&display=swap" rel="stylesheet"> 
<link rel="stylesheet" href='/static/style.css' />
"""

"""
Markdown files should either be standard markdown files or a file starting with
`---` which indicates the start of metadata. Those metadata will end with `---`.

The result will be put in a dictionary where the `body` key contains the text
of the markdown body and the `metadata` key contains a dictionary with all the
metadatas.
"""

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
    try:
        title = md["metadata"]["title"]
        ret += "<title>" + title + "</title>\n"
        desc = f'<meta name="description" content="{md["body"][0:50]}">'
    except:
        pass
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

# ----------------------------------- Main ----------------------------------- #

print(render_page(extract_md("source/index.md")))
