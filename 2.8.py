# ECHEC

import pyxel

pyxel.init(128, 128, title="Échec")
pyxel.mouse(True)

pyxel.load("my_resource.pyxres", True, True, True, True)
    
echiquier = [[0] * 8 for loop in range (8)]
jeu = "en attente"
commencer = 0

case_gauche = "" #Case selectionné clic gauche
tab_case_droite = [] #Tab avec les coordonees valides pour un clic droite


def remplir_chiquier_initiallement(tab, jeu):
    """Prends un tableau vide et met les pieces conforme le jeu choisi"""
    global commencer
    
    if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        if pyxel.mouse_x <= 64:
            jeu = "echecs"
        else:
            jeu = "dames"
            
    if jeu == "echecs":
        for i in range(8):
            tab[1][i] = "1b0" #ligne de pions bleu
            tab[6][i] = "1r0" #ligne de pions roses
            
        tab[0][1], tab[0][6] = "2b", "2b" #chevaux bleu
        tab[7][1], tab[7][6] = "2r", "2r" #chevaux rose
        
        tab[0][0], tab[0][7] = "3b", "3b" #tours bleu
        tab[7][0], tab[7][7] = "3r", "3r" #tours rose
        
        tab[0][3] = "4b" #reine bleu
        tab[7][3] = "4r" #reine rose
        
        tab[0][2], tab[0][5] = "5b", "5b" #fou bleu
        tab[7][2], tab[7][5] = "5r", "5r" #fou rose
        
        tab[0][4] = "6b" #roi bleu
        tab[7][4] = "6r" #roi rose
        
        commencer = 1
            
    elif jeu == "dames":
        for j in range(1, 8, 2):
            tab[0][j] = "7b" #dame bleu
            tab[1][j-1] = "7b"
            tab[2][j] = "7b"
            
            tab[5][j-1] = "7r" #dame rouge
            tab[6][j] = "7r"
            tab[7][j-1] = "7r"
                
        commencer = 1
                
    return tab
        
    
def echiquier_vide():
    """Dessine un échiquier vide au fond"""
    
    couleur_1 = 7
    couleur_2 = 4
    
    for i in range(8):
        for j in range(8):
            if i % 2 == 0:
                if j % 2 == 0:
                    pyxel.rect(j * 16, i * 16, 16, 16, couleur_1)
                else:
                    pyxel.rect(j * 16, i * 16, 16, 16, couleur_2)
            else:
                if j % 2 == 0:
                    pyxel.rect(j * 16, i * 16, 16, 16, couleur_2)
                else:
                    pyxel.rect(j * 16, i * 16, 16, 16, couleur_1)
                    
def dessiner_piece(tab):
    """Dessine une piece qui est dans tab
    0 est supposé une case vide"""
    
    for i in range(8):
        for j in range(8):
            
            case = tab[i][j]
            
            if case != 0: #Case non vide
                
                piece = int(case[0]) #Piece = 1 ou 2 .. ou 6
                couleur = case[1] #Couleur = b ou r
                
                if couleur == "b":
                    ligne_couleur = 0
                    
                elif couleur == "r":
                    ligne_couleur = 16
                
                if piece == 1: #Dessine un pion
                    pyxel.blt(j * 16, i * 16, 0, 0, ligne_couleur, 16, 16, 11)
                elif piece == 2: #Dessine un cheval
                    pyxel.blt(j * 16, i * 16, 0, 16, ligne_couleur, 16, 16, 11)
                elif piece == 3: #Dessine une tour
                    pyxel.blt(j * 16, i * 16, 0, 32, ligne_couleur, 16, 16, 11)
                elif piece == 4: #Dessine une reine
                    pyxel.blt(j * 16, i * 16, 0, 48, ligne_couleur, 16, 16, 11)
                elif piece == 5: #Dessine un fou
                    pyxel.blt(j * 16, i * 16, 0, 64, ligne_couleur, 16, 16, 11)
                elif piece == 6: #Dessine un roi
                    pyxel.blt(j * 16, i * 16, 0, 80, ligne_couleur, 16, 16, 11)
                elif piece == 7: #Dessine une dame
                    pyxel.blt(j * 16, i * 16, 0, 96, ligne_couleur, 16, 16, 11)
                    
def clic_case():
    """Le clic de la souris correspond à une position dans le tableau"""
    return pyxel.mouse_y  // 16, pyxel.mouse_x // 16


def valide_mouvement_pion():
    """Renvoie le nombre de fois qu'on a jouer avec le pion"""
    
def encadre(case: tuple) -> bool:
    """Fonction qui renvoie True si les valeurs dans case
    si 0 <= case <= 7
    False sinon"""
    return (case[0] >= 0) and (case[0] <= 7) and (case[1] >= 0) and (case[1] <= 7) 

def valide(clic: tuple, tab: list) -> list:
    """Renvoie un tableau tab avec des coordonnes valides pour rentrer dans l'échiquier"""
    global echiquier
    x = clic[0]
    y = clic[1]
    case = echiquier[x][y]
    
    if case == 0:
        return []
    
    piece = case[0]
    couleur = case[1]
    tab = []
    #coordonnes valides pour un pion
    if piece == "1":
        direction = 1 #vers le bas
        if couleur == "r":
            direction = -1 #vers le haut
        mouv = 1
        if case[2] == "0":
            mouv += 1 #si le pion n'a pas bouge"
            
        for i in range(mouv):
            devant = (clic[0]+(i*direction)+(1*direction),clic[1])
            if encadre(devant) and (echiquier[devant[0]][devant[1]] == 0):
                tab.append((devant[0],devant[1])) #devant
            
            #vers la droite si elle n'est pas vide
            if i == 0: #seulement au premier mouvement
                droite = (clic[0]+(i*direction)+(1*direction),clic[1]+1) 
                if encadre(droite) and (echiquier[droite[0]][droite[1]] != 0):
                    tab.append((droite[0],droite[1]))
            
            #vers la gauche si elle n'est pas vide
            if i == 0: #seulement au premier mouvement
                gauche = (clic[0]+(i*direction)+(1*direction),clic[1]-1)
                if encadre(gauche) and (echiquier[gauche[0]][gauche[1]] != 0):
                    tab.append((gauche[0],gauche[1]))

    #coordonnes valides pour un cheval
    if piece == "2":
        tab =[(clic[0]-2,clic[1]+1), (clic[0]-2,clic[1]-1),(clic[0]+2,clic[1]+1),
              (clic[0]+2,clic[1]-1),(clic[0]+1,clic[1]+2), (clic[0]+1,clic[1]-2),
              (clic[0]-1,clic[1]+2),(clic[0]-1,clic[1]-2)]
    #coordonnes valides pour une tour
    if piece == "3":
        for i in range(0,8):
            tab.append((clic[0],clic[1]+1+i))
            if not encadre((clic[0],clic[1]+1+i)) or echiquier[clic[0]][clic[1]+1+i] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0],clic[1]-1-i))
            if not encadre((clic[0],clic[1]-1-i)) or echiquier[clic[0]][clic[1]-1-i] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0]+1+i,clic[1]))
            if not encadre((clic[0]+1+i,clic[1])) or echiquier[clic[0]+1+i][clic[1]] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0]-1-i,clic[1]))
            if not encadre((clic[0]-1-i,clic[1])) or echiquier[clic[0]-1-i][clic[1]] != 0:
                break
    if piece == "4":
        for i in range(0,8):
            tab.append((clic[0],clic[1]+1+i))
            if not encadre((clic[0],clic[1]+1+i)) or echiquier[clic[0]][clic[1]+1+i] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0],clic[1]-1-i))
            if not encadre((clic[0],clic[1]-1-i)) or echiquier[clic[0]][clic[1]-1-i] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0]+1+i,clic[1]))
            if not encadre((clic[0]+1+i,clic[1])) or echiquier[clic[0]+1+i][clic[1]] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0]-1-i,clic[1]))
            if not encadre((clic[0]-1-i,clic[1])) or echiquier[clic[0]-1-i][clic[1]] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0]+1+i,clic[1]+1+i))
            if not encadre((clic[0]+1+i,clic[1]+1+i)) or echiquier[clic[0]+1+i][clic[1]+1+i] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0]-1-i,clic[1]-1-i))
            if not encadre((clic[0]-1-i,clic[1]-1-i)) or echiquier[clic[0]-1-i][clic[1]-1-i] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0]+1+i,clic[1]-1-i))
            if not encadre((clic[0]+1+i,clic[1]-1-i)) or echiquier[clic[0]+1+i][clic[1]-1-i] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0]-1-i,clic[1]+1+i))
            if not encadre((clic[0]-1-i,clic[1]+1+i)) or echiquier[clic[0]-1-i][clic[1]+1+i] != 0:
                break
        
    if piece == "5":
        for i in range(0,8):
            tab.append((clic[0]+1+i,clic[1]+1+i))
            if not encadre((clic[0]+1+i,clic[1]+1+i)) or echiquier[clic[0]+1+i][clic[1]+1+i] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0]-1-i,clic[1]-1-i))
            if not encadre((clic[0]-1-i,clic[1]-1-i)) or echiquier[clic[0]-1-i][clic[1]-1-i] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0]+1+i,clic[1]-1-i))
            if not encadre((clic[0]+1+i,clic[1]-1-i)) or echiquier[clic[0]+1+i][clic[1]-1-i] != 0:
                break
        for i in range(0,8):
            tab.append((clic[0]-1-i,clic[1]+1+i))
            if not encadre((clic[0]-1-i,clic[1]+1+i)) or echiquier[clic[0]-1-i][clic[1]+1+i] != 0:
                break
    if piece == "6":
        tab = [(clic[0]-1,clic[1]+1), (clic[0]-1,clic[1]-1),(clic[0]+1,clic[1]+1),
              (clic[0]+1,clic[1]-1),(clic[0]+1,clic[1]),
              (clic[0]-1,clic[1]),(clic[0],clic[1]+1),(clic[0],clic[1]-1)]
    
    #On enleve le pieces avec la même couleur que case
    tab = collision(couleur, tab)
    return tab

def collision(couleur: str, tab: list) -> list:
    """Fonction qui vérifie si les cases ne sont pas de la même couleur du clic
    ou si elle est vide, alors on la met dans tab_non_collision"""
    global echiquier
    
    tab_non_collision = []
    
    for case in tab:
        if encadre(case):
            piece_case = echiquier[case[0]][case[1]]
            if (piece_case == 0) or (piece_case[1] != couleur):
                tab_non_collision.append(case)
            
    return tab_non_collision

def update():
    global case_gauche, tab_case_droite
    
    if commencer == 0:
        remplir_chiquier_initiallement(echiquier, jeu)
        
    if commencer == 1:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #Ici le joueur selectionne une case
            case_gauche = clic_case()
            tab_case_droite = valide(case_gauche, tab_case_droite)
            #Les mouvements possibles rentrent dans tab_case_droite
        
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            #Ici le joueur selectionne où bouger la piece
            clic_temp = clic_case()
            for case_test in tab_case_droite:
                if clic_temp == case_test:
                    #La case est valide et on fait le mouvement
                    case = echiquier[case_gauche[0]][case_gauche[1]]
                    
                    if case[0] == "1": #Si c'est un pion
                        case = f"1{case[1]}1" #il ne peut plus avancer 2 cases
                        
                    echiquier[clic_temp[0]][clic_temp[1]] = case #mouvement
                    echiquier[case_gauche[0]][case_gauche[1]] = 0
                    #On vide le variables de mouvement
                    case_gauche = ""
                    tab_case_droite = []
                    
                    
def draw():     
    if commencer == 0:
        pyxel.rect(0, 0, 64, 128, 6)
        pyxel.rect(64, 0, 64, 128, 8)
        
        pyxel.text(20, 50, "ECHECS", 7)
        pyxel.blt(24, 56, 0, 16, 16, 16, 16, 11)
        
        pyxel.text(86, 50, "DAMES", 7)
        pyxel.blt(88, 56, 0, 96, 0, 16, 16, 11)
        
    if commencer == 1:
        echiquier_vide()

        if case_gauche != "":
            pyxel.rect(case_gauche[1] * 16, case_gauche[0] * 16, 16, 16, 5)
        for case_droite in tab_case_droite:
            pyxel.rect(case_droite[1] * 16, case_droite[0] * 16, 16, 16, 8)
    
        dessiner_piece(echiquier)
            
pyxel.run(update, draw)