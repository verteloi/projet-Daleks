import msvcrt
import os
from random  import randint

docSymbole = "🔷"
vide = "🔲"
dalekSymbole = "🔶"
feraille = "🔳"

nbVie = 1
nbTeleporteur = 1
nbBlaster = 3
docteurAncienX = 0
docteurAncienY = 0
nbDeplacement = 0
nbDalek = 0
score = 0
niveau = 0
meilleurParties = []

class Docteur:
    def __init__(self, vie, deplacement, x, y):
        self.vieDocteur = vie
        self.zappeur = True
        self.teleporteur = True
        self.deplacementDocteur = deplacement
        self.creditCosmique = 0
        self.position = [x,y]

doc = Docteur(1,1,0,0)

class Dalek:
    def __init__(self, vie, deplacement, valeur, x, y):
        self.vieDalek = vie
        self.deplacementDalek = deplacement
        self.valeurCosmique = valeur
        self.position = [x,y]

collectionDalek:list[Dalek] = []

grille = [
    [docSymbole, vide, vide, vide, vide, vide, vide, vide, vide],
    [vide, vide, vide, vide, vide, vide, vide, vide, vide],
    [vide, vide, vide, vide, vide, vide, vide, vide, vide],
    [vide, vide, vide, vide, vide, vide, vide, vide, vide],
    [vide, vide, vide, vide, vide, vide, vide, vide, vide],
    [vide, vide, vide, vide, vide, vide, vide, vide, vide],
    [vide, vide, vide, vide, vide, vide, vide, vide, vide],
    [vide, vide, vide, vide, vide, vide, vide, vide, vide],
]

def re_initialise():
    global nbVie
    global nbBlaster 
    global docteurAncienX
    global docteurAncienY
    global nbDeplacement
    global nbDalek
    global score
    global grille
    global collectionDalek
    global doc
    global niveau
    global meilleurParties
    global nbTeleporteur

    grille[:] = [  
        [docSymbole, vide, vide, vide, vide, vide, vide, vide, vide],
        [vide, vide, vide, vide, vide, vide, vide, vide, vide],
        [vide, vide, vide, vide, vide, vide, vide, vide, vide],
        [vide, vide, vide, vide, vide, vide, vide, vide, vide],
        [vide, vide, vide, vide, vide, vide, vide, vide, vide],
        [vide, vide, vide, vide, vide, vide, vide, vide, vide],
        [vide, vide, vide, vide, vide, vide, vide, vide, vide],
        [vide, vide, vide, vide, vide, vide, vide, vide, vide],
    ]

    nbVie = 1
    nbBlaster = 3
    nbTeleporteur = 1
    docteurAncienX = 0
    docteurAncienY = 0
    nbDeplacement = 0
    nbDalek = 0
    score = 0
    niveau = 0
    doc = Docteur(vie=1, deplacement=1, x=0, y=0)
    collectionDalek = []

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def deplacer_docteur(grille, nouveauX, nouveauY):
    global doc
    global nbDeplacement
    global niveau
    grille[doc.position[1]][doc.position[0]] = vide
    grille[nouveauY][nouveauX] = docSymbole
    doc.position[0] = nouveauX
    doc.position[1] = nouveauY
    nbDeplacement+=1
    if nbDeplacement % 3 == 0:
        creer_dalek(1, 1, 10)
        niveau += 1

def collision_dalek(dalek: Dalek):
    global score
    global grille
    if grille[dalek.position[1]][dalek.position[0]] == feraille:
        grille[dalek.position[1]][dalek.position[0]] = feraille
        collectionDalek.remove(dalek)
        score += 100
        return True
    else:
        return False

def deplacer_dalek(dalek: Dalek):
    x, y = dalek.position
    direction = randint(0, 3)

    if direction == 0: 
        if y > 0:
            grille[y][x] = vide
            dalek.position[1] -= 1
    elif direction == 1: 
        if x < 9 - 1:
            grille[y][x] = vide
            dalek.position[0] += 1
    elif direction == 2:
        if y < 8 - 1:
            grille[y][x] = vide
            dalek.position[1] += 1
    elif direction == 3:
        if x > 0:
            grille[y][x] = vide
            dalek.position[0] -= 1
    
    if not collision_dalek(dalek):
        grille[dalek.position[1]][dalek.position[0]] = dalekSymbole

def creer_dalek(vie, deplacement, valeur):
    global nbDalek
    while True:
        randomX = randint(0, 8)  
        randomY = randint(0, 7) 
        if grille[randomY][randomX] == vide:
            x, y = randomX, randomY
            break

    dalek = Dalek(vie,deplacement,valeur,x,y)
    collectionDalek.append(dalek)
    grille[y][x] = dalekSymbole
    nbDalek+=1
    
def ferailles():
    global score
    global collectionDalek
    global grille
    destroy = []
    for i in range(len(collectionDalek)):
        for k in range(i + 1, len(collectionDalek)):
            if collectionDalek[i].position == collectionDalek[k].position:
                grille[collectionDalek[i].position[1]][collectionDalek[i].position[0]] = feraille
                if (collectionDalek[i] not in destroy):
                    destroy.append(collectionDalek[i])
                if (collectionDalek[k] not in destroy):
                    destroy.append(collectionDalek[k])
    for dalek in destroy:
        if dalek in collectionDalek:
            collectionDalek.remove(dalek)
            score += 100

def teleporteur(doc: Docteur):
    global nbTeleporteur
    x = doc.position[0]
    y = doc.position[1]
    if nbTeleporteur >= 1:
        teleportValide = False
        while(not teleportValide):
            x = randint(0, 8)
            y = randint(0, 7)
            if(grille[y][x] == vide):
                nbTeleporteur -= 1
                teleportValide = True
    return x,y
    
def afficher_grille(grille):
    for ligne in grille:
        print("".join(ligne))

def on_key_event(keyPressed):
    x, y = doc.position  
    if keyPressed == b'q':
        blaster()
    elif keyPressed == b'e':
        x, y = teleporteur(doc)
    elif keyPressed in [b'\x00', b'\xe0']:
        key2 = msvcrt.getch()
        if key2 == b'H':  
            if y > 0 and grille[y-1][x] != feraille:
                y -= 1
        elif key2 == b'P':  
            if y < len(grille)-1 and grille[y+1][x] != feraille:
                y += 1
        elif key2 == b'K':  
            if x > 0 and grille[y][x-1] != feraille:
                x -= 1
        elif key2 == b'M':  
            if x < len(grille[0])-1 and grille[y][x+1] != feraille:
                x += 1
    return x, y

def afficher_infos(nbBlaster, score, niveau, nbteleporteur):
    print(f"Score : {score}")
    print(f"Niveau : {niveau}")
    print(f"Blaster shot (q) : {nbBlaster}")
    print(f"Teleporteur (e) : {nbTeleporteur}")

def detruire_dalek(x, y):
    global score
    for i in range(len(collectionDalek) - 1, -1, -1):  
        dalek = collectionDalek[i]
        if dalek.position == [x, y]:
            grille[dalek.position[1]][dalek.position[0]] = vide
            score += 100
            del collectionDalek[i]

def blaster():
    global nbBlaster 
    if nbBlaster < 1:
        return False
    else:
        nbBlaster -= 1
        detruire_dalek(doc.position[0], doc.position[1] + 1) 
        detruire_dalek(doc.position[0], doc.position[1] - 1) 
        detruire_dalek(doc.position[0] + 1, doc.position[1]) 
        detruire_dalek(doc.position[0] - 1, doc.position[1]) 
        detruire_dalek(doc.position[0] + 1, doc.position[1] + 1) 
        detruire_dalek(doc.position[0] - 1, doc.position[1] - 1) 
        detruire_dalek(doc.position[0] + 1, doc.position[1] - 1) 
        detruire_dalek(doc.position[0] - 1, doc.position[1] + 1) 

def verifier_collision_docteur_dalek():
    for dalek in collectionDalek:
        if dalek.position == [doc.position[0], doc.position[1]]:
            meilleurParties.append(score)
            print("\033[91mGAME OVER\033[0m")
            menu()

def classement():
    print("Classement des meilleures parties\n\n")
    for i, s in enumerate(sorted(meilleurParties, reverse=True), 1):
        print(f"{i}. {s}")
    print("\nq = Retour au menu")
    choix = msvcrt.getch()
    if choix == b'q':
        cls()
        menu()
    else:
        cls()
        classement()

def menu():
    print("Options\n")
    print("1. jouer")
    print("2. classement")
    choix = msvcrt.getch()
    if choix == b'1':
        cls()
        main_jeu()
    elif choix == b'2':
        cls()
        classement()
    else:
        cls()
        menu()

def main_jeu():
    global nouveauX, nouveauY
    creer_dalek(1,1,10)
    re_initialise()
    afficher_grille(grille)
    afficher_infos(nbBlaster, score, niveau, nbTeleporteur)
    while True:
        keyPressed = msvcrt.getch()
        cls()
        nouveauX, nouveauY = on_key_event(keyPressed)
        deplacer_docteur(grille, nouveauX, nouveauY)
        verifier_collision_docteur_dalek()
        for dalek in collectionDalek:
            deplacer_dalek(dalek)
        verifier_collision_docteur_dalek()
        ferailles()
        afficher_grille(grille)
        afficher_infos(nbBlaster, score, niveau, nbTeleporteur)

if __name__ == "__main__":
    menu()
