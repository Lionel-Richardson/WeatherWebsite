from bs4 import BeautifulSoup
import requests
import mysql.connector
from datetime import datetime
import time
db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="python",
    database="weather"
    )

mycursor = db.cursor()


def get_weather():
    temps = []

#Weather Channel
    html_text = requests.get(
        "https://weather.com/weather/today/l/2d7ddcd5bcb306eb395707b513d91ff9601ca1fb230431b3946fb889247f2a7f").text
    soup = BeautifulSoup(html_text, "lxml")
    weather = soup.find("div", class_="CurrentConditions--primary--2DOqs")
    temperature_weather_channel = weather.find("span", class_= "CurrentConditions--tempValue--MHmYY").text
    conditions_weather_channel = weather.find("div", class_= "CurrentConditions--phraseValue--mZC_p").text
    temps.append(int(temperature_weather_channel[0:-1]))
    weather_channel_weather = f"""
                        Weather Channel,
                        {temperature_weather_channel}
                        {conditions_weather_channel}
                        """
    mycursor.execute("INSERT INTO weather_site_temps (source, temperature, conditions, time) VALUES (%s,%s,%s,%s)",
                     ('Weather Channel', temperature_weather_channel, conditions_weather_channel, datetime.now()))
    db.commit()
    print(f"Weather Channel: {temperature_weather_channel[0:-1]}, {conditions_weather_channel}")


#Wunderground
    html_text = requests.get(
        "https://www.wunderground.com/weather/us/va/midlothian/KVAMIDLO74").text
    soup = BeautifulSoup(html_text, "lxml")
    temperature_wunderground = soup.find("span", class_="wu-value wu-value-to").text
    conditions_wunderground = soup.find("div", class_="condition-icon small-6 medium-12 columns").text
    temps.append(float(temperature_wunderground))
    wunderground_weather = f"""
                        Wunderground,
                        {temperature_wunderground}
                        {conditions_wunderground}
                        """
    mycursor.execute("INSERT INTO weather_site_temps (source, temperature, conditions, time) VALUES (%s,%s,%s,%s)",
                     ('Wunderground', temperature_wunderground, conditions_wunderground, datetime.now()))
    db.commit()
    print(f"Wunderground: {temperature_wunderground}, {conditions_wunderground}")

#NOAA
    html_text = requests.get(
        "https://forecast.weather.gov/MapClick.php?CityName=Midlothian&state=VA&site=AKQ&textField1=37.5025&textField2=-77.6398&e=0").text
    soup = BeautifulSoup(html_text, "lxml")
    temperature_noaa = soup.find("p", class_="myforecast-current-lrg").text
    conditions_noaa = soup.find("p", class_="myforecast-current").text
    temps.append(int(temperature_noaa[0:-2]))
    NOAA_weather = f"""
                        NOAA,
                        {temperature_noaa}
                        {conditions_noaa}
                        """
    mycursor.execute("INSERT INTO weather_site_temps (source, temperature, conditions, time) VALUES (%s,%s,%s,%s)",
                     ('NOAA', temperature_noaa, conditions_noaa, datetime.now()))
    db.commit()
    print(f"NOAA: {temperature_noaa[0:-2]}, {conditions_noaa}")

#Local Conditions
    html_text = requests.get(
        "https://www.localconditions.com/weather-midlothian-virginia/23112/").text
    soup = BeautifulSoup(html_text, "lxml")
    temperature_local = soup.find("p", class_="row-stat-value").text
    conditions_local_conditions = soup.find("p", style="font-size:20pt; padding-top:0px !important; margin-top:0px !important;").text
    raw_temp = (temperature_local.split(" ")[0:-1])
    for temp in raw_temp:
        updated_temp = temp[0:-2]
    temps.append(int(updated_temp))
    local_conditions_weather = f"""
                        Local Conditions,
                        {updated_temp}
                        """
    mycursor.execute("INSERT INTO weather_site_temps (source, temperature, conditions, time) VALUES (%s,%s,%s,%s)",
                     ('Local Conditions', updated_temp, conditions_local_conditions, datetime.now()))
    db.commit()
    print(f"Local Conditions: {updated_temp}, {conditions_local_conditions}")

#Average
    sum_temps = 0
    for temperatures in temps:
        sum_temps = sum_temps + temperatures

    average = round(sum_temps / 4)
    mycursor.execute("INSERT INTO weather_site_temps (source, temperature, time) VALUES (%s,%s,%s)",
                     ('Average', average, datetime.now()))
    db.commit()
    print(f"Average: {average}")


if __name__ == "__main__":
    while True:
        get_weather()
        time_wait = 1800
        time.sleep(time_wait)

