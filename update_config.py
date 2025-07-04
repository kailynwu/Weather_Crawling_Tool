import configparser

# 定义各 API 支持的数据范围
API_SUPPORTED_RANGES = {
    'hefeng': ['today', 'next_week', 'next_15_days'],
    'openweather': ['today', 'next_week'],
    'both': ['today', 'next_week', 'next_15_days']
}

def update_weather_config():
    # 初始化配置解析器
    config = configparser.ConfigParser()
    config_path = 'config/config.ini'

    # 读取配置文件
    config.read(config_path)

    # 检查是否存在 weather 部分，如果不存在则添加
    if 'weather' not in config:
        config.add_section('weather')
    if 'database' not in config:
        config.add_section('database')

    # 提示用户输入信息
    hefeng_api_key = input("请输入和风天气 API Key（留空则保持当前值）: ")
    openweather_api_key = input("请输入 OpenWeatherMap API Key（留空则保持当前值）: ")
    city = input("请输入要查询的城市（留空则保持当前值）: ")
    selected_api = input("请选择要使用的 API（hefeng/openweather/both，留空则保持当前值）: ")

    if selected_api:
        valid_choices = ['hefeng', 'openweather', 'both']
        if selected_api not in valid_choices:
            print("无效的选择，保持当前值。")
            selected_api = config.get('weather', 'selected_api', fallback='both')

    supported_ranges = API_SUPPORTED_RANGES[selected_api]
    data_range = input(f"请选择数据获取范围（{'/'.join(supported_ranges)}/all，留空则保持当前值）: ")

    use_database = input("是否开启数据库写入功能？(y/n，留空则保持当前值): ")
    if use_database:
        if use_database.lower() == 'y':
            config.set('database', 'use_database', 'True')
            host = input("请输入数据库主机地址（留空则保持当前值）: ")
            user = input("请输入数据库用户名（留空则保持当前值）: ")
            password = input("请输入数据库密码（留空则保持当前值）: ")
            database = input("请输入数据库名（留空则保持当前值）: ")
            if host:
                config.set('database', 'host', host)
            if user:
                config.set('database', 'user', user)
            if password:
                config.set('database', 'password', password)
            if database:
                config.set('database', 'database', database)
        else:
            config.set('database', 'use_database', 'False')

    # 更新配置信息
    if hefeng_api_key:
        config.set('weather', 'hefeng_api_key', hefeng_api_key)
    if openweather_api_key:
        config.set('weather', 'openweather_api_key', openweather_api_key)
    if city:
        config.set('weather', 'city', city)
    if selected_api in valid_choices:
        config.set('weather', 'selected_api', selected_api)
    if data_range:
        if data_range == 'all':
            config.set('weather', 'data_range', 'all')
        elif data_range in supported_ranges:
            config.set('weather', 'data_range', data_range)
        else:
            print("无效的数据范围选择，保持当前值。")

    # 将更新后的配置写入文件
    with open(config_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

    print("配置更新成功！")

if __name__ == "__main__":
    update_weather_config()
