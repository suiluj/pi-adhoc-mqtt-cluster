#!/bin/bash
SESSION=main
tmux="tmux -2 -f tmux.conf"

# if the session is already running, just attach to it.
$tmux has-session -t $SESSION
if [ $? -eq 0 ]; then
       echo "Session $SESSION already exists. Attaching."
       sleep 1
       $tmux attach -t $SESSION
       exit 0;
fi

# create a new session, named $SESSION, and detach from it
$tmux new-session -d -s $SESSION
$tmux new-window    -t $SESSION:0 
$tmux send-keys 'cd /home/pi/vscode_scripts/mqtt' C-m
$tmux send-keys 'python3 testsensor.py'
$tmux split-window  -h -t $SESSION:0
$tmux send-keys 'cd /home/pi/vscode_scripts/mqtt' C-m
$tmux send-keys 'python3 mqttmcp3008sensor.py'
$tmux new-window    -t $SESSION:1 
$tmux attach -t $SESSION:0