from flask import Flask, render_template, request, jsonify
import json
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

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
    if years is None:
        years = app.config['SIMULATION_YEARS']
    """
    Simule l'effet de la taxe Zucman sur 20 ans
    Taxe Zucman: 2.857% sur la valorisation (2% + flat tax)
    Taxe normale: 25% sur les bénéfices
    """

    # Données pour les graphiques
    years_data = []

    # Simulation sans Zucman
    no_zucman = {
        "profits": [],
        "employees": [],
        "state_revenue": [],
        "valuations": []
    }

    # Simulation avec Zucman
    with_zucman = {
        "profits": [],
        "employees": [],
        "state_revenue": [],
        "valuations": []
    }

    current_profit_no_zuc = profit
    current_profit_with_zuc = profit
    current_valuation_no_zuc = valuation
    current_valuation_with_zuc = valuation

    for year in range(years + 1):
        years_data.append(2024 + year)

        # === SCENARIO SANS ZUCMAN ===
        no_zucman["profits"].append(current_profit_no_zuc)
        no_zucman["valuations"].append(current_valuation_no_zuc)

        # Employés proportionnels au profit (base: ratio initial)
        employee_ratio = employees / profit
        current_employees_no_zuc = int(current_profit_no_zuc * employee_ratio)
        no_zucman["employees"].append(current_employees_no_zuc)

        # Recettes état: 25% des bénéfices
        state_revenue_no_zuc = current_profit_no_zuc * app.config['NORMAL_PROFIT_TAX']
        no_zucman["state_revenue"].append(state_revenue_no_zuc)

        # === SCENARIO AVEC ZUCMAN ===
        with_zucman["profits"].append(current_profit_with_zuc)
        with_zucman["valuations"].append(current_valuation_with_zuc)

        # Employés proportionnels au profit
        current_employees_with_zuc = int(current_profit_with_zuc * employee_ratio)
        with_zucman["employees"].append(current_employees_with_zuc)

        # Recettes état: 25% bénéfices + 2.857% valorisation
        zucman_tax = current_valuation_with_zuc * app.config['ZUCMAN_TAX_RATE']
        profit_tax = current_profit_with_zuc * app.config['NORMAL_PROFIT_TAX']
        state_revenue_with_zuc = profit_tax + zucman_tax
        with_zucman["state_revenue"].append(state_revenue_with_zuc)

        # Préparation année suivante
        if year < years:
            # Croissance des bénéfices
            current_profit_no_zuc *= (1 + growth_rate)
            current_profit_with_zuc *= (1 + growth_rate)

            # Impact Zucman sur les bénéfices (réduction des investissements)
            zucman_impact = current_valuation_with_zuc * app.config['ZUCMAN_TAX_RATE']
            current_profit_with_zuc -= zucman_impact * 0.5  # 50% de la taxe impacte les bénéfices futurs

            # Croissance des valorisations (plus modérée avec Zucman)
            current_valuation_no_zuc *= (1 + growth_rate * 0.8)
            current_valuation_with_zuc *= (1 + growth_rate * 0.6)  # Croissance réduite avec Zucman

    # Calcul des KPIs finaux
    final_profit_diff = no_zucman["profits"][-1] - with_zucman["profits"][-1]
    final_employees_diff = no_zucman["employees"][-1] - with_zucman["employees"][-1]
    total_zucman_revenue = sum(with_zucman["state_revenue"]) - sum(no_zucman["state_revenue"])

    kpis = {
        "profit_loss_percent": (final_profit_diff / no_zucman["profits"][-1]) * 100,
        "profit_loss_amount": final_profit_diff,
        "jobs_lost": final_employees_diff,
        "jobs_lost_percent": (final_employees_diff / no_zucman["employees"][-1]) * 100,
        "additional_tax_revenue": total_zucman_revenue,
        "tax_efficiency": total_zucman_revenue / final_profit_diff if final_profit_diff > 0 else 0
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