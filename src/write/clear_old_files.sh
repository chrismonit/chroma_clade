#!/bin/bash

# remove files in with timestamp older than 24 hours
# assuming the following directory structure:
# .
# ├── align
# │   └── README
# ├── clear_old_files.sh
# ├── output
# │   └── README
# └── tree
#     └── README

# find directory of this script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

# delete files with timestamp older than 24 hours, except README files
find $DIR/align $DIR/tree $DIR/output -type f -mmin +$((60*24)) ! -name README -exec rm {} \;

