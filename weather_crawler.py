import requests
import configparser
from datetime import datetime, timedelta
import os
import json
import mysql.connector
from mysql.connector import Error


def make_api_request(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response content: {response.text}")
    except requests.RequestException as e:
        print(f"Request error: {e}")
    return None


def get_location_id(city, api_key):
    url = "https://geoapi.qweather.com/v2/city/lookup"
    params = {
        "location": city,
        "key": api_key
    }
    data = make_api_request(url, params)
    if data and data["code"] == "200" and data["location"]:
        return data["location"][0]["id"]
    return None


# 和风天气 API 请求函数
def get_weather_from_hefeng(city, api_key, data_range):
    location_id = get_location_id(city, api_key)
    if not location_id:
        print("Failed to get location ID for the city.")
        return []

    if data_range == 'today':
        url = "https://devapi.qweather.com/v7/weather/now"
        params = {
            "location": location_id,
            "key": api_key
        }
    elif data_range == 'next_week':
        url = "https://devapi.qweather.com/v7/weather/7d"
        params = {
            "location": location_id,
            "key": api_key
        }
    elif data_range == 'next_15_days':
        url = "https://devapi.qweather.com/v7/weather/15d"
        params = {
            "location": location_id,
            "key": api_key
        }
    else:
        print("和风天气 API 不支持该数据范围")
        return []

    data = make_api_request(url, params)
    if not data:
        return []

    if data["code"] == "200":
        if data_range == 'today':
            weather_info = {
                "city": city,
                "temperature": data["now"]["temp"],
                "feels_like": data["now"]["feelsLike"],
                "condition": data["now"]["text"],
                "humidity": data["now"]["humidity"],
                "wind_speed": data["now"]["windSpeed"],
                "wind_direction": data["now"]["windDir"],
                "pressure": data["now"]["pressure"],
                "source": "hefeng",
                "data_range": data_range
            }
            return [weather_info]
        elif data_range in ['next_week', 'next_15_days']:
            weather_info_list = []
            for daily in data["daily"]:
                weather_info = {
                    "city": city,
                    "date": daily["fxDate"],
                    "temp_max": daily["tempMax"],
                    "temp_min": daily["tempMin"],
                    "condition_day": daily["textDay"],
                    "condition_night": daily["textNight"],
                    "humidity": daily["humidity"],
                    "wind_speed_day": daily["windSpeedDay"],
                    "wind_direction_day": daily["windDirDay"],
                    "wind_speed_night": daily["windSpeedNight"],
                    "wind_direction_night": daily["windDirNight"],
                    "pressure": daily["pressure"],
                    "source": "hefeng",
                    "data_range": data_range
                }
                weather_info_list.append(weather_info)
            return weather_info_list
    elif data["code"] == "401":
        print("和风天气 API 密钥无效，请检查。")
    elif data["code"] == "404":
        print("和风天气未找到该城市，请检查城市名称。")
    else:
        print(f"HeFeng API error: {data['code']}")
    return []


# OpenWeatherMap API 请求函数
def get_weather_from_openweather(city, api_key, data_range):
    if data_range == 'today':
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
    elif data_range == 'next_week':
        url = "https://api.openweathermap.org/data/2.5/forecast"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric"
        }
    else:
        print("OpenWeatherMap API 不支持该数据范围")
        return []

    data = make_api_request(url, params)
    if not data:
        return []

    if data["cod"] == 200:
        if data_range == 'today':
            weather_info = {
                "city": city,
                "temperature": data["main"]["temp"],
                "feels_like": data["main"]["feels_like"],
                "condition": data["weather"][0]["main"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "wind_direction": data["wind"]["deg"],
                "pressure": data["main"]["pressure"],
                "source": "openweather",
                "data_range": data_range
            }
            return [weather_info]
        elif data_range == 'next_week':
            weather_info_list = []
            today = datetime.now().date()
            for item in data["list"]:
                item_date = datetime.fromtimestamp(item["dt"]).date()
                if item_date - today <= timedelta(days=7):
                    weather_info = {
                        "city": city,
                        "date": item_date.strftime("%Y-%m-%d"),
                        "time": datetime.fromtimestamp(item["dt"]).strftime("%H:%M:%S"),
                        "temperature": item["main"]["temp"],
                        "feels_like": item["main"]["feels_like"],
                        "condition": item["weather"][0]["main"],
                        "humidity": item["main"]["humidity"],
                        "wind_speed": item["wind"]["speed"],
                        "wind_direction": item["wind"]["deg"],
                        "pressure": item["main"]["pressure"],
                        "source": "openweather",
                        "data_range": data_range
                    }
                    weather_info_list.append(weather_info)
            return weather_info_list
    elif data["cod"] == "401":
        print("OpenWeatherMap API 密钥无效，请检查。")
    elif data["cod"] == "404":
        print("OpenWeatherMap 未找到该城市，请检查城市名称。")
    else:
        print(f"OpenWeather API error: {data['cod']}")
    return []


# 多渠道获取天气信息
def get_weather(city, hefeng_api_key, openweather_api_key, selected_api, data_range):
    API_SUPPORTED_RANGES = {
        'hefeng': ['today', 'next_week', 'next_15_days'],
        'openweather': ['today', 'next_week'],
        'both': ['today', 'next_week', 'next_15_days']
    }
    weather_info_list = []
    if data_range == 'all':
        ranges_to_fetch = API_SUPPORTED_RANGES[selected_api]
        for range_item in ranges_to_fetch:
            if selected_api in ['hefeng', 'both']:
                hefeng_info = get_weather_from_hefeng(city, hefeng_api_key, range_item)
                weather_info_list.extend(hefeng_info)
            if selected_api in ['openweather', 'both']:
                openweather_info = get_weather_from_openweather(city, openweather_api_key, range_item)
                weather_info_list.extend(openweather_info)
    else:
        if selected_api in ['hefeng', 'both']:
            hefeng_info = get_weather_from_hefeng(city, hefeng_api_key, data_range)
            weather_info_list.extend(hefeng_info)
        if selected_api in ['openweather', 'both']:
            openweather_info = get_weather_from_openweather(city, openweather_api_key, data_range)
            weather_info_list.extend(openweather_info)
    return weather_info_list


def save_weather_data(weather_info_list, city, data_range):
    # 创建 data 目录（如果不存在）
    if not os.path.exists('data'):
        os.makedirs('data')

    # 生成文件名
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    if data_range == 'all':
        filename = f"data/{city}_all_{timestamp}.json"
    else:
        filename = f"data/{city}_{data_range}_{timestamp}.json"

    # 将数据保存到 JSON 文件
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(weather_info_list, f, ensure_ascii=False, indent=4)

    print(f"天气数据已保存到 {filename}")


def create_connection(config):
    try:
        connection = mysql.connector.connect(
            host=config.get('database', 'host'),
            user=config.get('database', 'user'),
            password=config.get('database', 'password'),
            database=config.get('database', 'database')
        )
        return connection
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None


def create_table(connection):
    cursor = connection.cursor()
    create_table_query = """
    CREATE TABLE IF NOT EXISTS weather_data (
        id INT AUTO_INCREMENT PRIMARY KEY,
        city VARCHAR(255) NOT NULL,
        source VARCHAR(50) NOT NULL,
        data_range VARCHAR(50) NOT NULL,
        date DATE,
        `time` TIME,
        temperature FLOAT,
        feels_like FLOAT,
        `condition` VARCHAR(255),
        humidity INT,
        wind_speed FLOAT,
        wind_direction VARCHAR(50),
        pressure FLOAT,
        temp_max FLOAT,
        temp_min FLOAT,
        condition_day VARCHAR(255),
        condition_night VARCHAR(255),
        wind_speed_day FLOAT,
        wind_direction_day VARCHAR(50),
        wind_speed_night FLOAT,
        wind_direction_night VARCHAR(50)
    )
    """
    cursor.execute(create_table_query)
    connection.commit()


def insert_weather_data(connection, weather_info):
    cursor = connection.cursor()
    insert_query = """
    INSERT INTO weather_data (
        city, source, data_range, date, `time`, temperature, feels_like, `condition`,
        humidity, wind_speed, wind_direction, pressure, temp_max, temp_min,
        condition_day, condition_night, wind_speed_day, wind_direction_day,
        wind_speed_night, wind_direction_night
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    date_value = weather_info.get('date')
    if date_value:
        date_value = datetime.strptime(date_value, "%Y-%m-%d").date()
    time_value = weather_info.get('time')
    if time_value:
        time_value = datetime.strptime(time_value, "%H:%M:%S").time()

    values = (
        weather_info['city'],
        weather_info['source'],
        weather_info['data_range'],
        date_value,
        time_value,
        weather_info.get('temperature'),
        weather_info.get('feels_like'),
        weather_info.get('condition'),
        weather_info.get('humidity'),
        weather_info.get('wind_speed'),
        weather_info.get('wind_direction'),
        weather_info.get('pressure'),
        weather_info.get('temp_max'),
        weather_info.get('temp_min'),
        weather_info.get('condition_day'),
        weather_info.get('condition_night'),
        weather_info.get('wind_speed_day'),
        weather_info.get('wind_direction_day'),
        weather_info.get('wind_speed_night'),
        weather_info.get('wind_direction_night')
    )
    cursor.execute(insert_query, values)
    connection.commit()


if __name__ == "__main__":
    # 读取配置文件
    config = configparser.ConfigParser()
    config.read('config/config.ini')

    # 获取配置信息
    HEFENG_API_KEY = config.get('weather', 'hefeng_api_key')
    OPENWEATHER_API_KEY = config.get('weather', 'openweather_api_key')
    city = config.get('weather', 'city')
    selected_api = config.get('weather', 'selected_api', fallback='both')
    data_range = config.get('weather', 'data_range', fallback='today')
    use_database = config.getboolean('database', 'use_database', fallback=False)

    weather_info_list = get_weather(city, HEFENG_API_KEY, OPENWEATHER_API_KEY, selected_api, data_range)
    for info in weather_info_list:
        if info['data_range'] == 'today':
            print(f"Source: {info['source']}")
            print(f"City: {info['city']}")
            print(f"Temperature: {info['temperature']}°C")
            print(f"Feels Like: {info['feels_like']}°C")
            print(f"Condition: {info['condition']}")
            print(f"Humidity: {info['humidity']}%")
            print(f"Wind Speed: {info['wind_speed']} m/s")
            print(f"Wind Direction: {info['wind_direction']}")
            print(f"Pressure: {info['pressure']} hPa")
        elif info['data_range'] in ['next_week', 'next_15_days']:
            print(f"Source: {info['source']}")
            print(f"City: {info['city']}")
            print(f"Date: {info['date']}")
            if 'temp_max' in info:
                print(f"Max Temperature: {info['temp_max']}°C")
                print(f"Min Temperature: {info['temp_min']}°C")
                print(f"Day Condition: {info['condition_day']}")
                print(f"Night Condition: {info['condition_night']}")
                print(f"Humidity: {info['humidity']}%")
                print(f"Day Wind Speed: {info['wind_speed_day']} m/s")
                print(f"Day Wind Direction: {info['wind_direction_day']}")
                print(f"Night Wind Speed: {info['wind_speed_night']} m/s")
                print(f"Night Wind Direction: {info['wind_direction_night']}")
                print(f"Pressure: {info['pressure']} hPa")
            else:
                print(f"Time: {info['time']}")
                print(f"Temperature: {info['temperature']}°C")
                print(f"Feels Like: {info['feels_like']}°C")
                print(f"Condition: {info['condition']}")
                print(f"Humidity: {info['humidity']}%")
                print(f"Wind Speed: {info['wind_speed']} m/s")
                print(f"Wind Direction: {info['wind_direction']}")
                print(f"Pressure: {info['pressure']} hPa")
        print("-" * 40)

    # 保存数据
    save_weather_data(weather_info_list, city, data_range)

    if use_database:
        connection = create_connection(config)
        if connection:
            create_table(connection)
            for weather_info in weather_info_list:
                insert_weather_data(connection, weather_info)
            connection.close()
            print("天气数据已成功写入数据库。")
            print("天气数据已成功写入数据库。")