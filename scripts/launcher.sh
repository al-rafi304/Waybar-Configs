
app_list=("launcher" "firefox" "xfce4-terminal" "thunar")
app_icon=("" "" "" "")

index_file="/tmp/launch_idx"
icon_file="/tmp/launch_icon"

if [ -e "$index_file" ];then
	index="$(cat "$index_file")"
else
	index=0
	echo "0" > "$index_file"
fi

current_app=${app_list[index]}
current_icon=${app_icon[index]}

if [ ! -e "$icon_file" ];then
	echo $current_icon > $icon_file
fi

cycle_apps() {
	index=$(( (index + 1) % ${#app_list[@]} ))
	echo "$index" > "$index_file"
	current_app="$app_list["$index"]"
	echo "$index"
}

update_icons() {
	current_icon=${app_icon[index]}
	echo $current_icon >> $icon_file

	#echo "{\"text\": \"$current_icon\", \"tooltip\": \"Launching $current_app\"}"
}

on_click() {
	if [ "$index" != "0" ];then
		$current_app
	else
		~/.config/rofi/launchers/type-1/launcher.sh
	fi
}


if [[ "$1" == "--exec" ]];then
	update_icons
elif [[ "$1" == "--click" ]]; then
	on_click
elif [[ "$1" == "--cycle" ]]; then
	cycle_apps && update_icons
fi