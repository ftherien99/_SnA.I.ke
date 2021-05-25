# SnA.I.ke

                                                                       _________         _________
                                                                      /         \       /         \   
                                                                     /  /~~~~~\  \     /  /~~~~~\  \  
                                                                     |  |     |  |     |  |     |  |
                                                                     |  |     |  |     |  |     |  |
                                                                     |  |     |  |     |  |     |  |         /
                                                                     |  |     |  |     |  |     |  |       //
                                                                    (o  o)    \  \_____/  /     \  \_____/ /
                                                                     \__/      \         /       \        /
                                                                      |         ~~~~~~~~~         ~~~~~~~~
                                                                      ^


    Source: https://ascii.co.uk/art/snake   

## Sommaire
Bienvenue à SnA.I.ke, le serpent intelligent utilisant la magie du Deep Reinforcement Learning! Dans ce document, vous trouverez toutes les informations pertinentes afin de bien naviguer dans le programme.

## Installation
Afin de s'assurer le bon fonctionnement du programme, s'il vous plaît suivres ces étapes:
- Installer Python
- Installer Visual Studio Code
- Installer Pygame grâce à la commande: "pip install pygame"
- Installer Numpy grâce à la commande: "pip install numpy"
- Installer Torch grâce à la commande: "pip install torch"
- Installer Bokeh grâce à la commande: "pip install bokeh"
- Installer Psycopg2 grâce à la commande: "pip install psycopg2"
- Installer pgAdmin4
- À l'aide de pgAdmin4, créer la base de données "snake"
- Aux lignes 14 et 15 du document SnakeDAO, remplacer les information écrites par les vôtres

## Utilisations
### Jouer une partie
Afin de jouer une partie classique de snake, il faut premièrement cliquer sur le bouton "play" dans le menu principal. Ensuite, plusieurs options seront offerte afin de personnaliser votre expérience. Vous pouvez choisir la couleur de différents aspects du jeu (la tête, le corps et la pomme), la vitesse du serpent ainsi que la grandeur du tableau. Il ne vous reste plus qu'appuyer sur le bouton "start" et à jouer!

#### Plusieurs options vous sont offertes durant la partie:
- Le bouton "reset" vous permettra de recommencer la partie
- Le bouton "pause" vous permettra de mettre le jeu sur pause (cliquer une autre fois pour continuer la partie)
- Le bouton "quit" vous permettra de quitter la partie et revenir au menu principal
- Vos highscores seront enregistrés tout dépendament de la grosseur du tableau

### Jouer une simulation
La deuxième fonctionnalitée du programme est d'entrainer et de visualiser un agent de snake utilisant de l'apprentissage par renforcement profond. Afin de démarrer une simulation, il faut cliquer sur le bouton "simulation" dans le menu principal. Comme quand on joue une partie, plusieurs options vous seront offertes. Vous pouvez choisir la couleur des aspects du jeu (la tête, le corps et la pomme), le nombre d'épisodes (le nombre de fois que le serpent va jouer) et puis la grandeur du tableau. Il ne vous reste plus qu'appuyer sur le bouton "start" pour commencer la simulation!

#### Plusieurs options vous sont offertes durant la simulation:
- Le bouton "pause" vous permettra de mettre la simulation sur pause (cliquer une autre fois pour reprendre)
- Le bouton "quit" vous permettra de quitter la simulation et revenir au menu principal
- Les highscores de l'intelligence artificielle seront enregistrés dépendamment de la grosseur du tableau
- Plusieurs informations pertinentes seront affichées à la droite du tableau

### Graphiques
Dernièrement, nous vous proposons l'option d'analyser les résultats de l'intelligence artificielle en forme de graphiques. Pour ce faire, il faut premièrement cliquer sur le bouton "diagrams". 

#### Plusieurs options seront offertes afin de choisir les données à visualiser:
- Il faut premièrement choisir les données à observer, vous avez l'option d'analyser le nombre de points par épisodes, le nombre de récompenses par épisode, le temps en secondes par épisode et le nombre de pas par épisodes.
- Ensuite, vous pouvez choisir de quelle grosseure de tableau proviennent le données
- Finaleemnt, cliquer sur le bouton "show graph" ouvrira une fenêtre HTML avec le graphique choisit
- Cliquer sur le bouton "main menu" pour revenir au menu principal

## Références
 - Références pour le deep reinforcement learning: https://youtu.be/wc-FxNENg9U, Dossier References/DQL dans le git
 - Références pour Bokeh: https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_1.html
 - Références pour Psycopg2: https://www.psycopg.org/docs/
 - Références pour Torch: https://pytorch.org/docs/stable/index.html
 - Références pour Pygame: https://www.pygame.org/docs/, https://youtu.be/4_9twnEduFA
 - Références pour Numpy: https://numpy.org/doc/



## Remerciements
### Remerciements spécials au personnes m'ayant aidé dans mon projet
- Jean-Christophe Demers
- Pierre-Paul Monty