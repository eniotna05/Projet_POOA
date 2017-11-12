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
