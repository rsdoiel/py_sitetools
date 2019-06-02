#!/usr/bin/env python3
#
# boutique.py is an example of a "boutique" static site generator
# built on py_sitetools and py_dataset.
#

# Import our python packages
import os
import sys
import json
from py_dataset import dataset
from py_sitetools import mkpage, frontmatter, version_no, Logger

log = Logger(os.getpid())

# Minimal configuration
docs_dir = "docs"
site_dir = "htdocs"
c_name = "boutique.ds"
index_tmpl = "templates/index.tmpl"

# Create our boutique.ds if required
if os.path.exists("boutique.ds") == False:
    dataset.init("boutique.ds")

# crawl docs_dir and ingest files into data collection.
for path, folders, files in os.walk(docs_dir):
    #log.print(f"Processing {path}")
    for filename in files:
        if filename.endswith(".md"):
            f_name = os.path.join(path, filename)
            log.print(f"Ingesting {f_name}")
            metadata = frontmatter(f_name)
            with open(f_name) as f:
                src = f.read()
            if "id" in metadata:
                key = str(metadata["id"])
                if dataset.has_key(c_name, key):
                    err = dataset.update(c_name, key, { "metadata": metadata, "content": f_name, "src": src})
                else:
                    err = dataset.create(c_name, key, { "metadata": metadata, "content": f_name, "src": src})
                if err != "":
                    log.fatal(err)
            else:
                log.print(f"Warning, no front matter for {f_name}")

# for each dataset record render appropriate HTML pages
keys = dataset.keys(c_name)
for key in keys:
    page, err = dataset.read(c_name, key)
    if err != "":
        log.print(f"WARNING: could not read {key} from {c_name}, skipping")
    if 'output' in page['metadata']:
        p = page['metadata']['output']
        f_name = os.path.join(site_dir, p)
        d_name = os.path.join(site_dir, os.path.dirname(p))
        if os.path.exists(d_name) == False:
            os.makedirs(d_name, exist_ok = True)
        page_data = [
            f"content={page['content']}",
            f"front_matter=json:{json.dumps(page['metadata'])}",
        ]
        err = mkpage(f_name, [ "templates/page.tmpl" ], page_data)
        if err != "":
            log.fatal(f"Failed ({key}) {f_name}, {err}");
        else:
            log.print(f"Wrote {f_name}")

# Write out log message showing version of mkpage, frontmatter
# and dataset used.
print("Built using", end = " ")
for i, app_name in enumerate([ "mkpage", "frontmatter", "dataset" ]):
    version = version_no(app_name).strip()
    if i == 2:
        print(" and", end = " ")
    elif i > 0:
        print(",", end = " ")
    print(f"{version}", end = "")
print("")

