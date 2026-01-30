# Goo Simulation

Jeu de physique où l'objectif est de créer un chemin de "goos" entre deux plateformes.

## Installation

```bash
pip install -r requierements.txt
```

## Lancement

```bash
python main.py
```

## Règles

- Cliquez pour placer des goos qui se connectent automatiquement par ressorts
- Les goos proches (< 20cm) créent des liens élastiques
- Objectif : relier les deux plateformes pendant 3 secondes

## Contrôles

- **Clic gauche** : Placer un goo

## Technologies

- Python 3
- Arcade
