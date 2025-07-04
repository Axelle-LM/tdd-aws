# Projet AWS + Vue

Projet de cours pour comprendre AWS Amplify, DynamoDB et l'importance de tester son code.
L'objectif a été d'ajouter/récupérer des utilisateurs via des lambdas fonctions, et d'utiliser des tests unitaires pour s'assurer de couvrir la plupart des cas.

## Comment ça marche ?

* `add_user()` : Ajoute un user dans une table DynamoDB.
* `get_user()` : Récupère un user grâce à son id.
* `user_handler` : Lambda qui gère les requêtes POST et GET.

## Installation

```bash
# clone
git clone
cd ./proj-aws/amplify

# backend (Python)
python -m venv venv
venv\Scripts\activate
```

## Lancer les tests

```bash
pytest  # devrait tout passer à 100 %
```

Couverture :

```bash
pytest --cov
```