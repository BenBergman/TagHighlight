#!/usr/bin/python
from __future__ import print_function

import os
import zipfile
import fnmatch

vimfiles_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))

# Recursive glob function, from
# http://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python#2186565
def Rglob(path, match):
    matches = []
    for root, dirnames, filenames in os.walk(path):
        for filename in fnmatch.filter(filenames, match):
            matches.append(os.path.join(root, filename))
    return matches

# List of paths to include (either explicit files or paths to search)
paths = {
        '.py': ['plugin/TagHighlight',__file__],
        '.vim': ['plugin/tag_highlight.vim','autoload/TagHighlight'],
        '.txt': ['plugin/TagHighlight/data','plugin/TagHighlight/instructions.txt'],
        '.spec': ['plugin/TagHighlight/TagHighlight.spec'],
        }

# Create the zipfile
zipf = zipfile.ZipFile(os.path.join(vimfiles_dir,'dist','taghighlight.zip'), 'w')

# Collect the specified paths into a zip file
for ext, pathlist in paths.items():
    for path in pathlist:
        # Get the full path (specified relative to vimfiles directory)
        full_path = os.path.join(vimfiles_dir, path)
        if os.path.exists(full_path):
            if os.path.isfile(full_path):
                files = [full_path]
            elif os.path.isdir(full_path):
                files = Rglob(full_path, '*' + ext)
            else:
                print("Unrecognised path: " + full_path)

            if len(files) > 0:
                for f in files:
                    dirname = os.path.dirname(os.path.relpath(f,vimfiles_dir))
                    zipf.write(f,os.path.join(dirname, os.path.basename(f)), zipfile.ZIP_DEFLATED)
            else:
                print("No files found for path: " + full_path)
        else:
            print("Path does not exist: " + full_path)
# Close the zipfile
zipf.close()
