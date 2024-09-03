#!/bin/bash

# List of common VPN interfaces, adjust as necessary
vpn_interfaces=("tun0" "CloudflareWARP")

vpn_icon_connected="󰴳"  # Icon for connected VPN2
vpn_icon_disconnected="󰦜 VPN"  # Icon for disconnected VPN
vpn_icon_connecting="󱆢 Connecting..."  # Icon for connecting VPN

vpn_connected=false
vpn_ip=""

status_file="/tmp/vpn_status"
status="disconnected"
# Read the connection status from the status file
if [ -f $status_file ]; then
    status=$(cat $status_file)
fi

if [ "$status" = "connecting" ]; then
    echo "{\"text\": \"$vpn_icon_connecting\", \"class\": \"connecting\"}"
fi

# Check for active VPN interfaces and retrieve the IP address
for iface in "${vpn_interfaces[@]}"; do
    iface_status=$(ip link show "$iface" 2>/dev/null | grep -oP "(?<=state )\w+")
    if [ "$iface_status" = "UP" ] || [ "$iface_status" = "UNKNOWN" ]; then
        vpn_connected=true
        vpn_ip=$(ip -4 addr show "$iface" | grep -oP "(?<=inet\s)\d+(\.\d+){3}")
        break
    fi
done

# Output the appropriate icon and IP address based on VPN connection status
if [ "$vpn_connected" = true ]; then
    echo "connected" > $status_file
    echo "{\"text\": \"$vpn_icon_connected $vpn_ip\", \"class\": \"connected\"}"
else
    echo "{\"text\": \"$vpn_icon_disconnected\", \"class\": \"disconnected\"}"
fi