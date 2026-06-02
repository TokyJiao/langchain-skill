# weather.py
from langchain_core.tools import tool

@tool(description="获取指定城市天气信息")
def get_weather(city: str):
    return {
        "location": city,
        "condition": "Cloudy",
        "temperature": 26,
        "feels_like": 28,
        "humidity": 78,
        "wind": 12
    }