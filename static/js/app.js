// Configuration globale des graphiques
Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif';
Chart.defaults.font.size = 12;
Chart.defaults.color = '#64748b';

class ZucItApp {
    constructor() {
        this.charts = {};
        this.currentCompany = null;
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.loadDefaultCompany();
    }

    setupEventListeners() {
        // Boutons de sélection d'entreprise
        document.querySelectorAll('.company-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.selectCompany(e.target.dataset.company);
            });
        });

        // Soumission du formulaire
        document.getElementById('simulation-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.runSimulation();
        });
    }

    selectCompany(companyId) {
        // Mise à jour visuelle des boutons
        document.querySelectorAll('.company-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-company="${companyId}"]`).classList.add('active');

        if (companyId === 'custom') {
            this.loadCustomCompany();
        } else {
            this.loadCompanyData(companyId);
        }
    }

    async loadCompanyData(companyId) {
        try {
            const response = await fetch(`/company/${companyId}`);
            const company = await response.json();

            if (company.error) {
                console.error('Erreur:', company.error);
                return;
            }

            this.currentCompany = company;
            this.populateForm(company);
        } catch (error) {
            console.error('Erreur lors du chargement:', error);
        }
    }

    loadCustomCompany() {
        this.currentCompany = null;
        // Garder les valeurs actuelles du formulaire pour l'entreprise personnalisée
    }

    loadDefaultCompany() {
        this.selectCompany('apple'); // Charger Apple par défaut
    }

    populateForm(company) {
        document.getElementById('company-name').value = company.name;
        document.getElementById('valuation').value = company.valuation / 1000000000; // Convertir en milliards
        document.getElementById('profit').value = company.profit / 1000000; // Convertir en millions
        document.getElementById('employees').value = company.employees;
        document.getElementById('growth-rate').value = company.growth_rate * 100; // Convertir en pourcentage
    }

    async runSimulation() {
        const formData = this.getFormData();

        // Afficher l'état de chargement
        this.showLoading(true);

        try {
            const response = await fetch('/simulate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const results = await response.json();
            this.displayResults(results);
        } catch (error) {
            console.error('Erreur lors de la simulation:', error);
            alert('Erreur lors de la simulation. Veuillez réessayer.');
        } finally {
            this.showLoading(false);
        }
    }

    getFormData() {
        return {
            valuation: parseFloat(document.getElementById('valuation').value) * 1000000000, // Convertir milliards en euros
            profit: parseFloat(document.getElementById('profit').value) * 1000000, // Convertir millions en euros
            employees: parseInt(document.getElementById('employees').value),
            growth_rate: parseFloat(document.getElementById('growth-rate').value)
        };
    }

    showLoading(show) {
        const btn = document.querySelector('.zucman-btn');
        if (show) {
            btn.textContent = '⏳ Simulation en cours...';
            btn.disabled = true;
        } else {
            btn.textContent = '🚀 ZUCMAN GO !';
            btn.disabled = false;
        }
    }

    displayResults(results) {
        // Afficher la section des résultats
        const resultsSection = document.getElementById('results-section');
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });

        // Afficher les KPIs
        this.displayKPIs(results.kpis);

        // Créer les graphiques
        this.createCharts(results);

        // Afficher l'analyse détaillée
        this.displayAnalysis(results);
    }

    displayKPIs(kpis) {
        // Perte de bénéfices
        document.getElementById('profit-loss-percent').textContent =
            `${kpis.profit_loss_percent.toFixed(1)}%`;
        document.getElementById('profit-loss-amount').textContent =
            `${this.formatCurrency(kpis.profit_loss_amount)} perdus`;

        // Emplois perdus
        document.getElementById('jobs-lost-percent').textContent =
            `${kpis.jobs_lost_percent.toFixed(1)}%`;
        document.getElementById('jobs-lost').textContent =
            `${kpis.jobs_lost.toLocaleString()} emplois`;

        // Hausse des prix
        document.getElementById('price-increase-percent').textContent =
            `+${kpis.price_increase_percent.toFixed(1)}%`;

        // Recettes supplémentaires de l'État (avec gestion du signe et coloring)
        const revenueCard = document.getElementById('revenue-kpi-card');
        const revenueTitle = document.getElementById('revenue-kpi-title');
        const revenueAmount = this.formatCurrencyMillions(kpis.additional_tax_revenue);

        if (kpis.additional_tax_revenue >= 0) {
            revenueTitle.textContent = '🏛️ Recettes État supplémentaires';
            document.getElementById('additional-tax-revenue').textContent = `+${revenueAmount} M€`;
            revenueCard.className = 'kpi-card positive';
        } else {
            revenueTitle.textContent = '🏛️ Recettes État perdues';
            document.getElementById('additional-tax-revenue').textContent = `${revenueAmount} M€`; // Le - est déjà inclus
            revenueCard.className = 'kpi-card negative';
        }

        document.getElementById('tax-efficiency').textContent =
            `${kpis.tax_efficiency.toFixed(2)}€ récupérés / 1€ taxé`;
    }

    createCharts(results) {
        // Détruire les graphiques existants
        Object.values(this.charts).forEach(chart => chart.destroy());
        this.charts = {};

        const years = results.years;
        const noZucman = results.no_zucman;
        const withZucman = results.with_zucman;

        // Graphique des bénéfices
        this.charts.profit = new Chart(document.getElementById('profit-chart'), {
            type: 'line',
            data: {
                labels: years,
                datasets: [
                    {
                        label: 'Sans Zucman',
                        data: noZucman.profits,
                        borderColor: '#059669',
                        backgroundColor: 'rgba(5, 150, 105, 0.1)',
                        borderWidth: 3,
                        fill: true
                    },
                    {
                        label: 'Avec Zucman',
                        data: withZucman.profits,
                        borderColor: '#dc2626',
                        backgroundColor: 'rgba(220, 38, 38, 0.1)',
                        borderWidth: 3,
                        fill: true
                    }
                ]
            },
            options: this.getChartOptions('Bénéfices (€)', true)
        });

        // Graphique des emplois
        this.charts.employees = new Chart(document.getElementById('employees-chart'), {
            type: 'line',
            data: {
                labels: years,
                datasets: [
                    {
                        label: 'Sans Zucman',
                        data: noZucman.employees,
                        borderColor: '#059669',
                        backgroundColor: 'rgba(5, 150, 105, 0.1)',
                        borderWidth: 3,
                        fill: true
                    },
                    {
                        label: 'Avec Zucman',
                        data: withZucman.employees,
                        borderColor: '#dc2626',
                        backgroundColor: 'rgba(220, 38, 38, 0.1)',
                        borderWidth: 3,
                        fill: true
                    }
                ]
            },
            options: this.getChartOptions('Nombre d\'employés', false)
        });

        // Graphique des recettes fiscales
        this.charts.revenue = new Chart(document.getElementById('revenue-chart'), {
            type: 'bar',
            data: {
                labels: years,
                datasets: [
                    {
                        label: 'Sans Zucman',
                        data: noZucman.state_revenue,
                        backgroundColor: 'rgba(5, 150, 105, 0.7)',
                        borderColor: '#059669',
                        borderWidth: 1
                    },
                    {
                        label: 'Avec Zucman',
                        data: withZucman.state_revenue,
                        backgroundColor: 'rgba(37, 99, 235, 0.7)',
                        borderColor: '#2563eb',
                        borderWidth: 1
                    }
                ]
            },
            options: this.getChartOptions('Recettes fiscales (€)', true)
        });

        // Graphique des valorisations
        this.charts.valuation = new Chart(document.getElementById('valuation-chart'), {
            type: 'line',
            data: {
                labels: years,
                datasets: [
                    {
                        label: 'Sans Zucman',
                        data: noZucman.valuations,
                        borderColor: '#059669',
                        backgroundColor: 'rgba(5, 150, 105, 0.1)',
                        borderWidth: 3,
                        fill: true
                    },
                    {
                        label: 'Avec Zucman',
                        data: withZucman.valuations,
                        borderColor: '#dc2626',
                        backgroundColor: 'rgba(220, 38, 38, 0.1)',
                        borderWidth: 3,
                        fill: true
                    }
                ]
            },
            options: this.getChartOptions('Valorisation (€)', true)
        });

        // Graphique des prix
        this.charts.prices = new Chart(document.getElementById('prices-chart'), {
            type: 'line',
            data: {
                labels: years,
                datasets: [
                    {
                        label: 'Sans Zucman',
                        data: noZucman.prices,
                        borderColor: '#059669',
                        backgroundColor: 'rgba(5, 150, 105, 0.1)',
                        borderWidth: 3,
                        fill: true
                    },
                    {
                        label: 'Avec Zucman',
                        data: withZucman.prices,
                        borderColor: '#dc2626',
                        backgroundColor: 'rgba(220, 38, 38, 0.1)',
                        borderWidth: 3,
                        fill: true
                    }
                ]
            },
            options: this.getChartOptions('Index des prix (base 100)', false)
        });
    }

    getChartOptions(yAxisLabel, isCurrency) {
        return {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Année'
                    },
                    grid: {
                        color: 'rgba(226, 232, 240, 0.5)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: yAxisLabel
                    },
                    grid: {
                        color: 'rgba(226, 232, 240, 0.5)'
                    },
                    ticks: {
                        callback: isCurrency ?
                            (value) => this.formatCurrency(value, true) :
                            (value) => value.toLocaleString()
                    }
                }
            }
        };
    }

    displayAnalysis(results) {
        const analysisDiv = document.getElementById('detailed-analysis');
        const kpis = results.kpis;

        const companyName = document.getElementById('company-name').value;

        let analysis = `
            <p><strong>Analyse pour ${companyName} :</strong></p>

            <p>La simulation sur 20 ans révèle un impact significatif de la taxe Zucman :</p>

            <p><strong>💸 Impact économique négatif :</strong></p>
            <ul>
                <li>Perte de bénéfices cumulés : <strong>${this.formatCurrency(kpis.profit_loss_amount)}</strong> (${kpis.profit_loss_percent.toFixed(1)}%)</li>
                <li>Destruction d'emplois : <strong>${kpis.jobs_lost.toLocaleString()}</strong> postes (${kpis.jobs_lost_percent.toFixed(1)}%)</li>
                <li>Réduction de la capacité d'investissement et d'innovation</li>
            </ul>

            <p><strong>🏛️ Recettes fiscales :</strong></p>
            <ul>
                <li>Recettes supplémentaires pour l'État : <strong>${this.formatCurrency(kpis.additional_tax_revenue)}</strong></li>
                <li>Efficacité fiscale : <strong>${kpis.tax_efficiency.toFixed(2)}€</strong> collectés pour chaque euro de richesse détruite</li>
            </ul>
        `;

        if (kpis.tax_efficiency < 1) {
            analysis += `
                <p><strong>⚠️ Attention :</strong> L'efficacité fiscale est inférieure à 1, ce qui signifie que la taxe détruit plus de richesse qu'elle n'en collecte. Cet effet correspond à ce que Frédéric Bastiat appelait "ce qui ne se voit pas" - les conséquences économiques indirectes et négatives des politiques fiscales.</p>
            `;
        }

        analysisDiv.innerHTML = analysis;
    }

    formatCurrency(amount, short = false) {
        if (short && Math.abs(amount) >= 1000000000) {
            return (amount / 1000000000).toFixed(1) + 'Md€';
        } else if (short && Math.abs(amount) >= 1000000) {
            return (amount / 1000000).toFixed(1) + 'M€';
        } else if (short && Math.abs(amount) >= 1000) {
            return (amount / 1000).toFixed(0) + 'k€';
        }

        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }

    formatCurrencyMillions(amount) {
        return (amount / 1000000).toFixed(1);
    }
}

// Initialiser l'application quand le DOM est chargé
document.addEventListener('DOMContentLoaded', () => {
    new ZucItApp();
});