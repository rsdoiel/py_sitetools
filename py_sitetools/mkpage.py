#
# mkpage.py is an internal package wrapping the mkpage set of command
# line utilities found at https://github.com/caltechlibrary/mkpage.
#
import os
import sys
import json
from subprocess import Popen, PIPE, run

from .logger import Logger

log = Logger(os.getpid())

#
# mkpage wrapes the mkpage command from mkpage
# @param output_filename is the output file
# @param templates is an array of Go style templates
# @data is a dict structure that will be passed into mkpage as JSON
#
def mkpage(output_filename, templates = [], data = []):
    cmd = ['mkpage', '-o', output_filename]
    for item in data:
        cmd.append(item)
    for tmpl in templates:
        cmd.append(tmpl)
    print(f"DEBUG cmd -> {' '.join(cmd)}")
    with Popen(cmd, stdout = PIPE, stderr = PIPE) as proc:
        err = proc.stderr.read().strip().decode('utf-8')
        if err != '':
            log.print(f"{' '.join(cmd[0:3])} error: {err}")
            return err
        out = proc.stdout.read().strip().decode('utf-8')
        if out != "":
            log.print(f"{out}");
    return ""

#
# frontmatter extracts front matter from a Markdown document
# returning the results as a python dictionary. Currently
# supports only JSON style front matter.
#
# @param input_filename is the Markdown file containing front matter
# @return a Python dict of the front matter found or an empty dict
# if none found.
#
def frontmatter(input_filename):
    cmd = ['frontmatter', '-i', input_filename]
    src = ''
    with Popen(cmd, stdout = PIPE, stderr = PIPE) as proc:
        err = proc.stderr.read().strip().decode('utf-8')
        if err != '':
            log.print(f"{' '.join(cmd[0:3])} error: {err}")
        out = proc.stdout.read().strip().decode('utf-8')
        if (out.startswith("{") and out.endswith("}")) or (out.startswith("[") and out.endswith("]")):
            try:
                result = json.loads(out.encode('utf-8'))
            except Exception as e:
                log.fatal(f"Warning {input_filename} has invalid metadata")
            return result
        elif out != "":
            log.print(f"WARNING: Front matter isn't JSON for {input_filename}, {out}")
    return {}

#
# version_no shows the version number of mkpage cli referenced.
#
# @param cli_name either mkpage or frontmatter
# @return version number found or system exit with error
#
def version_no(cli_name):
    # FIXME: command[0] might need a .exe extension on Windows 10?
    cmd = [cli_name, '-version']
    p = Popen(cmd, stdout = PIPE, stderr = PIPE)
    (version, err) = p.communicate()
    if err.decode('utf-8') != '':
        log.fatal(f"ERROR: {cli_name} -version, {err.decode('utf-8')}")
        sys.exit(1)
    return version.decode('utf-8')

