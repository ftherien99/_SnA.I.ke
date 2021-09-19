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
Bienvenue à SnA.I.ke, le jeu de snake intelligent utilisant la magie de l'apprentissage par renforcement profond! Ce projet contient 3 fonctionnalités principales. Premièrement, vous pourrez jouer au jeu snake de base à l'aide des touches WASD. Ensuite, vous pourrez observer et entraîner l'intelligence artificielle afin que celle-ci apprenne comment jouer au jeu. Finalement, vous allez pouvoir visualiser les données enregistrées lors des simulations en forme de graphiques. Dans ce document, vous trouverez toutes les informations pertinentes afin de bien naviguer dans le programme.

## Installation
Afin de d'assurer le bon fonctionnement du programme, s'il vous plaît suivre ces étapes:
- Installer Python
- Installer Visual Studio Code
- Installer pip
- Installer Pygame grâce à la commande: "pip install pygame"
- Installer Numpy grâce à la commande: "pip install numpy"
- Installer Torch grâce à la commande: "pip install torch"
- Installer Bokeh grâce à la commande: "pip install bokeh"
- Installer Psycopg2 grâce à la commande: "pip install psycopg2"
- Installer pgAdmin4
- À l'aide de pgAdmin4, créer la base de données "snake"
- Aux lignes 14 et 15 du document SnakeDAO, remplacer les informations écrites par les vôtres

## Utilisations
### Jouer une partie
Afin de jouer une partie classique de snake, il faut premièrement cliquer sur le bouton "play" dans le menu principal. Ensuite, plusieurs options seront offertes pour de personnaliser votre expérience. Vous pouvez choisir la couleur des différents aspects du jeu (la tête, le corps et la pomme), la vitesse du serpent ainsi que la grandeur du tableau. Il ne vous reste plus qu'à appuyer sur le bouton "start" et à jouer! Ici, le but du jeu est de ramasser les pommes sans toucher les murs ou votre propre queue. Afin de naviguer dans l'environnement, vous pouvez utiliser les touches WASD sur le clavier. Plus vous mangez de pommes, plus votre serpent sera long, donc prenez garde!

#### Plusieurs options vous sont offertes durant la partie:
- Le bouton "reset" vous permettra de recommencer la partie
- Le bouton "pause" vous permettra de mettre le jeu sur pause (cliquer une autre fois pour continuer la partie)
- Le bouton "quit" vous permettra de quitter la partie et revenir au menu principal
- Vos highscores seront enregistrés selon la grosseur du tableau

### Jouer une simulation
La deuxième fonctionnalité du programme est d'entrainer et de visualiser un agent de snake utilisant de l'apprentissage par renforcement profond. Afin de démarrer une simulation, il faut cliquer sur le bouton "simulation" dans le menu principal. Comme quand on joue une partie, plusieurs options vous seront offertes. Vous pouvez choisir la couleur des aspects du jeu (la tête, le corps et la pomme), le nombre d'épisodes (le nombre de fois que le serpent va jouer) et puis la grandeur du tableau. Il ne vous reste plus qu'à appuyer sur le bouton "start" pour commencer la simulation!

#### Plusieurs options vous sont offertes durant la simulation:
- Le bouton "pause" vous permettra de mettre la simulation sur pause (cliquer une autre fois pour reprendre)
- Le bouton "quit" vous permettra de quitter la simulation et revenir au menu principal
- Les highscores de l'intelligence artificielle seront enregistrés dépendamment de la grosseur du tableau
- Plusieurs informations pertinentes seront affichées à la droite du tableau

### Graphiques
Finalement, nous vous proposons l'option d'analyser les résultats de l'intelligence artificielle en forme de graphiques. Pour ce faire, il faut premièrement cliquer sur le bouton "diagrams". 

#### Plusieurs options seront offertes afin de choisir les données à visualiser:
- Il faut premièrement choisir les données à observer. Vous avez l'option d'analyser le nombre de points par épisode, le nombre de récompenses par épisode, le temps en secondes par épisode et le nombre de pas par épisode.
- Ensuite, vous pouvez choisir de quelle grosseur de tableau provient les données
- Par la suite, cliquer sur le bouton "show graph", qui ouvrira une fenêtre HTML avec le graphique choisit
- Cliquer sur le bouton "main menu" pour revenir au menu principal

## Références
 - Références pour l'apprentissage par renforcement profond: https://youtu.be/wc-FxNENg9U, https://youtu.be/JgvyzIkgxF0, https://youtu.be/zR11FLZ-O9M, Dossier References/DQL dans le git
 - Références pour Bokeh: https://docs.bokeh.org/en/latest/docs/first_steps/first_steps_1.html
 - Références pour Psycopg2: https://www.psycopg.org/docs/
 - Références pour Torch: https://pytorch.org/docs/stable/index.html
 - Références pour Pygame: https://www.pygame.org/docs/, https://youtu.be/4_9twnEduFA
 - Références pour Numpy: https://numpy.org/doc/



## Remerciements
### Remerciement spécial aux personnes qui m'ont aidé durant mon projet:
- Jean-Christophe Demers
- Pierre-Paul Monty