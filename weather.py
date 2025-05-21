import bs4
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

towns = {
    'Գորիս': 'syunik/goris',
    'Կապան': 'syunik/kapan',
    'Մեղրի': 'syunik/meghri',
    'Սիսիան': 'syunik/sisian',
    'Տաթև': 'syunik/tatev',
    'Տեղ': 'syunik/tegh',
    'Քաջարան': 'syunik/kadzharan',
}

def get_armenian_month(month):
    months = {
        1: "հունվարի", 2: "փետրվարի", 3: "մարտի", 4: "ապրիլի",
        5: "մայիսի", 6: "հունիսի", 7: "հուլիսի", 8: "օգոստոսի",
        9: "սեպտեմբերի", 10: "հոկտեմբերի", 11: "նոյեմբերի", 12: "դեկտեմբերի"
    }
    return months.get(month, "")

def generate_weather_report(cities_data, date=None):
    if date is None:
        date = datetime.now() + timedelta(days=1)

    day = date.day
    month = get_armenian_month(date.month)

    # Header
    report = [
        f"🔵 Եղանակը Սյունիքում {month} {day}-ին",
        "➖" * 10,
        "⛅ Սյունիքի մարզում տեղումներ չեն սպասվում",
        "➖" * 10,
        ""
    ]

    # City data
    for city, temps in cities_data.items():
        day_temp, night_temp = temps
        day_temp_str = f"+{day_temp}" if day_temp > 0 else f"{day_temp}"
        night_temp_str = f"+{night_temp}" if night_temp > 0 else f"{night_temp}"

        city_report = [
            f"🟦 {city}",
            f"🌖 {day_temp_str}°C (ցերեկ)",
            f"🌗 {night_temp_str}°C (երեկո)",
            ""
        ]
        report.extend(city_report)

    return "\n".join(report)

cities_data = {}

for town, town_url in towns.items():
    page = requests.get(f'https://exanak.am/tomorrow-weather-forecast/{town_url}')
    soup = BeautifulSoup(page.text, 'html.parser')

    weather = soup.find_all(class_='num')
    day_temp = int(weather[0].text.replace('℃', '').strip())
    night_temp = int(weather[1].text.replace('℃', '').strip())
    cities_data[town] = (day_temp, night_temp)

sorted_cities = ["Գորիս", "Կապան", "Մեղրի", "Սիսիան", "Տաթև", "Տեղ", "Քաջարան"]
sorted_cities_data = {city: cities_data[city] for city in sorted_cities}

if __name__ == "__main__":
    print(generate_weather_report(sorted_cities_data))

