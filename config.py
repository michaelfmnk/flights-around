from pydantic import BaseModel, Field, HttpUrl
import yaml

class Config(BaseModel):
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT")
    latitude: float
    longitude: float
    radius_km: int
    opensky_url: HttpUrl
    adsb_url: HttpUrl

def load_config(file_path: str = "config.yaml") -> Config:
    with open(file_path, "r") as file:
        config_data = yaml.safe_load(file)
    return Config(**config_data)