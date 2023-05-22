#!/bin/bash
if ! command -v python &> /dev/null ; then
    echo "command 'python' could not be found";

python -m pip freeze > requirements.txt
