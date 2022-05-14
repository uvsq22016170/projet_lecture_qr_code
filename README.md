Ce projet permet de lire et créer un QR code de taille 25x25.

Type de données possible : ascii ou hexadécimal
    Longueur maximum du message : 16 pour de l'ascii et 32 pour de l'hexadécimal
Filtres possibles : - pas de filtre
                    - damier (la case en haut à gauche noire)
                    - lignes horizontales alternées noires et blanches (la plus haute est noire)
                    - lignes verticales alternées noires et blanches (la plus à gauche est noire)

Au lancement du programme une fenêtre s'ouvre.
Les différentes fonctions possibles sont déclenchées par les deux boutons suivants :
    - Lire un QR code : Ouvre une fenêtre pour choisir un QR code, décode en fonction du filtre et du format des données et affiche les information contenues dans ce QR  code.
    - Créer le QR code : Affiche et sauvegarde un QR code à partir : - des informations à écrire dans le QR code
                                                                     - du format des données choisi
                                                                     - du filtre choisi
                                                                     - du nom du QR code