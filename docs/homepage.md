+++
id = 1
output = "index.html"
title = "Oq, a 'boutique' generated site",
creators = [ "R. S. Doiel" ]
pub_date = "2019-06-01",
byline = "By Almost Anonymous"
+++

[Home](/) | [Two](/two/) | [Three](/three/)

### a "boutique.py" overview

This is a demo of using [mkpage]() to process Markdown documents 
with frontmatter. Three types of front matter are supported JSON,
TOML and YAML. The front matter in this demo is used to 
to generate a static website with 
`boutique.py` using [py_sitetools](https://github.com/rsdoiel/py_sitetools)and [py_dataset](https://github.com/caltechlibrary/py_dataset).

This file was create in "docs/homepage.md" but gets rendered to
[index.html](/) in the site directory folder. The front matter
was written in TOML. The template will should the JSON version of
the front matter as py_sitetools converts each front matter format
to JSON before rendering to a Python 3 Dict.

