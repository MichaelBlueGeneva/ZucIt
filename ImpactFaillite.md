# Méthodes d'estimation du risque de faillite

## 1. Méthode Score Z d'Altman (Modifiée)

**Principe :** Utilise le célèbre Z-Score d'Altman adapté pour intégrer l'impact de la taxe Zucman.

**Formule Z-Score modifiée :**
```
Z = 1.2×(Fonds_roulement/Actif) + 1.4×(Bénéfices_non_distribués/Actif)
    + 3.3×(EBIT/Actif) + 0.6×(Valeur_marché/Dettes) + 1.0×(CA/Actif)
```

**Seuils de risque :**
- **Z > 2.99** : Zone sûre (faible risque faillite)
- **1.81 < Z < 2.99** : Zone grise (risque modéré)
- **Z < 1.81** : Zone de détresse (risque élevé)

**Impact Taxe Zucman :**
- Réduit EBIT directement
- Diminue les bénéfices non distribués
- Augmente le poids des dettes (valorisation impactée)

**Avantages :**
- Méthode éprouvée scientifiquement
- Utilisée par les banques et investisseurs
- Intègre plusieurs ratios financiers

**Implémentation :**
```python
def calculate_z_score(working_capital, total_assets, retained_earnings,
                     ebit, market_value, total_debt, sales):
    z_score = (1.2 * working_capital/total_assets +
               1.4 * retained_earnings/total_assets +
               3.3 * ebit/total_assets +
               0.6 * market_value/total_debt +
               1.0 * sales/total_assets)

    if z_score > 2.99:
        return "Sûr"
    elif z_score > 1.81:
        return "Risque modéré"
    else:
        return "Risque élevé"
```

## 2. Méthode Seuil de Trésorerie Critique

**Principe :** Prédit la faillite quand la trésorerie devient insuffisante pour honorer les obligations.

**Mécanisme :**
1. Calcul des flux de trésorerie avec taxe Zucman
2. Projection des besoins (salaires, dettes, fournisseurs)
3. Identification du point où trésorerie < besoins critiques

**Variables clés :**
- Trésorerie initiale
- Flux de trésorerie opérationnels (après taxe)
- Charges fixes incompressibles
- Échéancier de dettes

**Formule :**
```
Trésorerie_t = Trésorerie_t-1 + Flux_opérationnels_t - Charges_fixes_t - Taxe_Zucman_t
```

**Seuil critique :** 3-6 mois de charges fixes

**Avantages :**
- Approche très concrète et pratique
- Donne une date précise de risque
- Facile à comprendre pour les dirigeants

**Implémentation :**
```python
def months_to_bankruptcy(cash, operating_cf, fixed_costs, zucman_tax):
    monthly_burn = (fixed_costs + zucman_tax) / 12 - operating_cf / 12
    if monthly_burn <= 0:
        return float('inf')  # Pas de risque
    return cash / monthly_burn
```

## 3. Méthode Ratio de Couverture des Intérêts

**Principe :** Mesure la capacité à honorer les charges financières avec l'EBITDA réduit.

**Formule :** `Ratio = EBITDA / Charges_financières`

**Seuils d'alerte :**
- **Ratio > 4** : Situation saine
- **2 < Ratio < 4** : Surveillance nécessaire
- **1.2 < Ratio < 2** : Difficulté financière
- **Ratio < 1.2** : Risque de défaut imminent

**Impact Taxe Zucman :**
- Réduit l'EBITDA disponible
- Peut dégrader rapidement le ratio
- Affecte la notation de crédit

**Avantages :**
- Utilisé par les agences de notation
- Indicateur précoce de difficultés
- Lié aux covenants bancaires

**Implémentation :**
```python
def coverage_ratio_analysis(ebitda, financial_charges, zucman_impact):
    adjusted_ebitda = ebitda - zucman_impact
    ratio = adjusted_ebitda / financial_charges

    if ratio > 4:
        return "Sain", 0
    elif ratio > 2:
        return "Surveillance", 1
    elif ratio > 1.2:
        return "Difficulté", 2
    else:
        return "Défaut imminent", 3
```

## 4. Méthode Simulation Monte Carlo

**Principe :** Simule de multiples scénarios économiques pour estimer la probabilité de faillite.

**Variables aléatoires :**
- Croissance du chiffre d'affaires (loi normale)
- Inflation des coûts (loi log-normale)
- Taux d'intérêt (processus stochastique)
- Chocs sectoriels (loi de Poisson)

**Mécanisme :**
1. Génération de 10 000 scénarios
2. Application de la taxe Zucman dans chaque scénario
3. Calcul du pourcentage de scénarios menant à la faillite

**Critères de faillite :**
- Capitaux propres négatifs pendant 2 ans
- Incapacité à honorer les dettes > 6 mois
- Pertes cumulées > 80% de la valorisation

**Avantages :**
- Capture l'incertitude économique
- Donne une probabilité chiffrée
- Peut tester différents niveaux de taxe

**Implémentation :**
```python
def monte_carlo_bankruptcy(initial_conditions, zucman_tax, n_simulations=10000):
    bankruptcy_count = 0

    for i in range(n_simulations):
        # Générer scénario aléatoire
        growth_rates = np.random.normal(0.05, 0.1, 20)  # 20 ans
        cost_inflation = np.random.lognormal(0.02, 0.05, 20)

        # Simuler évolution avec Zucman
        equity = initial_equity
        for year in range(20):
            revenue_growth = growth_rates[year]
            cost_growth = cost_inflation[year]
            # ... calculs avec impact Zucman

            if equity < -initial_equity * 0.5:  # Critère faillite
                bankruptcy_count += 1
                break

    return bankruptcy_count / n_simulations
```

## 5. Méthode Analyse de Sensibilité Multi-Variables

**Principe :** Identifie les combinaisons de variables qui mènent à la faillite.

**Variables testées :**
- Niveau de taxe Zucman (0.5% à 5%)
- Croissance économique (-2% à +8%)
- Taux d'intérêt (1% à 10%)
- Élasticité prix-demande
- Niveau d'endettement initial

**Méthode :**
1. Définition d'un plan d'expérience (grid search)
2. Calcul de l'impact pour chaque combinaison
3. Mapping des zones de faillite
4. Identification des variables critiques

**Résultats :**
- Cartographie des risques
- Seuils critiques pour chaque variable
- Variables les plus impactantes
- Scénarios de stress-test

**Avantages :**
- Vision complète des vulnérabilités
- Permet l'optimisation des politiques
- Identifie les leviers de protection

**Implémentation :**
```python
def sensitivity_analysis():
    results = {}

    # Définir les plages de test
    zucman_rates = np.linspace(0.005, 0.05, 10)
    growth_rates = np.linspace(-0.02, 0.08, 11)
    interest_rates = np.linspace(0.01, 0.10, 10)

    for zr in zucman_rates:
        for gr in growth_rates:
            for ir in interest_rates:
                # Simuler scenario
                years_to_bankruptcy = simulate_scenario(zr, gr, ir)
                results[(zr, gr, ir)] = years_to_bankruptcy

    return results
```

## Disponibilité des Données Publiques

### Données Facilement Accessibles
- **Chiffre d'affaires** : Rapports annuels, bilans comptables
- **Bénéfices/Pertes** : Comptes de résultat publics
- **Capitalisation boursière** : Données de marché temps réel
- **Nombre d'employés** : Rapports sociaux, LinkedIn, estimations
- **Dette totale** : Bilans comptables (dettes court + long terme)

### Données Partiellement Accessibles
- **Trésorerie** : Souvent dans les bilans consolidés (grandes entreprises)
- **EBITDA** : Calculable à partir des données comptables publiques
- **Charges financières** : Notes aux comptes, rapports détaillés

### Données Difficiles d'Accès
- **Flux de trésorerie opérationnels détaillés** : PME/startups privées
- **Répartition des investissements** : Information stratégique
- **Covenants bancaires** : Contrats privés

## Méthodes Adaptées aux Données ZucIt

### Méthode 1: Ratio Dette/Valorisation Simplifié
**Données requises :** Valorisation (donnée), Estimation dette (2x profit annuel)
```python
def debt_ratio_risk(valuation, estimated_debt):
    ratio = estimated_debt / valuation
    if ratio > 0.7: return "Risque élevé"
    elif ratio > 0.4: return "Risque modéré"
    else: return "Risque faible"
```

### Méthode 2: Burn Rate sur Profit
**Données requises :** Profit, Taxe Zucman, Charges fixes estimées
```python
def profit_burn_analysis(profit, zucman_tax, growth_rate):
    net_profit_after_tax = profit - zucman_tax
    if net_profit_after_tax < 0:
        # Calcul années avant épuisement des réserves
        estimated_reserves = profit * 2  # 2 ans de profit en réserve
        monthly_burn = abs(net_profit_after_tax) / 12
        months_to_bankruptcy = estimated_reserves / monthly_burn
        return f"Faillite dans {months_to_bankruptcy:.1f} mois"
    return "Profitable"
```

### Méthode 3: Seuil de Rentabilité Critique
**Données requises :** Profit, Valorisation, Taux de croissance
```python
def profitability_threshold_risk(profit, valuation, zucman_tax):
    profit_margin = profit / (profit / 0.1)  # Estimation CA avec marge 10%

    # Seuils critiques basés sur la marge
    if profit_margin < 0.02:  # < 2% marge
        return "Faillite imminente"
    elif profit_margin < 0.05:  # < 5% marge
        return "Zone rouge"
    elif profit_margin < 0.10:  # < 10% marge
        return "Zone orange"
    else:
        return "Zone verte"
```

## Recommandations d'usage pour ZucIt

**Méthode recommandée :** **Combinaison 2+3** (Burn Rate + Seuils de Rentabilité)

### Implémentation Pratique pour ZucIt:
```python
def zucit_bankruptcy_risk(valuation, profit, employees, zucman_tax):
    # Méthode 2: Analyse Burn Rate
    net_profit = profit - zucman_tax
    if net_profit < 0:
        estimated_reserves = valuation * 0.05  # 5% de la valorisation en réserves
        monthly_burn = abs(net_profit) / 12
        months_survival = estimated_reserves / monthly_burn

        if months_survival < 6:
            return "Faillite imminente (< 6 mois)"
        elif months_survival < 18:
            return "Difficulté sévère (< 18 mois)"
        else:
            return "Situation tendue mais gérable"

    # Méthode 3: Seuils de rentabilité
    estimated_revenue = profit / 0.08  # Marge nette 8% typique
    new_margin = net_profit / estimated_revenue

    if new_margin < 0:
        return "Pertes - Restructuration nécessaire"
    elif new_margin < 0.02:
        return "Marge critique - Risque faillite"
    elif new_margin < 0.05:
        return "Marge faible - Surveillance"
    else:
        return "Situation financière stable"

# Intégration dans ZucIt
def add_bankruptcy_kpi(simulation_results):
    final_profit = simulation_results["with_zucman"]["profits"][-1]
    final_valuation = simulation_results["with_zucman"]["valuations"][-1]
    final_zucman_tax = final_valuation * 0.02857

    bankruptcy_risk = zucit_bankruptcy_risk(
        final_valuation, final_profit, 1000, final_zucman_tax
    )

    simulation_results["kpis"]["bankruptcy_risk"] = bankruptcy_risk
    return simulation_results
```

### Avantages de cette approche:
- **Utilise uniquement les données disponibles dans ZucIt**
- **Méthodes simples et explicables** aux utilisateurs
- **Résultats concrets** : nombre de mois ou état qualitatif
- **Adaptable** selon le profil d'entreprise (startup vs grande entreprise)

Cette approche pragmatique permet d'estimer le risque de faillite sans données comptables complexes, en se basant sur les paramètres déjà disponibles dans la simulation ZucIt.