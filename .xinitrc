[[ -f ~/.Xresources ]] && xrdb -merge ~/.Xresources

#exec i3 --shmlog-size=26214400
exec qtile start
