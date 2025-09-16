from flask import Flask, render_template, request, jsonify
import json
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

def ensure_real(value):
    """S'assurer qu'une valeur est un nombre réel, pas complexe."""
    if isinstance(value, complex):
        return value.real
    return value

# Exemples d'entreprises
EXAMPLE_COMPANIES = {
    "apple": {
        "name": "Apple Inc.",
        "valuation": 3000000000000,  # 3T€
        "profit": 100000000000,     # 100B€
        "employees": 164000,
        "growth_rate": 0.08         # 8%
    },
    "microsoft": {
        "name": "Microsoft Corp.",
        "valuation": 2800000000000,  # 2.8T€
        "profit": 83000000000,      # 83B€
        "employees": 221000,
        "growth_rate": 0.12         # 12%
    },
    "google": {
        "name": "Google/Alphabet",
        "valuation": 1700000000000,  # 1.7T€
        "profit": 76000000000,      # 76B€
        "employees": 190000,
        "growth_rate": 0.10         # 10%
    },
    "startup": {
        "name": "Startup Tech",
        "valuation": 50000000,       # 50M€
        "profit": 2000000,          # 2M€
        "employees": 50,
        "growth_rate": 0.25         # 25%
    }
}

def simulate_zucman_effect(valuation, profit, employees, growth_rate, years=None):
    """
    Simule l'effet de la taxe Zucman sur 20 ans avec modèle économique complet
    Taxe Zucman: 2.857% sur la valorisation (2% + flat tax)
    Taxe normale: 25% sur les bénéfices
    """
    
    # Validation des entrées pour éviter les divisions par zéro
    if profit <= 0:
        profit = max(1000000, valuation * 0.001)  # Minimum 1M ou 0.1% de la valorisation
    if valuation <= 0:
        valuation = profit * 10  # Valorisation minimum basée sur le profit
    if employees <= 0:
        employees = 1000  # Minimum d'employés
    
    if years is None:
        years = app.config['SIMULATION_YEARS']

    # Données pour les graphiques
    years_data = []

    # Simulation sans Zucman
    no_zucman = {
        "profits": [],
        "employees": [],
        "state_revenue": [],
        "valuations": [],
        "prices": []  # Nouveau: évolution des prix
    }

    # Simulation avec Zucman
    with_zucman = {
        "profits": [],
        "employees": [],
        "state_revenue": [],
        "valuations": [],
        "prices": []  # Nouveau: évolution des prix
    }

    # Variables initiales
    current_profit_no_zuc = profit
    current_profit_with_zuc = profit
    current_valuation_no_zuc = valuation
    current_valuation_with_zuc = valuation

    # Variables pour le modèle économique complet
    base_price = 100.0  # Prix de référence (base 100)
    current_price_no_zuc = base_price
    current_price_with_zuc = base_price

    # Estimation du chiffre d'affaires initial (profit / marge typique de 10%)
    estimated_revenue = profit / 0.10

    for year in range(years + 1):
        years_data.append(2024 + year)

        # === SCENARIO SANS ZUCMAN ===
        no_zucman["profits"].append(current_profit_no_zuc)
        no_zucman["valuations"].append(current_valuation_no_zuc)
        no_zucman["prices"].append(current_price_no_zuc)

        # Employés avec méthode mixte productivité-demande (sans Zucman)
        current_employees_no_zuc = employees  # Pas d'impact sans taxe
        no_zucman["employees"].append(current_employees_no_zuc)

        # Recettes état: 25% des bénéfices
        state_revenue_no_zuc = current_profit_no_zuc * app.config['NORMAL_PROFIT_TAX']
        no_zucman["state_revenue"].append(state_revenue_no_zuc)

        # === SCENARIO AVEC ZUCMAN ===
        with_zucman["profits"].append(current_profit_with_zuc)
        with_zucman["valuations"].append(current_valuation_with_zuc)
        with_zucman["prices"].append(current_price_with_zuc)

        # Calcul taxe Zucman
        zucman_tax = current_valuation_with_zuc * app.config['ZUCMAN_TAX_RATE']

        # === MODÈLE ÉCONOMIQUE COMPLET - EMPLOI MIXTE PRODUCTIVITÉ-DEMANDE ===

        # Canal 1: Effet Productivité (moins d'investissement → moins de productivité → plus d'emploi pour même production)
        investment_reduction = zucman_tax * app.config['INVESTMENT_RATIO_OF_PROFIT']
        # Protection contre division par zéro
        if current_profit_with_zuc > 0:
            productivity_impact = investment_reduction / current_profit_with_zuc * app.config['INVESTMENT_ELASTICITY']
        else:
            productivity_impact = 0
        employment_from_productivity = productivity_impact * app.config['PRODUCTIVITY_EMPLOYMENT_ELASTICITY'] * employees

        # Canal 2: Effet Demande (prix plus élevés → moins de demande → moins d'emploi)
        price_increase_pct = (current_price_with_zuc - base_price) / base_price
        demand_reduction = price_increase_pct * app.config['DEMAND_ELASTICITY']
        employment_from_demand = demand_reduction * app.config['DEMAND_EMPLOYMENT_ELASTICITY'] * employees

        # Effet net sur l'emploi
        net_employment_change = employment_from_productivity + employment_from_demand
        min_employees = max(1, int(employees * 0.05))  # Plancher 5%
        current_employees_with_zuc = max(min_employees, int(employees + net_employment_change))

        with_zucman["employees"].append(current_employees_with_zuc)

        # Recettes état: 25% bénéfices + taxe Zucman
        profit_tax = current_profit_with_zuc * app.config['NORMAL_PROFIT_TAX']
        state_revenue_with_zuc = profit_tax + zucman_tax
        with_zucman["state_revenue"].append(state_revenue_with_zuc)

        # Préparation année suivante
        if year < years:
            # === MODÈLE ÉCONOMIQUE COMPLET POUR LES BÉNÉFICES ===

            # Croissance de base
            current_profit_no_zuc *= (1 + growth_rate)
            base_growth_with_zuc = current_profit_with_zuc * (1 + growth_rate)

            # Canal 1: Impact Investissement
            investment_available = current_profit_with_zuc - zucman_tax * app.config['INVESTMENT_RATIO_OF_PROFIT']
            # Protection contre division par zéro
            if current_profit_with_zuc > 0:
                investment_ratio = max(0.1, investment_available / current_profit_with_zuc)  # Éviter les valeurs négatives
            else:
                investment_ratio = 0.1  # Valeur par défaut
            investment_impact = ensure_real(investment_ratio ** app.config['INVESTMENT_ELASTICITY'])
            canal_investment = ensure_real(base_growth_with_zuc * (investment_impact - 1) * 0.4)

            # Canal 2: Impact Prix-Demande
            price_increase = zucman_tax * app.config['PRICE_PASS_THROUGH']
            relative_price_increase = price_increase / estimated_revenue
            demand_change = relative_price_increase * app.config['DEMAND_ELASTICITY']
            canal_prix_demande = ensure_real(base_growth_with_zuc * demand_change * 0.3)

            # Canal 3: Impact Compétitivité
            cost_increase = zucman_tax / estimated_revenue
            market_share_change = cost_increase * app.config['MARKET_SHARE_ELASTICITY']
            canal_competitivite = ensure_real(base_growth_with_zuc * market_share_change * 0.25)

            # Canal 4: Impact Financement
            # Protection contre division par zéro
            if current_profit_with_zuc > 0:
                cash_flow_impact = zucman_tax / current_profit_with_zuc
            else:
                cash_flow_impact = 0
            financing_cost_change = cash_flow_impact * app.config['FINANCING_COST_IMPACT']
            canal_financement = ensure_real(base_growth_with_zuc * (-financing_cost_change) * 0.05)

            # Impact total
            total_impact = canal_investment + canal_prix_demande + canal_competitivite + canal_financement
            # S'assurer que le résultat est un nombre réel
            total_impact = ensure_real(total_impact)
            current_profit_with_zuc = max(0, base_growth_with_zuc + total_impact)

            # Mise à jour des prix
            current_price_no_zuc *= (1 + 0.02)  # Inflation normale 2%
            price_increase_from_tax = (zucman_tax / estimated_revenue) * app.config['PRICE_PASS_THROUGH'] * 100
            current_price_with_zuc = current_price_no_zuc + price_increase_from_tax

            # Croissance des valorisations
            current_valuation_no_zuc *= (1 + growth_rate * 0.8)
            profit_ratio = current_profit_with_zuc / base_growth_with_zuc if base_growth_with_zuc != 0 else 1.0
            valuation_growth_factor = max(0.2, profit_ratio) * 0.6
            current_valuation_with_zuc *= (1 + growth_rate * valuation_growth_factor)

    # Calcul des KPIs finaux
    final_profit_diff = no_zucman["profits"][-1] - with_zucman["profits"][-1]
    final_employees_diff = no_zucman["employees"][-1] - with_zucman["employees"][-1]
    total_zucman_revenue = sum(with_zucman["state_revenue"]) - sum(no_zucman["state_revenue"])

    # Calcul du total de la taxe Zucman collectée sur les valorisations
    total_zucman_tax_collected = 0
    current_val_temp = valuation
    for year in range(years):
        total_zucman_tax_collected += current_val_temp * app.config['ZUCMAN_TAX_RATE']
        current_val_temp *= (1 + growth_rate * 0.6)  # Croissance réduite avec Zucman

    # Nouveau KPI: Augmentation des prix
    final_price_increase = with_zucman["prices"][-1] - no_zucman["prices"][-1]
    price_increase_percent = (final_price_increase / no_zucman["prices"][-1]) * 100

    kpis = {
        "profit_loss_percent": (final_profit_diff / no_zucman["profits"][-1]) * 100 if no_zucman["profits"][-1] > 0 else 0,
        "profit_loss_amount": final_profit_diff,
        "jobs_lost": final_employees_diff,
        "jobs_lost_percent": (final_employees_diff / no_zucman["employees"][-1]) * 100 if no_zucman["employees"][-1] > 0 else 0,
        "additional_tax_revenue": total_zucman_revenue,
        "tax_efficiency": total_zucman_revenue / total_zucman_tax_collected if total_zucman_tax_collected > 0 else 0,
        "total_zucman_tax_collected": total_zucman_tax_collected,
        "price_increase_percent": price_increase_percent,
        "price_increase_absolute": final_price_increase
    }

    return {
        "years": years_data,
        "no_zucman": no_zucman,
        "with_zucman": with_zucman,
        "kpis": kpis
    }

@app.route('/')
def index():
    return render_template('index.html', companies=EXAMPLE_COMPANIES)

@app.route('/methodology')
def methodology():
    return render_template('explanation.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json

    valuation = float(data['valuation'])
    profit = float(data['profit'])
    employees = int(data['employees'])
    growth_rate = float(data['growth_rate']) / 100  # Convert percentage to decimal

    results = simulate_zucman_effect(valuation, profit, employees, growth_rate)
    return jsonify(results)

@app.route('/company/<company_id>')
def get_company(company_id):
    if company_id in EXAMPLE_COMPANIES:
        return jsonify(EXAMPLE_COMPANIES[company_id])
    return jsonify({"error": "Company not found"}), 404

if __name__ == '__main__':
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])