
# py_sitetools

This Python 3 package wraps Caltech Library's 
[mkpage](https://github.com/caltechlibrary/mkpage) (v0.0.26) 
command line tools for building light weight boutique static
 site generators.

## Example boutique static site generator

At less than 80 lines of Python [boutique.py](boutique.py) 
is an example of how easy it is to make a content management
system building on 
[py_dataset](https://github.com/caltechlibrary/py_dataset), 
and py_sitetools. 

Boutique reads a "docs" folder for Markdown files, ingests them
into a dataset collection called "boutique.ds". Each markdown
file is expected to have a JSON front matter section with the
following fields--

+ id (any unique string)
+ title (title of page)
+ creators (an array of strings of author names)
+ byline (a single string used as a byline)
+ pub_date (date of publication)
+ output the filename and path to render to relative to the site root

On ingest the front matter is separate from the markdown document 
creating a record structure like

```json
    {
        "metadata": { ... },
        "content" : PATH_TO_MARKDOWN_DOC
    }
```

This will get saved in the dataset collection named "boutique.ds".

After page ingest the collection content is iterated over creating
the described pages in the "htdocs" folder identified in the 
_boutique.py_ program as **site_dir**. The layout of the website
is idependent of the contents of the docs directory. Each page
identifies explicitly where it will be published to.

The whole Python 3 script for _boutique.py_ is about 80 lines, the whole
**py_sitetools** is under 200 (including boutque.py).


