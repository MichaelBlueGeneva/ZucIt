# ZucIt

ZucIt est une application Flask qui permet de simuler l'effet de la taxe Zucman. Elle a pour but de montrer "ce qui ne se vois pas", comme disais Hayek.
On choisit une entreprise parmi quelques exemple ou on créé sa propre entreprise. Tout les chiffres sont modifiables. On a la valorisation de l'entreprise, le benefice, le nombre d'employé et la croissance.
Avec un bouton "Zucman GO", on alimente des graphique et des KPI pour montrer l'evolution sur 20 ans du benefice de l'entreprise, du nb employé (on le mettra proportionnel au benefice) et des recettes de l'etat (25% du benefice + 2.857% valorisation si Zucman (2% plus flat tax)). A voir comment montrer le taux de chomage plutot que le nb employé (proportionnel ?)
L'evolution du benefice est en tenant compte de la croissance mais aussi si Zucman en retirant 2.857% valorisation des benefices.
Les KPI sont l'effet de Zucman au bout de 20 ans.
