#!/bin/bash

if [[ "$1" == "--exec" ]]; then
    status=$(playerctl status -p spotify 2>/dev/null)
    if [[ "$(echo $?)" -eq 0 ]]; then
        title=$(playerctl metadata --format='{{ title }}' -p spotify)
        tooltip=$(playerctl -p spotify metadata --format='{{ title }} - {{ artist }}')
        
        echo $(jq -n --arg text "$title" --arg tooltip "$tooltip" --arg class "playing" \
            '{text: $text, class: $class, tooltip: $tooltip}')
    else
        echo '{"text": "Spotify", "class": "stop"}'
    fi
elif [[ "$1" == "--play-pause" ]]; then
    if pgrep -x "spotify" >/dev/null; then
        playerctl play-pause -p spotify
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