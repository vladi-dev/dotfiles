#!/usr/bin/env sh

exec 1>/tmp/autostart.log 2>&1

runCommand() {
    pkill "$(echo "$@" | cut -d ' ' -f 1)"
    ("$@" > /tmp/"$1.log" 2>&1) &
}

runCommand feh --bg-scale ~/Pictures/Wallpapers/wall.png
runCommand conky
runCommand dunst
