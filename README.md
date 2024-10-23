# Plane Tracker Telegram Bot

 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is a Telegram bot that tracks planes around a specified location and notifies you when new planes enter the area. The bot uses the OpenSky Network and ADS-B API to fetch flight data.

## Features

- Tracks planes around a specified location.
- Notifies you only when new planes enter the specified area.
- Provides flight details including origin and destination.

## Prerequisites

- Python 3.7+
- Telegram Bot Token
- OpenSky Network API
- ADS-B API

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/plane-tracker-bot.git
    cd plane-tracker-bot
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

4. Create a `config.yaml` file in the root directory with the following content:
    ```yaml
    telegram_bot_token: "YOUR_TELEGRAM_BOT_TOKEN"
    latitude: 42.4412
    longitude: 19.2626
    radius_km: 70
    opensky_url: "https://opensky-network.org"
    adsb_url: "https://api.adsbdb.com"
    ```

## Usage

1. Run the bot:
    ```sh
    python main.py
    ```
2. Start the bot by sending the `/start` command in your Telegram chat.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.