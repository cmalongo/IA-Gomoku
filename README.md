# Gomoku AI

## Description

Ce projet implémente une **Intelligence Artificielle (IA) pour le jeu du Gomoku** en utilisant **Python** et **NumPy**. 
L'objectif est de développer une IA compétitive respectant des contraintes de performance et de temps d'exécution.

L'IA repose sur l'**algorithme Minimax** avec **élagage alpha-bêta** et diverses heuristiques avancées.

## Auteurs

- **Gabriel Maccione**
- **Cyrille Malongo**
- **Antoine Lin**
- **Merwane Mallem**

## Fonctionnalités

- **Affichage textuel du plateau**
- **Gestion des règles officielles du Gomoku**
- **Implémentation d'une IA avancée avec Minimax**
- **Prise en compte de plusieurs heuristiques défensives et offensives**
- **Restriction des coups noirs sur les premiers tours**

## Installation

1. Assurez-vous d'avoir **Python 3** installé.
2. Installez les dépendances requises avec la commande suivante :
   ```bash
   pip install numpy
   ```
3. Exécutez le fichier **Gomoku_code.py** pour lancer une partie.

## Utilisation

Exécutez le script avec :
```bash
python Gomoku_code.py
```
L'utilisateur peut choisir de jouer en tant que **Noir (N) ou Blanc (B)**.

## Règles Spécifiques Implémentées

- **Le premier coup noir est forcé au centre du plateau.**
- **Le second coup noir doit être en dehors du carré central de 7x7 cases.**
- **La victoire est déterminée par un alignement de 5 pions (horizontal, vertical ou diagonal).**

## Stratégies d'IA

### Défensives :
- **Blocage d'un alignement de 4 pions adverses** (xxxx_ → xxxx0)
- **Blocage d'un alignement de 3 pions adverses** (xxx_ → xxx0)
- **Blocage d'un alignement de 2 pions adverses avec un espace** (xx_x → xx0x)

### Offensives :
- **Création d'une double menace de 4 pions** (permet d'assurer une victoire rapide)
- **Attaque prioritaire lorsqu'un alignement de 3 pions est détecté**
- **Stratégie d'ouverture offensive pour les noirs**

## Optimisations et Contraintes

- **Limitation du temps d'exécution à 10 secondes par coup**
- **Réduction des heuristiques pour équilibrer la performance et la vitesse**

## Conclusion

Ce projet a permis de développer une **IA robuste et compétitive** pour le jeu du Gomoku. 
L'utilisation d'un algorithme **Minimax avec élagage alpha-bêta** et l'intégration d'heuristiques avancées ont permis 
d'optimiser le comportement de l'IA en attaque comme en défense.

