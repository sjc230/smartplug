#!/bin/bash
clear
PYTHON=$(which python3)
SCRIPTPATH="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"
#echo "Script path: $SCRIPTPATH"
now="$(date +'%d/%m/%Y %T')"

# SERVICE="$SCRIPTPATH/spp_tools.py"
SERVICE="$SCRIPTPATH/mqtt_to_influx.py"
LOG="log.txt"
process=$(pgrep -f "$SERVICE")
process=${process[0]}
#echo "the process ID of $mac is $process"

if [[ ! -z $process ]]
then
    echo "$SERVICE is running at $now"
else
#    echo "$SERVICE stopped at $now, restart!"
#    echo "$SERVICE stopped at $now, restart!" >> $SCRIPTPATH/$LOG
    cd $SCRIPTPATH
    #nohup $PYTHON $SERVICE &
    $PYTHON $SERVICE
fi
