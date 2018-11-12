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
$tmux send-keys 'cd /home/pi/vscode_scripts/dash' C-m
$tmux send-keys './app.py' C-m
$tmux split-window  -h -t $SESSION:0
$tmux send-keys 'cd /home/pi/vscode_scripts/mqtt' C-m
$tmux send-keys 'python3 mqttinfoscraper.py' C-m
$tmux split-window  -h -t $SESSION:0
$tmux send-keys 'cd /home/pi/vscode_scripts/mqtt; python3 mqttdatatoinfluxdb.py' C-m
$tmux new-window    -t $SESSION:1 
$tmux new-window    -t $SESSION:2  
$tmux new-window    -t $SESSION:3  
$tmux split-window  -h -t $SESSION:3
$tmux new-window    -t $SESSION:4
$tmux select-window -t $SESSION:0
$tmux attach -t $SESSION