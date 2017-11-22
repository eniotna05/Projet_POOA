# Projet_POOA
Projet n°05 sur le whiteboard collaboratif.
Pour accéder à la version Desktop, voir [ici](https://github.com/eniotna05/Projet_POOA/)

## Disclaimer
Attention, par manque de temps, le débugging a été réduit sur la version Android, (notamment en ce qui concerne l'intégration spécifique, lorsque l'application est passée en background ou sur le support portrait / paysage par exemple).

## Instructions pour Android
1/ Télécharger le paquet _Whiteboard-1.0.apk_ dans le dossier _bin/_, le mettre sur son téléphone et l'installer.

2/ Lancer le serveur depuis un ordinateur :
```bash
$ python server.py
```

3/ Ouvrir l'application sur son smartphone

4/ Pour que les clients soient connectés et puissent échanger des dessins, ils doivent choisir des noms uniques dans la popup de lancement. L'utilisateur doit également choisir l'IP du serveur auquel il souhaite se connecter. Il est fortement recommandé d'être sur le même réseau LAN (même réseau wifi par exemple).

## Précisions sur le code

### Compilation spécifique

Nous utilisons le projet [Buildozer](https://github.com/kivy/buildozer) qui permet de porter du code python3 utilisant Kivy sous Android. Le travail a donc consisté à installer la chaine de compilation spécifique pour Android et à paramétrer le fichier _buildozer.spec_ définissant les étapes de la compilation.

Une fois le projet correctement paramétré, on compile une nouvelle version avec :
```bash
$ buildozer android deploy run
```

Une application iOS pourrait théoriquement être compilé en suivant un processus similaire.

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
