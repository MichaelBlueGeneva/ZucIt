# Méthodes d'estimation de l'impact sur l'emploi

## 1. Méthode Proportionnelle Simple (Actuelle)

**Principe :** L'emploi est directement proportionnel au profit de l'entreprise.

**Formule :** `Employés = Profit × Ratio_initial`

**Avantages :**
- Simple à calculer et comprendre
- Relation directe profit/emploi

**Inconvénients :**
- Trop simpliste, ne considère pas l'inertie RH
- Peut créer des variations irréalistes
- Ne tient pas compte des coûts fixes d'emploi

**Implémentation :**
```python
employee_ratio = employees_initial / profit_initial
current_employees = max(min_employees, int(current_profit * employee_ratio))
```

## 2. Méthode Élasticité Emploi-Profit

**Principe :** Utilise un coefficient d'élasticité économétrique entre emploi et profit.

**Formule :** `Δ Emploi % = Élasticité × Δ Profit %`

**Paramètres :**
- Élasticité emploi-profit : 0.3 à 0.7 selon le secteur
- Tech/services : 0.3-0.4 (capital-intensif)
- Industrie : 0.5-0.6 (main-d'œuvre importante)
- Commerce : 0.6-0.7 (labour-intensif)

**Avantages :**
- Basé sur des données économétriques réelles
- Varie selon le secteur d'activité
- Plus réaliste que la proportionnalité directe

**Implémentation :**
```python
elasticity = 0.4  # Pour tech/services
profit_change_pct = (current_profit - initial_profit) / initial_profit
employment_change_pct = elasticity * profit_change_pct
current_employees = initial_employees * (1 + employment_change_pct)
```

## 3. Méthode avec Inertie et Délais

**Principe :** L'ajustement de l'emploi suit les changements de profit avec un délai et une inertie.

**Paramètres :**
- Délai d'ajustement : 1-3 ans
- Coefficient d'inertie : 0.2-0.4 par période
- Coûts de licenciement/embauche

**Formule :** `Emploi_t = Emploi_t-1 + α × (Emploi_cible - Emploi_t-1)`

**Avantages :**
- Reflète la réalité des ajustements RH
- Évite les variations brutales
- Considère les coûts de transaction

**Implémentation :**
```python
adjustment_speed = 0.3  # 30% d'ajustement par an
target_employees = calculate_target_from_profit(current_profit)
current_employees = previous_employees + adjustment_speed * (target_employees - previous_employees)
```

## 4. Méthode Seuils de Rentabilité

**Principe :** L'emploi suit des paliers selon la rentabilité de l'entreprise.

**Seuils :**
- Profit > 15% CA : Embauche active (+3-5% emploi/an)
- Profit 5-15% CA : Maintien effectifs
- Profit 0-5% CA : Réduction modérée (-2-5% emploi/an)
- Profit < 0% : Restructuration (-10-20% emploi/an)

**Avantages :**
- Reflète les décisions managériales réelles
- Intègre les contraintes de trésorerie
- Évite la sur-réaction aux fluctuations mineures

**Implémentation :**
```python
profit_margin = current_profit / revenue
if profit_margin > 0.15:
    employment_growth = 0.04  # +4%
elif profit_margin > 0.05:
    employment_growth = 0.0   # Maintien
elif profit_margin > 0:
    employment_growth = -0.03 # -3%
else:
    employment_growth = -0.15 # -15%
```

## 5. Méthode Mixte Productivité-Demande

**Principe :** Combine l'impact de la productivité et de la demande sur l'emploi.

**Composantes :**
- Effet productivité : Taxe → Moins d'investissement → Baisse productivité → Plus d'emploi pour même production
- Effet demande : Taxe → Prix plus élevés → Moins de demande → Moins d'emploi
- Effet net = Effet demande - Effet productivité

**Paramètres :**
- Élasticité prix-demande : -0.5 à -2.0
- Impact investissement sur productivité : 10-30%
- Part de la taxe reportée sur les prix : 50-80%

**Avantages :**
- Modèle économique complet
- Considère les mécanismes de marché
- Peut capturer des effets contre-intuitifs

**Implémentation :**
```python
# Effet productivité
investment_reduction = zucman_tax * 0.6
productivity_impact = investment_reduction * 0.2
employment_from_productivity = productivity_impact * 0.3

# Effet demande
price_increase = zucman_tax * 0.7  # 70% reporté sur prix
demand_reduction = price_increase * demand_elasticity
employment_from_demand = demand_reduction * 0.8

# Effet net
net_employment_change = employment_from_demand + employment_from_productivity
```

## Recommandations d'usage

**Pour ZucIt :** Utiliser la **Méthode 3 (Inertie et Délais)** comme méthode principale car elle :
- Évite les variations brutales irréalistes
- Reflète mieux la réalité des ajustements RH
- Reste compréhensible pour les utilisateurs

**Paramètres suggérés :**
- Délai d'ajustement : 2 ans
- Vitesse d'ajustement : 25% par an
- Plancher minimum : 5-10% des effectifs initiaux
- Élasticité emploi-profit : 0.4 (secteur tech)