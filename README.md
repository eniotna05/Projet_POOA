# Projet_POOA
Projet n°06 sur le whiteboard collaboratif.
Pour accéder à la version Android, voir [ici](https://github.com/eniotna05/Projet_POOA/tree/Android)

## Instructions
1/ Installer [Kivy](https://kivy.org/#download) (librarie graphique python). L'installation est détaillée sur leur site et dépend de l'OS utilisé.

2/ Lancer le serveur :
```bash
$ python server.py
```

3/ Lancer autant de clients que désiré :
```bash
$ python main.py
```

4/ Pour que les clients soient connectés et puissent échanger des dessins, ils doivent choisir des noms uniques dans la popup de lancement. L'utilisateur doit également choisir l'IP du serveur auquel il souhaite se connecter. Il est fortement recommandé d'être sur le même réseau LAN (même réseau wifi par exemple).

Si le serveur est lancé sur la même machine que le client, simplement écrire _localhost_ connectera le client au serveur local.

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


### Bugs connus
- Un bug intervient parfois lorsqu'un client se connecte, crée de nombreuses
images et ensuite un autre client se connecte, toutes les images créées
précèdemment ne sont pas récupéré. Le problème ne se situe pas au niveau de
notre base de donné car tout est bien récupéré. Il se situe au niveau du canvas
kivy qui très probablement ne parvient pas à éxécuter de nombreuses informations
données à la suite. La modification de l'horloge kivy ou la mise en place de buffer
ne résoudent pas le problème.
- Concernant l'écriture du texte, la mise à l'échelle telle que nous l'avions pensée est impossible à réaliser sous Kivy : il est impossible de redimensionner la taille texture du texte a posteriori en fonction du cadre que l'utilisateur a tracé. Pour contourner le problème, il faudrait demander avant l'écriture à l'utilisateur la taille de police qu'il souhaiterait utiliser.
