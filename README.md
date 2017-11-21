# Projet_POOA
Projet n°05 sur le whiteboard collaboratif.

## Instructions
1/ Installer [Kivy](https://kivy.org/docs/gettingstarted/installation.html) (librarie graphique python) :

2/ Lancer le serveur :
```bash
$ python server.py
```

3/ Lancer autant de clients que désiré :
```bash
$ python main.py
```

4/ Pour que les clients soient connectés et puissent échanger des dessins, ils doivent prendre des noms uniques dans le cadre prévu à cet affet et faire "Enter".

## Précisions sur le code

### Structure des strings transmises par socket
1 lettre pour préciser la commande souhaités + les paramètres en fonction de la commande, séparés par des virgules + un point pour indiquer la fin de la string.
Les paramètres peuvent être des coordonnées de points, des longueurs ou la couleur de la forme par exemple.

### Commandes implémentées
- C : créer un object Circle
- E : créer un object Ellipse
- S : créer un object Square
- R : créer un object Rectangle
- L : créer un object Line
- P : créer un object Picture
- T : créer un object Text

- Q : quitter le serveur
- H : "Hello", utilisé pour le handshake à l'ouverture de la connection
- D : supprimer un objet (Delete)
- Z : demander la suppression d'un objet (DeleteRequest)
- N : refuser la suppression d'un objet (NegativeAnswer)

### Conventions de nommage
Pour les objets qui sont partagés par plusieurs threads et passés en référence
lors de la construction des objets les contenant, on les considère comme publics
(on accède in fine au même objet en mémoire).
Les variables des objets Kivy hérités ne respectent pas les conventions de
nommage avec "\_" ou "\__"


### Bugs détectés
- Un bug intervient parfois lorsqu'un client se connecte, crée de nombreuses
images et ensuite un autre client se connecte, toutes les images créées
précèdemment ne sont pas récupéré. Le problème ne se situe pas au niveau de
notre base de donné car tout est bien récupéré. Il se situe au niveau du canvas
kivy qui très probablement ne parvient pas à éxécuter de nombreuses informations
données à la suite. La modification de l'horloge kivy ou la mise en place de buffer
ne résoudent pas le problème.
