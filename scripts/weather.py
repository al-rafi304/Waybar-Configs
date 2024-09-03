import requests
import json
from datetime import datetime
from waybarColors import Color
import os


colors = Color(os.path.expanduser("~/.config/waybar/mocha.css")).get_colors()

weather_icons = {
    # WMO Code, Night Icon, Day Icon, Info
    1: {'night':'', 'day':'', 'color': colors['yellow'], 'info':'Sunny'},
    0: {'night':'', 'day':'', 'color': colors['yellow'], 'info':'Sunny'},
    2: {'night':'', 'day':'', 'color': colors['sky'], 'info':'Partly Clouded'},
    3: {'night':'', 'day':'', 'color': colors['blue'], 'info':'Cloudy'},
    45: {'night':'', 'day':'󰖑', 'color': colors['subtext1'], 'info':'Foggy'},
    48: {'night':'', 'day':'󰖑', 'color': colors['subtext1'], 'info':'Rime Fog'},
    51: {'night':'', 'day':'', 'color': colors['blue'], 'info':'Light Drizzle'},
    53: {'night':'', 'day':'', 'color': colors['blue'], 'info':'Drizzle'},
    55: {'night':'', 'day':'', 'color': colors['blue'], 'info':'Heavy Drizzle'},
    61: {'night':'', 'day':'󰖗', 'color': colors['teal'], 'info':'Light Rain'},
    63: {'night':'', 'day':'', 'color': colors['teal'], 'info':'Rain'},
    65: {'night':'', 'day':'', 'color': colors['teal'], 'info':'Heavy Rain'},
    80: {'night':'', 'day':'', 'color': colors['sky'], 'info':'Light Showers'},
    81: {'night':'', 'day':'', 'color': colors['sky'], 'info':'Showers'},
    82: {'night':'', 'day':'', 'color': colors['sky'], 'info':'Heavy Showers'},
    95: {'night':'', 'day':'󰖓', 'color': colors['mauve'], 'info':'Thunderstorm'},
    96: {'night':'', 'day':'', 'color': colors['mauve'], 'info':'Light Hail Thunderstorm'},
    99: {'night':'', 'day':'', 'color': colors['mauve'], 'info':'Hail Thunderstorm'},
    'null': {'night':'󰖐', 'day':'󰖐', 'color': colors['overlay0'], 'info':'Unknown'}
}

def temp_color(temp):
    if temp > 33:
        return colors['red']
    elif temp >= 30:
        return colors['yellow']
    elif temp >= 27:
        return colors['flamingo']
    elif temp >= 23:
        return colors['teal']
    elif temp >= 20:
        return colors['sky']
    else:
        return colors['blue']

def main():
    try:
        url = "https://api.open-meteo.com/v1/forecast?latitude=23.6850&longitude=90.3563&current=temperature_2m,precipitation,rain,weather_code,wind_speed_10m,wind_direction_10m&hourly=temperature_2m,precipitation_probability,weather_code,is_day&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        response = requests.get(url)
    except:
        o = {"text": "󰖐 Offline"}
        print(json.dumps(o))
        return

    data = response.json()

    current_hour = int(datetime.now().strftime("%H"))
    is_day = 'day' if int(data['hourly']['is_day'][current_hour]) == 1 else 'night'
    weather_code = data['current']['weather_code']
    weather_code = weather_code if weather_code in weather_icons.keys() else 'null'
    weather_temp = data['current']['temperature_2m']
    weather_icon = weather_icons[weather_code][is_day]
    rain_prcnt = data['hourly']['precipitation_probability'][current_hour]
    temp_min = round(data['daily']['temperature_2m_min'][0])
    temp_max = round(data['daily']['temperature_2m_max'][0])
    hourly_temp = []
    hourly_code = []
    hourly_icon = []
    hourly_colors = []
    hourly_rain = []
    hours_12 = []

    for i in range(1, 6):
        nth_code = data['hourly']['weather_code'][current_hour+i]
        nth_temp = data['hourly']['temperature_2m'][current_hour+i]
        nth_rain = data['hourly']['precipitation_probability'][current_hour+i]
        nth_hour = (current_hour+i) % 24
        hourly_temp.append(round(nth_temp))
        hourly_code.append(nth_code)
        hourly_rain.append(nth_rain)
        hourly_icon.append(weather_icons[int(nth_code)][is_day]) 
        hourly_colors.append(weather_icons[int(nth_code)]['color'])
        hours_12.append(datetime.strptime(str(nth_hour), "%H").strftime("%-I%p"))




    tooltip_text = str.format(
        "{} \n{} \n{} \n{} \n\n{}\t{}\t{}\t{}\t{} \n{}\t{}\t{}\t{}\t{} \n{}\t{}\t{}\t{}\t{}",
        f'<span foreground="{colors['rosewater']}" size="large">{weather_temp}°C</span>',
        f'<span foreground="{colors['text']}">{weather_icons[weather_code]['info']}</span> <span foreground="{weather_icons[weather_code]['color']}" size="x-large">{weather_icon}</span> ',
        f'<span foreground="{colors['text']}">Rain:</span> <span foreground="{colors['blue'] if int(rain_prcnt)>=40 else colors['text']}"><span size="small">󰖌</span>{rain_prcnt}%</span>',
        f'<span foreground="{colors['text']}" size="smaller">H:{temp_max}° L:{temp_min}°</span>',
        f'<span foreground="{colors['text']}" size="small">{hours_12[0]}</span>',
        f'<span foreground="{colors['text']}" size="small">{hours_12[1]}</span>',
        f'<span foreground="{colors['text']}" size="small">{hours_12[2]}</span>',
        f'<span foreground="{colors['text']}" size="small">{hours_12[3]}</span>',
        f'<span foreground="{colors['text']}" size="small">{hours_12[4]}</span>',
        f'<span foreground="{hourly_colors[0]}" size="xx-large">{hourly_icon[0]}</span>' + (f'<span foreground="{colors["blue"]}" size="small"> 󰖌{hourly_rain[0]}%</span>' if hourly_rain[0] >= 40 else ''),
        f'<span foreground="{hourly_colors[1]}" size="xx-large">{hourly_icon[1]}</span>' + (f'<span foreground="{colors["blue"]}" size="small"> 󰖌{hourly_rain[1]}%</span>' if hourly_rain[1] >= 40 else ''),
        f'<span foreground="{hourly_colors[2]}" size="xx-large">{hourly_icon[2]}</span>' + (f'<span foreground="{colors["blue"]}" size="small"> 󰖌{hourly_rain[2]}%</span>' if hourly_rain[2] >= 40 else ''),
        f'<span foreground="{hourly_colors[3]}" size="xx-large">{hourly_icon[3]}</span>' + (f'<span foreground="{colors["blue"]}" size="small"> 󰖌{hourly_rain[3]}%</span>' if hourly_rain[3] >= 40 else ''),
        f'<span foreground="{hourly_colors[4]}" size="xx-large">{hourly_icon[4]}</span>' + (f'<span foreground="{colors["blue"]}" size="small"> 󰖌{hourly_rain[4]}%</span>' if hourly_rain[4] >= 40 else ''),
        f'<span foreground="{temp_color(hourly_temp[0])}" size="small">{hourly_temp[0]}°C</span>',
        f'<span foreground="{temp_color(hourly_temp[1])}" size="small">{hourly_temp[1]}°C</span>',
        f'<span foreground="{temp_color(hourly_temp[2])}" size="small">{hourly_temp[2]}°C</span>',
        f'<span foreground="{temp_color(hourly_temp[3])}" size="small">{hourly_temp[3]}°C</span>',
        f'<span foreground="{temp_color(hourly_temp[4])}" size="small">{hourly_temp[4]}°C</span>'
    )

    output_icon = f'<span foreground="{weather_icons[weather_code]['color']}" size="x-large">{weather_icon}</span>'
    output_temp = f'<span foreground="{temp_color(round(weather_temp))}">{round(weather_temp)}°C</span>'
    output_rain = f'<span foreground="{colors['blue'] if int(rain_prcnt)>=40 else colors['text']}"><span size="small">󰖌</span>{rain_prcnt}%</span>'
    output = {
        "text": f'{output_icon} {output_temp}',
        "tooltip": tooltip_text,
        "alt": f'{output_rain}'
    }

    # print(json.dumps({"text": "lol"}))
    print(json.dumps(output))

main()