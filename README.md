# Battle-IA — Ultimate Tic-Tac-Toe

Un jeu de morpion géant en console, écrit en Python, pour jouer contre une IA Minimax avec élagage alpha-bêta.

## Lancer le jeu

Python 3 est nécessaire. Aucune dépendance externe à installer.

```sh
python ultimate_tic_tac_toe.py
```

Choisis qui commence : `1` pour le joueur ou `2` pour l'IA. Le joueur humain utilise les X et l'IA les O. À chaque tour, saisis la colonne puis la ligne, entre 1 et 9.

## Règles

- Le plateau contient neuf mini-plateaux de morpion.
- La position du coup dans un mini-plateau détermine le mini-plateau où l'adversaire doit jouer.
- Si ce mini-plateau est déjà gagné ou terminé, l'adversaire peut jouer dans n'importe quel mini-plateau encore ouvert.
- Aligne trois mini-plateaux gagnés pour remporter la partie.

## Intelligence artificielle

L'IA utilise Minimax, l'élagage alpha-bêta et un tri des coups favorisant les victoires locales, les centres et les coins. La partie utilise une profondeur de recherche de 6 ; le temps de réflexion dépend de la position et de la machine.

Le code source fourni est conservé tel quel.

