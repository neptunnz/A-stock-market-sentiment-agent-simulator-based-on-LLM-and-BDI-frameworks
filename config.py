"""
Configuration File: Stores API keys and system configurations.
"""
import os

# Baidu Wenxin API configuration
BAIDU_API_KEY = "bce-v3/ALTAK-sqxDsBHgj2ifI2OrfTq2X/e4fd6c8dec76c9a8b13e98f8e279710ff4fe73db"

# Extract access_key and secret_key from API Key
# API Key format: bce-v3/{access_key}/{secret_key}
def parse_api_key(api_key: str):
    """Parse API Key"""
    parts = api_key.split('/')
    if len(parts) >= 3:
        access_key = parts[1]
        secret_key = parts[2]
        return access_key, secret_key
    return None, None

ACCESS_KEY, SECRET_KEY = parse_api_key(BAIDU_API_KEY)

# Market configuration
INITIAL_STOCK_PRICE = 100.0  # initial stock price
BASE_VOLATILITY = 0.02  # base volatility
NEWS_IMPACT_MULTIPLIER = 0.05  # news impact multiplier

# Agent configuration
AGENT_TYPES = ['optimistic', 'pessimistic', 'calm']
AGENT_NAMES = {
    'optimistic': ['optimistic investor A', 'optimistic investor B'],
    'pessimistic': ['pessimistic investor A', 'pessimistic investor B'],
    'calm': ['calm investor A']
}

