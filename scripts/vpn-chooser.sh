#!/bin/bash

# Checking internet connectivity
if ping -c 1 8.8.8.8 &>/dev/null; then

	status_file="/tmp/vpn_status"
	vpn_interfaces=("tun0" "CloudflareWARP")
	current_interface="init"
	vpn_connected=false
	vpn_ip=""

	# Check for active VPN interfaces and retrieve the IP address
	for iface in "${vpn_interfaces[@]}"; do
		iface_status=$(ip link show "$iface" 2>/dev/null | grep -oP "(?<=state )\w+")
		if [ "$iface_status" = "UP" ] || [ "$iface_status" = "UNKNOWN" ]; then
			vpn_connected=true
			vpn_ip=$(ip -4 addr show "$iface" | grep -oP "(?<=inet\s)\d+(\.\d+){3}")
			current_interface="$iface"
			break
		fi
	done


	# Define the prompt options

	if [ "$vpn_connected" = true ]; then
		CHOICE=$(echo -e "CloudflareWarp\nProtonVPN\nDisconnect" | rofi -dmenu -p "Choose VPN:" -theme ~/.config/rofi/launchers/type-1/style-11.rasi)
	else
		CHOICE=$(echo -e "CloudflareWarp\nProtonVPN" | rofi -dmenu -p "Choose VPN:" -theme ~/.config/rofi/launchers/type-1/style-11.rasi)
	fi

	#CHOICE=$(echo -e "Warp\nOpenVPN\nDisconnect" | rofi -dmenu -p "Choose VPN:" -theme .config/openbox/themes/default/rofi/networkmenu.rasi)

	# Check the user's choice and execute the corresponding command
	case "$CHOICE" in
		CloudflareWarp)
			# Replace with your Warp connection command
			echo "connecting" > $status_file
			# Example command to connect to Warp
			warp-cli connect
			;;
		ProtonVPN)
			# Replace with your OpenVPN connection command
			echo "connecting" > $status_file
			# Example command to connect to OpenVPN
			#sudo openvpn --config ~/protonVPN.ovpn
			nmcli connection up ProtonVPN || echo "disconnected" > /tmp/vpn_status
			;;
		Disconnect)
			
			if [ "$current_interface" = "CloudflareWARP" ]; then
				echo "Disconnecting Warp..."
				warp-cli disconnect && echo "disconnected" > $status_file
			elif [ "$current_interface" = "tun0" ]; then
				echo "Disconnecting OpenVPN..."
				#sudo pkill -f openvpn
				nmcli connection down ProtonVPN && echo "disconnected" > $status_file
				
			fi
			;;
		*)
			echo "No valid choice made."
			;;
	esac
#else
#	rofi -e "No internet connection!"
fi
