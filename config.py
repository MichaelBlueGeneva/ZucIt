"""
Configuration settings for ZucIt Flask application
"""

import os

class Config:
    # Server configuration
    HOST = os.environ.get('ZUCIT_HOST', '127.0.0.1')
    PORT = int(os.environ.get('ZUCIT_PORT', 5004))
    DEBUG = os.environ.get('ZUCIT_DEBUG', 'True').lower() == 'true'

    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY', 'zucit-dev-secret-key-2024')

    # Application settings
    SIMULATION_YEARS = 20
    ZUCMAN_TAX_RATE = 0.02857  # 2% + flat tax
    NORMAL_PROFIT_TAX = 0.25   # 25%

    # Economic Model Parameters (Method 5 - Complete Economic Model)
    # Canal Investment
    INVESTMENT_ELASTICITY = 0.4      # Impact investissement sur productivité
    INVESTMENT_RATIO_OF_PROFIT = 0.3 # Part profit consacrée à l'investissement

    # Canal Prix-Demande
    PRICE_PASS_THROUGH = 0.7         # % de la taxe reportée sur les prix
    DEMAND_ELASTICITY = -1.2         # Élasticité prix-demande

    # Canal Compétitivité
    COMPETITIVENESS_IMPACT = 0.25    # Impact coûts sur parts de marché
    MARKET_SHARE_ELASTICITY = -0.8   # Élasticité parts de marché/coûts

    # Canal Financement
    FINANCING_COST_IMPACT = 0.15     # Impact cash-flow sur coûts financement

    # Employment Model Parameters (Method 5 - Mixed Productivity-Demand)
    PRODUCTIVITY_EMPLOYMENT_ELASTICITY = 0.3  # Plus de productivité = moins d'emploi
    DEMAND_EMPLOYMENT_ELASTICITY = 0.8        # Plus de demande = plus d'emploi