#!/bin/bash

if [[ "$1" == "--exec" ]]; then
    status=$(playerctl status -p spotify)
    if [[ "$(echo $?)" -eq 0 ]]; then
        echo "$(playerctl metadata --format='{{ title }}' -p spotify)"
    else
        echo "Spotify"
    fi
elif [[ "$1" == "--play-pause" ]]; then
    if pgrep -x "spotify" > /dev/null; then
        playerctl play-pause
    else
        spotify &
    fi
elif [[ "$1" == "--next" ]]; then
	playerctl next -p spotify
elif [[ "$1" == "--prev" ]]; then
	playerctl previous -p spotify
elif [[ "$1" == "--seek-forward" ]]; then
	playerctl position 3+ -p spotify
elif [[ "$1" == "--seek-backward" ]]; then
	playerctl position 3- -p spotify
fi