#SHOOTER

**Prérequis**

Modifier le nom d'utilisateur et le mot de passe de la base de donnée par vos informations

**Fonctionnement du jeu**

Chaque joueur entrera son pseudo au lancement du jeu. Vous avez ensuite la possibilités de choisir plusieur options. Vous aller ainsi pouvoir choir le layout du jeu, le nombre de vie de chaque joueur et la vitesse du tir de chaque joueur. Le but du jeu est de tuer son adversaire jusqu'a ce qu'il ne possède plus de vie. Vous pourrez vous aider de rebond contre les murs pour plus d'efficacités.

*Enjoy !*

**Note sur le développement du jeu**

Nous avons implémenter une physique à la balle à travers la possibilité de viser et les rebonds sur les murs.
Nous avons ajouter 2 nouveaux écrans que sont l'écran vie, qui permet de choisir le nombre de vie de chaque joueur ainsi que l'écran layout qui permet de choisir le fond du jeu pour permettre au joueur de personnaliser leur expérience de jeu.
Nous avons essayer de connecter le stick arcade sans succès en effet de nombreuses problématique se sont posé tout au long du développement : 
- Au départ nous avons longuement bloqués sur le démarrage du stick en effet la commande pip n'as cesser de nous jouer des tours ce qui nous empecher de mettre en place l'envirronement virtuel nécessaire au stick. Par la suite on a longuement fais fausse routes en pensant récupérer les infos du stick avec la fonction display_info(), on a essayer avec request.form.get notemment sans succès.
- En dernière chance on a décider de partir sur un controller Xbox. Mais la de nouveaux impossible d'utiliser la commande pip et d'installer les packages nécessaire.

Je vous fournit donc nos différentes approche au cours du développement.