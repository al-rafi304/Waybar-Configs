import requests
import json
from datetime import datetime
from waybarColors import Color
import os, sys


class Weather:
    def __init__(self):
        self.colors = Color(os.path.expanduser("~/.config/waybar/mocha.css")).get_colors()
        self.weather_icons = {
            # WMO Code, Night Icon, Day Icon, Info
            1: {'night':'', 'day':'', 'color': self.colors['yellow'], 'info':'Sunny'},
            0: {'night':'', 'day':'', 'color': self.colors['yellow'], 'info':'Sunny'},
            2: {'night':'', 'day':'', 'color': self.colors['sky'], 'info':'Partly Clouded'},
            3: {'night':'', 'day':'', 'color': self.colors['blue'], 'info':'Cloudy'},
            45: {'night':'', 'day':'󰖑', 'color': self.colors['subtext1'], 'info':'Foggy'},
            48: {'night':'', 'day':'󰖑', 'color': self.colors['subtext1'], 'info':'Rime Fog'},
            51: {'night':'', 'day':'', 'color': self.colors['blue'], 'info':'Light Drizzle'},
            53: {'night':'', 'day':'', 'color': self.colors['blue'], 'info':'Drizzle'},
            55: {'night':'', 'day':'', 'color': self.colors['blue'], 'info':'Heavy Drizzle'},
            61: {'night':'', 'day':'󰖗', 'color': self.colors['teal'], 'info':'Light Rain'},
            63: {'night':'', 'day':'', 'color': self.colors['teal'], 'info':'Rain'},
            65: {'night':'', 'day':'', 'color': self.colors['teal'], 'info':'Heavy Rain'},
            80: {'night':'', 'day':'', 'color': self.colors['sky'], 'info':'Light Showers'},
            81: {'night':'', 'day':'', 'color': self.colors['sky'], 'info':'Showers'},
            82: {'night':'', 'day':'', 'color': self.colors['sky'], 'info':'Heavy Showers'},
            95: {'night':'', 'day':'󰖓', 'color': self.colors['mauve'], 'info':'Thunderstorm'},
            96: {'night':'', 'day':'', 'color': self.colors['mauve'], 'info':'Light Hail Thunderstorm'},
            99: {'night':'', 'day':'', 'color': self.colors['mauve'], 'info':'Hail Thunderstorm'},
            'null': {'night':'󰖐', 'day':'󰖐', 'color': self.colors['overlay0'], 'info':'Unknown'}
        }

        self.data = {
            'hourly': {
                'code': [],
                'temp': [],
                'icon': [],
                'colors': [],
                'rain': [],
                'time': []
            },
            'daily': {
                'code': [],
                'temp_min': [],
                'temp_max': [],
                'temp': [],
                'icon': [],
                'colors': [],
                'rain': [],
                'time': []
            },
            'current_hour': None,
            'is_day': None,
            'weather_code': None,
            'weather_temp': None,
            'weather_icon': None,
            'rain_prcnt': None,
            'temp_min': None,
            'temp_max': None,
        }

        self.url = "https://api.open-meteo.com/v1/forecast?latitude=23.625&longitude=90.375&current=temperature_2m,precipitation,rain,weather_code,wind_speed_10m,wind_direction_10m&hourly=temperature_2m,precipitation_probability,weather_code,is_day&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max&timezone=auto"
        self.save_file = '/tmp/weather_data.txt'
    
    def run(self, type='hourly'):
        # print("Fetching data...")
        data = self.fetch_data()
        if data == None:
            self.show_data(type=type)
        else:
            self.extract_data(data)
            self.show_data(type=type)

    def get_temp_color(self, temp):
        if temp > 33:
            return self.colors['red']
        elif temp >= 30:
            return self.colors['yellow']
        elif temp >= 27:
            return self.colors['flamingo']
        elif temp >= 23:
            return self.colors['teal']
        elif temp >= 20:
            return self.colors['sky']
        else:
            return self.colors['blue']
        
    def fetch_data(self):
        try:
            response = requests.get(self.url)
            # print("Response status: ", response.status_code)
        except:
            # print("Error fetching data...")
            return None
        data = response.json()
        json_data = json.dumps(data, indent=4)
        with open(self.save_file, 'w') as file:
            file.write(json_data)
        
        # f = open(self.save_file, 'r').read()
        # saved_data = json.loads(f)
        return data

    def extract_data(self, data):
        self.data['current_hour'] = int(datetime.now().strftime("%H"))
        self.data['is_day'] = 'day' if int(data['hourly']['is_day'][self.data['current_hour']]) == 1 else 'night'
        self.data['weather_code'] = data['current']['weather_code']
        self.data['weather_code'] = self.data['weather_code'] if self.data['weather_code'] in self.weather_icons.keys() else 'null'
        self.data['weather_temp'] = data['current']['temperature_2m']
        self.data['weather_icon'] = self.weather_icons[self.data['weather_code']][self.data['is_day']]
        self.data['rain_prcnt'] = data['hourly']['precipitation_probability'][self.data['current_hour']]
        self.data['temp_min'] = round(data['daily']['temperature_2m_min'][0])
        self.data['temp_max'] = round(data['daily']['temperature_2m_max'][0])

        for i in range(1, 6):
            # Hourly Data
            nth_code = data['hourly']['weather_code'][self.data['current_hour']+i]
            nth_temp = data['hourly']['temperature_2m'][self.data['current_hour']+i]
            nth_rain = data['hourly']['precipitation_probability'][self.data['current_hour']+i]
            nth_hour = (self.data['current_hour']+i) % 24
            self.data['hourly']['temp'].append(round(nth_temp))
            self.data['hourly']['code'].append(nth_code)
            self.data['hourly']['rain'].append(nth_rain)
            self.data['hourly']['icon'].append(self.weather_icons[int(nth_code)][self.data['is_day']]) 
            self.data['hourly']['colors'].append(self.weather_icons[int(nth_code)]['color'])
            self.data['hourly']['time'].append(datetime.strptime(str(nth_hour), "%H").strftime("%-I%p"))

            # Daily Data
            nth_code = data['daily']['weather_code'][i]
            nth_temp_max = data['daily']['temperature_2m_max'][i]
            nth_temp_min = data['daily']['temperature_2m_min'][i]
            nth_rain = data['daily']['precipitation_probability_max'][i]
            nth_day = data['daily']['time'][i]
            self.data['daily']['code'].append(nth_code)
            self.data['daily']['temp_max'].append(round(nth_temp_max))
            self.data['daily']['temp'].append(round(nth_temp_max))
            self.data['daily']['temp_min'].append(round(nth_temp_min))
            self.data['daily']['rain'].append(nth_rain)
            self.data['daily']['icon'].append(self.weather_icons[int(nth_code)]['day'])
            self.data['daily']['colors'].append(self.weather_icons[int(nth_code)]['color'])
            self.data['daily']['time'].append(datetime.strptime(str(nth_day), "%Y-%m-%d").strftime("%a"))

    def show_data(self, type='hourly'):
        if type==None:
            print(json.dumps({"text": "󰖐 Offline"}))
            return

        tooltip_text = str.format(
            "{} \n{} \n{} \n{} \n\n{}\t{}\t{}\t{}\t{} \n{}\t{}\t{}\t{}\t{} \n{}\t{}\t{}\t{}\t{}",
            f'<span foreground="{self.colors['rosewater']}" size="large">{self.data['weather_temp']}°C</span>',
            f'<span foreground="{self.colors['text']}">{self.weather_icons[self.data['weather_code']]['info']}</span> <span foreground="{self.weather_icons[self.data['weather_code']]['color']}" size="x-large">{self.data['weather_icon']}</span> ',
            f'<span foreground="{self.colors['text']}">Rain:</span> <span foreground="{self.colors['blue'] if int(self.data['rain_prcnt'])>=40 else self.colors['text']}"><span size="small">󰖌</span>{self.data['rain_prcnt']}%</span>',
            f'<span foreground="{self.colors['text']}" size="smaller">H:{self.data['temp_max']}° L:{self.data['temp_min']}°</span>',
            f'<span foreground="{self.colors['text']}" size="small">{self.data[type]['time'][0]}</span>',
            f'<span foreground="{self.colors['text']}" size="small">{self.data[type]['time'][1]}</span>',
            f'<span foreground="{self.colors['text']}" size="small">{self.data[type]['time'][2]}</span>',
            f'<span foreground="{self.colors['text']}" size="small">{self.data[type]['time'][3]}</span>',
            f'<span foreground="{self.colors['text']}" size="small">{self.data[type]['time'][4]}</span>',
            f'<span foreground="{self.data[type]['colors'][0]}" size="xx-large">{self.data[type]['icon'][0]}</span>' + (f'<span foreground="{self.colors["blue"]}" size="small"> 󰖌{self.data[type]['rain'][0]}%</span>' if self.data[type]['rain'][0] >= 40 else ''),
            f'<span foreground="{self.data[type]['colors'][1]}" size="xx-large">{self.data[type]['icon'][1]}</span>' + (f'<span foreground="{self.colors["blue"]}" size="small"> 󰖌{self.data[type]['rain'][1]}%</span>' if self.data[type]['rain'][1] >= 40 else ''),
            f'<span foreground="{self.data[type]['colors'][2]}" size="xx-large">{self.data[type]['icon'][2]}</span>' + (f'<span foreground="{self.colors["blue"]}" size="small"> 󰖌{self.data[type]['rain'][2]}%</span>' if self.data[type]['rain'][2] >= 40 else ''),
            f'<span foreground="{self.data[type]['colors'][3]}" size="xx-large">{self.data[type]['icon'][3]}</span>' + (f'<span foreground="{self.colors["blue"]}" size="small"> 󰖌{self.data[type]['rain'][3]}%</span>' if self.data[type]['rain'][3] >= 40 else ''),
            f'<span foreground="{self.data[type]['colors'][4]}" size="xx-large">{self.data[type]['icon'][4]}</span>' + (f'<span foreground="{self.colors["blue"]}" size="small"> 󰖌{self.data[type]['rain'][4]}%</span>' if self.data[type]['rain'][4] >= 40 else ''),
            f'<span foreground="{self.get_temp_color(self.data[type]['temp'][0])}" size="small">{self.data[type]['temp'][0]}°C</span>',
            f'<span foreground="{self.get_temp_color(self.data[type]['temp'][1])}" size="small">{self.data[type]['temp'][1]}°C</span>',
            f'<span foreground="{self.get_temp_color(self.data[type]['temp'][2])}" size="small">{self.data[type]['temp'][2]}°C</span>',
            f'<span foreground="{self.get_temp_color(self.data[type]['temp'][3])}" size="small">{self.data[type]['temp'][3]}°C</span>',
            f'<span foreground="{self.get_temp_color(self.data[type]['temp'][4])}" size="small">{self.data[type]['temp'][4]}°C</span>'
        )

        output_icon = f'<span foreground="{self.weather_icons[self.data['weather_code']]['color']}" size="x-large">{self.data['weather_icon']}</span>'
        output_temp = f'<span foreground="{self.get_temp_color(round(self.data['weather_temp']))}">{round(self.data['weather_temp'])}°C</span>'
        output_rain = f'<span foreground="{self.colors['blue'] if int(self.data['rain_prcnt'])>=40 else self.colors['text']}"><span size="small">󰖌</span>{self.data['rain_prcnt']}%</span>'
        output = {
            "text": f'{output_icon} {output_temp}',
            "tooltip": tooltip_text,
            "alt": f'{output_rain}'
        }

        # print(json.dumps({"text": "lol"}))
        print(json.dumps(output))


weather = Weather()
if len(sys.argv) > 1:
    weather.run(type=sys.argv[1])
else:
    weather.run()
