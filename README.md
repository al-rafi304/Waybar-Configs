![1725125124(08-31-24)](https://github.com/user-attachments/assets/9cabbd80-a8ff-4dc3-962a-7bd784d91ada)
![image](https://github.com/user-attachments/assets/9ac2464a-1953-45e5-af0f-6a80651eb288)
![image](https://github.com/user-attachments/assets/38bc3b6b-dc3f-4e9d-a631-b926d4185358)
![1725125192(08-31-24)](https://github.com/user-attachments/assets/0e782ce1-6479-44cf-a752-77ca6e0df536)

# About
These are my waybar configuration files that includes custom modules and Catppuccin color theme. It's highly depended on rofi and rofi themes. 
Modules:
- **Weather**: Fetches data from [Open Meteo](https://open-meteo.com/en/docs) API and displays detailed information in the tooltip. Colors and icons dynamically change depending on weather type and temperature. *Note: Make sure to change location in weather.py file*
- **VPN**: Displays Rofi's dmenu to choose from configured VPNs and shows status of connection. *Note: Make sure to configure VPN profiles in NetworkManager and the VPN scripts*
- **Spotify**: Displays currently playing song and includes mouse controls for interating with media
- **Launcher**: Launches specific apps which can be selected by scrolling. Rofi launcher is default.
- **Default modules**: Workspaces, CPU, Memory, Disk, Clock, Pulseaudio, network, network speed (modifying nework module)

# Requirements
[Rofi](https://github.com/davatorium/rofi) for displaying prompt menues. (*Note: Not tested on [rofi-wayland](https://archlinux.org/packages/extra/x86_64/rofi-wayland/), I'm setting window mode to floating for rofi on Hyprland* )
```
sudo pacman -S rofi
```
Rofi themes from [adi1090x/rofi](https://github.com/adi1090x/rofi) are used for custom rofi menus  
```
git clone --depth=1 https://github.com/adi1090x/rofi.git
cd rofi
chmod +x setup.sh
./setup.sh
```
[NetworkManger](https://wiki.archlinux.org/title/NetworkManager) needs to be installed if not already present

```
sudo pacman -S networkmanager
```

# Installation
Clone the repo and move everything to `.config/waybar` file
```
git clone git@github.com:al-rafi304/Waybar-Configs.git
mv Waybar-Configs/* .config/waybar/
```

### Fonts
 - Install JetBrains fonts 
	```
	sudo pacman -S ttf-jetbrains-mono
	sudo pacman -S ttf-jetbrains-mono-nerd
	```
 - Download `NerdFontsSymbolsOnly.zip`
	```
	curl -L -o NerdFontsSymbolsOnly.zip https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/NerdFontsSymbolsOnly.zip
	```
 - Extract it to fonts file `/usr/share/fonts/TTF`
   ```
   sudo unzip NerdFontsSymbolsOnly.zip -d /usr/share/fonts/TTF -x LICENSE README.md
   ```

### VPN Setup
Currently the VPN module contains two VPNs: [CloudflareWarp](https://aur.archlinux.org/packages/cloudflare-warp-bin) and [OpenVPN](https://wiki.archlinux.org/title/OpenVPN) (using Proton VPN profile). You can change/modify/remove any of these with your preferred choices.
 - Install CloudflareWarp
	```
	yay -S cloudflare-warp-bin
	```
 - Installing OpenVPN plugin for NetworkManager
	```
	sudo pacman -S networkmanager-openvpn
	```
 - Import OpenVPN configuration file to NetworkManager
	```
	nmcli connection import type openvpn file /path/to/your/config.ovpn
	```
 - Set up authentication
   ```
   nmcli connection modify your_connection_name +vpn.data "username=your_username"
   nmcli connection modify your_connection_name +vpn.secrets "password=your_password"
   ```

### Change Weather Locatin
Just update the *latitude* and *longitude* with your location's in [`scripts/weather.py`](https://github.com/al-rafi304/Waybar-Configs/blob/46ff5a3c197ed42a5d8f59695fe901696d63f81f/scripts/weather.py#L49 ) file's `url` variable

### Changing Color Scheme
It's currently using [Catppuccin's](https://github.com/catppuccin/waybar) *Mocha* color theme is used which can also be changed just by replacing the `mocha.css` file with another css file and import it in `style.css`. **Do not change the color names** in the css file containing colors
