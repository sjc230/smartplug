#!/bin/bash
clear
PYTHON=$(which python3)
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
# #echo "Script path: $SCRIPTPATH"
# now="$(date +'%d/%m/%Y %T')"

# SERVICE="$SCRIPTPATH/spp_tools.py"
SERVICE="$SCRIPTPATH/remote_control.py"

cd $SCRIPTPATH

$PYTHON $SERVICE

