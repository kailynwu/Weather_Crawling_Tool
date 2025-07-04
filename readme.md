# 天气爬取工具

## 项目概述
本项目是一个功能强大的天气爬取工具，支持从和风天气和 OpenWeatherMap 两个知名 API 获取天气数据。获取到的天气数据会被保存为 JSON 文件，方便后续的数据分析和处理。同时，该工具还支持将数据写入 MySQL 数据库，以实现数据的长期存储和管理。用户可以通过配置文件灵活地选择使用的 API、查询的城市、数据获取范围，还能决定是否开启数据库写入功能。

## 功能特性
- **多 API 支持**：支持从和风天气和 OpenWeatherMap 两个 API 获取天气数据，满足不同数据源的需求。
- **灵活配置**：用户可以通过 `config.ini` 文件或 `update_config.py` 脚本修改配置信息，包括 API 密钥、查询城市、使用的 API、数据获取范围以及数据库相关信息。
- **数据保存**：将获取的天气数据保存为 JSON 文件，方便后续分析和使用。
- **数据库支持**：支持将天气数据写入 MySQL 数据库，方便长期存储和管理。

## 项目结构
```plaintext
天气爬取工具/
├── .idea/                   # IDE 配置文件
├── config/                  # 配置文件目录
│   └── config.ini           # 配置文件
├── data/                    # 保存天气数据的目录
├── .gitignore               # Git 忽略文件
├── requirements.txt         # 项目依赖文件
├── update_config.py         # 更新配置文件的脚本
├── weather_crawler.py       # 天气爬取主脚本
└── README.md                # 项目说明文件
```

## 安装与配置

### 安装依赖
在运行项目之前，需要安装项目所需的依赖库。这些依赖库的信息记录在 `requirements.txt` 文件中，可使用以下命令进行安装：
```bash
pip install -r requirements.txt
```
`requirements.txt` 文件内容如下：
```plaintext
requests
mysql-connector-python
```
- `requests`：用于发送 HTTP 请求，获取 API 数据。
- `mysql-connector-python`：用于连接和操作 MySQL 数据库。

### 配置文件
在 `config/config.ini` 文件中配置相关信息：
```ini
[weather]
hefeng_api_key = your_hefeng_api_key
openweather_api_key = your_openweather_api_key
city = Nanjing
selected_api = hefeng
data_range = all

[database]
use_database = True
host = your_database_host
user = your_database_user
password = your_database_password
database = your_database_name
```
- `hefeng_api_key`：和风天气 API 密钥。
- `openweather_api_key`：OpenWeatherMap API 密钥。
- `city`：要查询的城市。
- `selected_api`：要使用的 API，可选值为 `hefeng`、`openweather` 或 `both`。
- `data_range`：数据获取范围，可选值为 `today`、`next_week`、`next_15_days` 或 `all`。
- `use_database`：是否开启数据库写入功能，可选值为 `True` 或 `False`。
- `host`：数据库主机地址。
- `user`：数据库用户名。
- `password`：数据库密码。
- `database`：数据库名。

### 更新配置
可以运行 `update_config.py` 脚本来更新配置文件：
```bash
python update_config.py
```
该脚本会提示用户输入新的配置信息，包括 API 密钥、查询城市、使用的 API、数据获取范围以及数据库相关信息。

## 使用方法
运行 `weather_crawler.py` 脚本来获取天气数据：
```bash
python weather_crawler.py
```
脚本会根据配置文件中的信息，从指定的 API 获取天气数据，并将数据保存为 JSON 文件。如果开启了数据库写入功能，还会将数据写入 MySQL 数据库。

## 代码说明

### `update_config.py`
此脚本用于更新配置文件 `config/config.ini` 中的信息。它会引导用户输入新的配置参数，并将更新后的配置保存到文件中。具体功能如下：
1. **读取配置文件**：使用 `configparser` 读取 `config/config.ini` 文件。
2. **提示用户输入信息**：包括 API 密钥、查询城市、使用的 API、数据获取范围以及数据库相关信息。
3. **验证用户输入**：确保用户输入的信息合法，如 API 选择、数据范围等。
4. **更新配置文件**：将用户输入的信息更新到 `config/config.ini` 文件中。

### `weather_crawler.py`
这是天气爬取的主脚本，主要功能包括：
1. **API 请求**：根据配置文件中的信息，从和风天气和 OpenWeatherMap API 获取天气数据。
2. **数据处理**：对获取的天气数据进行处理，提取所需信息。
3. **数据保存**：将处理后的天气数据保存为 JSON 文件，并根据配置决定是否将数据写入 MySQL 数据库。

## 注意事项
1. **API 密钥**：请确保在配置文件中填写有效的 API 密钥，否则无法获取天气数据。
2. **数据库配置**：如果开启了数据库写入功能，请确保数据库服务正常运行，并填写正确的数据库连接信息。
3. **数据范围**：不同的 API 支持的数据范围不同，请根据实际情况选择合适的数据范围。

## 贡献
如果你对本项目有任何建议或改进意见，欢迎提交 issue 或 pull request。我们非常欢迎社区的参与和贡献，共同完善这个项目。

## 许可证
本项目采用 `BSD - 2 - Clause` 许可证。以下是许可证的详细内容：

```plaintext
BSD 2-Clause License

Copyright (c) 2025, kailynwu
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
```