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

## Instructions pour Android
Il est également possible d'utiliser notre Whiteboard collaboratif sur Android (avec un support et débugging réduit cependant, notamment en ce qui concerne l'intégration lorsque l'application est passée en background). Pour que l'application et le serveur puissent communiquer, il faut qu'ils soient sur le même réseau local (même wifi par exemple). Voici les étapes :
1/ Récupérer l'addresse IP du serveur avec :
```bash
$ ifconfig
```
et repérer le champ inet addr dans wlan0 par exemple (probablement quelque chose comme 192.168.0.10).

2/ Lancer le serveur :
```bash
$ python server.py
```

3/ Lancer l'application "Whiteboard" sur Android

4/ Rentrer l'IP du serveur et l'id de l'user dans les champs texte prévus pour se connecter au serveur
