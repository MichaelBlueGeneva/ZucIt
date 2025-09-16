"""
Configuration settings for ZucIt Flask application
"""

import os

class Config:
    # Server configuration
    HOST = os.environ.get('ZUCIT_HOST', '127.0.0.1')
    PORT = int(os.environ.get('ZUCIT_PORT', 5001))
    DEBUG = os.environ.get('ZUCIT_DEBUG', 'True').lower() == 'true'

    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'zucit-dev-secret-key-2024')

    # Application settings
    SIMULATION_YEARS = 20
    ZUCMAN_TAX_RATE = 0.02857  # 2% + flat tax
    NORMAL_PROFIT_TAX = 0.25   # 25%