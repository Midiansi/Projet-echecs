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

#Pour les echecs
en_passant = [] #Tableau pour appliquer la regle en passant
mouvement_precedent = (0, 1)
roque = [] #Tableau pour faire le mouvement roque

#Pour les dames
dames_manger = [] #Tableau pour pour manger les pieces dans le jeu de dames
nb_pieceB, nb_pieceR = 0, 0

compteur_mouv = 0 #Variable qui va compter combien de fois les pieces ont bouge
vainqueur = "aucun"

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
        
        tab[0][0], tab[0][7] = "3b0", "3b0" #tours bleu
        tab[7][0], tab[7][7] = "3r0", "3r0" #tours rose
        
        tab[0][3] = "4b" #reine bleu
        tab[7][3] = "4r" #reine rose
        
        tab[0][2], tab[0][5] = "5b", "5b" #fou bleu
        tab[7][2], tab[7][5] = "5r", "5r" #fou rose
        
        tab[0][4] = "6b0" #roi bleu
        tab[7][4] = "6r0" #roi rose
        
        commencer = 1
            
    elif jeu == "dames":
        for j in range(1, 8, 2):
            tab[0][j] = "7b" #pierre bleu
            tab[1][j-1] = "7b"
            tab[2][j] = "7b"
            
            tab[5][j-1] = "7r" #pierre rose
            tab[6][j] = "7r"
            tab[7][j-1] = "7r"
                
        commencer = 1
                
    return tab, jeu
        
    
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
                elif piece == 7: #Dessine une pierre
                    pyxel.blt(j * 16, i * 16, 0, 96, ligne_couleur, 16, 16, 11)
                elif piece == 8: #dessine une dame 
                    pyxel.blt(j * 16, i * 16, 0, 112, ligne_couleur, 16, 16, 11)
                    
                    
def clic_case():
    """Le clic de la souris correspond à une position dans le tableau"""
    return pyxel.mouse_y  // 16, pyxel.mouse_x // 16
    
def encadre(case: tuple) -> bool:
    """Fonction qui renvoie True si les valeurs dans case
    si 0 <= case <= 7
    False sinon"""
    return (case[0] >= 0) and (case[0] <= 7) and (case[1] >= 0) and (case[1] <= 7) 

def valide(clic: tuple, tab: list) -> list:
    """Renvoie un tableau tab avec des coordonnes valides pour rentrer dans l'échiquier"""
    global echiquier, en_passant, mouvement_precedent, dames_manger, roque
    x = clic[0]
    y = clic[1]
    case = echiquier[x][y]
    
    if case == 0:
        return []
    
    piece = case[0]
    couleur = case[1]
    tab = []
    
    en_passant = []
    dames_manger = []
    roque = []
    
    #coordonnes valides pour un pion
    if piece == "1":
        direction = 1 #vers le bas
        if couleur == "r":
            direction = -1 #vers le haut
        mouv = 1
        if case[2] == "0":
            mouv += 1 #si le pion n'a pas bouge"
            
        limite_devant = 0 #variable pour ne pas sauter une autre au deuxieme tour de boucle
            
        for i in range(mouv):
            if i == 1 and limite_devant == 1:
                break #on s'arrete pour ne pas sauter une case devant
            
            devant = (clic[0]+(i*direction)+(1*direction),clic[1])
            if encadre(devant) and (echiquier[devant[0]][devant[1]] == 0):
                tab.append(devant) #devant
            else:
                limite_devant = 1 #on ne pourra pas sauter une case
            
            #vers la droite si elle n'est pas vide
            if i == 0: #seulement au premier mouvement
                droite = (clic[0]+(i*direction)+(1*direction),clic[1]+1) 
                if encadre(droite) and (echiquier[droite[0]][droite[1]] != 0):
                    tab.append(droite)
                    
                #regle en passant pour la droite
                passant_d = (clic[0], clic[1] + 1)
                if encadre(passant_d) and encadre(droite) and\
                   (passant_d == mouvement_precedent):
                    piece_passant = echiquier[passant_d[0]][passant_d[1]]
                    piece_droite = echiquier[droite[0]][droite[1]]
                    
                    if piece_droite == 0 and piece_passant != 0 and\
                       piece_passant[0] == "1" and piece_passant[2] == "1":
                        tab.append((droite[0],droite[1]))
                        en_passant += [droite, passant_d]
                   
                #vers la gauche si elle n'est pas vide
                gauche = (clic[0]+(i*direction)+(1*direction),clic[1]-1)
                if encadre(gauche) and (echiquier[gauche[0]][gauche[1]] != 0):
                    tab.append(gauche)
                
                #regle en passant pour la gauche
                passant_g = (clic[0], clic[1] - 1)
                if encadre(passant_g) and encadre(gauche) and\
                   (passant_g == mouvement_precedent):
                    piece_passant = echiquier[passant_g[0]][passant_g[1]]
                    piece_gauche = echiquier[gauche[0]][gauche[1]]
                    
                    if piece_gauche == 0 and piece_passant != 0 and\
                       piece_passant[0] == "1" and piece_passant[2] == "1":
                        tab.append((gauche[0],gauche[1]))
                        en_passant += [gauche, passant_g]

    #coordonnes valides pour un cheval
    elif piece == "2":
        tab =[(clic[0]-2,clic[1]+1), (clic[0]-2,clic[1]-1),(clic[0]+2,clic[1]+1),
              (clic[0]+2,clic[1]-1),(clic[0]+1,clic[1]+2), (clic[0]+1,clic[1]-2),
              (clic[0]-1,clic[1]+2),(clic[0]-1,clic[1]-2)]
    #coordonnes valides pour une tour
    elif piece == "3":
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
        
        #Test du mouvement roque pour un roi a droite
        roi_droite = (clic[0], clic[1] + 4)
        if encadre(roi_droite) and case[2] == "0"\
           and echiquier[roi_droite[0]][roi_droite[1]] != 0 and\
           echiquier[clic[0]][clic[1]+1] == 0 and \
           echiquier[clic[0]][clic[1]+2] == 0 and echiquier[clic[0]][clic[1]+3] == 0 and\
           echiquier[roi_droite[0]][roi_droite[1]][0] == "6" and\
           echiquier[roi_droite[0]][roi_droite[1]][2] == "0":
            tab.append(roi_droite)
            roque += [roi_droite, (clic[0], clic[1] + 2), clic, (clic[0], clic[1] +3)]
            #Roque prends ou est le roi, ou mettre la tour et ou mettre le roi
        
        #Test du mouvement roque pour un roi a gauche
        roi_gauche = (clic[0], clic[1] - 3)
        if encadre(roi_gauche) and case[2] == "0"\
           and echiquier[roi_gauche[0]][roi_gauche[1]] != 0 and\
           echiquier[clic[0]][clic[1]-1] == 0 and echiquier[clic[0]][clic[1]-2] == 0 and\
           echiquier[roi_gauche[0]][roi_gauche[1]][0] == "6" and\
           echiquier[roi_gauche[0]][roi_gauche[1]][2] == "0":
            tab.append(roi_gauche)
            roque += [roi_gauche, (clic[0], clic[1]-1), clic, (clic[0],clic[1]-2)]
        
    #coordonnes valides pour un reine
    elif piece == "4":
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
    #coordonnes valides pour un fou
    elif piece == "5":
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
    #coordonnes valides pour un roi
    elif piece == "6":
        tab = [(clic[0]-1,clic[1]+1), (clic[0]-1,clic[1]-1),(clic[0]+1,clic[1]+1),
              (clic[0]+1,clic[1]-1),(clic[0]+1,clic[1]),
              (clic[0]-1,clic[1]),(clic[0],clic[1]+1),(clic[0],clic[1]-1)]
        
        #Test pour faire le roque avec un tour a gauche
        tour_gauche = (clic[0],clic[1]-4)
        if encadre(tour_gauche) and echiquier[tour_gauche[0]][tour_gauche[1]] != 0\
           and case[2] == "0" and\
           echiquier[clic[0]][clic[1]-1] == 0 and echiquier[clic[0]][clic[1]-2] == 0 and\
           echiquier[clic[0]][clic[1]-3] == 0 and\
           echiquier[tour_gauche[0]][tour_gauche[1]][0] == "3" and\
           echiquier[tour_gauche[0]][tour_gauche[1]][2] == "0":
            tab.append(tour_gauche)
            roque += [clic, (clic[0],clic[1]-2), tour_gauche, (clic[0],clic[1]-1)]
            
        #Test pour faire le roque avec une tour a droite
        tour_droite = (clic[0],clic[1]+3)
        if encadre(tour_droite) and echiquier[tour_droite[0]][tour_droite[1]] != 0\
           and case[2] == "0" and\
           echiquier[clic[0]][clic[1]+1] == 0 and echiquier[clic[0]][clic[1]+2] == 0 and\
           echiquier[tour_droite[0]][tour_droite[1]][0] == "3" and\
           echiquier[tour_droite[0]][tour_droite[1]][2] == "0":
            tab.append(tour_droite)
            roque += [clic, (clic[0],clic[1]+2), tour_droite, (clic[0],clic[1]+1)]        
        
    #coordonnes valides pour une pierre:
    elif piece == "7":
        direction = 1 #vers le bas
        if couleur == "r":
            direction = -1 #vers le haut
            
        gauche = (clic[0]+(1*direction),clic[1]-1)
        if encadre(gauche) and (echiquier[gauche[0]][gauche[1]] == 0):
            tab.append(gauche)
        
        droite = (clic[0]+(1*direction),clic[1]+1)
        if encadre(droite) and (echiquier[droite[0]][droite[1]] == 0):
            tab.append(droite)
            
        haut_gauche_manger = (clic[0]-2,clic[1]-2) #test si on peut manger en haut a gauche
        if gauche != (haut_gauche_manger[0]+1, haut_gauche_manger[1]+1):
            gauche = (clic[0]-1,clic[1]-1) #on inverse gauche
            #pour faire le test de la gauche oppose
            
        if encadre(haut_gauche_manger) and (echiquier[gauche[0]][gauche[1]] != 0)\
           and (echiquier[gauche[0]][gauche[1]][1] != couleur) and\
           echiquier[haut_gauche_manger[0]][haut_gauche_manger[1]] == 0:
            #si la case loin est vide et la case pres est de couleur oppose
            dames_manger += [(haut_gauche_manger),(gauche)]
            tab = [] #on enleve tout deplacement, manger devient obligatoire
            for i in range(0, len(dames_manger), 2):
                tab += [dames_manger[i]]
        
        haut_droite_manger = (clic[0]-2,clic[1]+2) #test si on peut manger en haut a droite
        if droite != (haut_droite_manger[0]+1, haut_droite_manger[1]-1):
            droite = (clic[0]-1, clic[1]+1) #on inverse droite
            #pour faire le test de la droite oppose
            
        if encadre(haut_droite_manger) and (echiquier[droite[0]][droite[1]] != 0)\
           and (echiquier[droite[0]][droite[1]][1] != couleur) and\
           echiquier[haut_droite_manger[0]][haut_droite_manger[1]] == 0:
            #si la case loin est vide et la case pres est de couleur oppose
            dames_manger += [(haut_droite_manger),(droite)]
            tab = [] #on enleve tout deplacement, manger devient obligatoire
            for i in range(0, len(dames_manger), 2):
                tab += [dames_manger[i]]
        
        bas_gauche_manger = (clic[0]+2,clic[1]-2) 
        if gauche != (bas_gauche_manger[0]+1, bas_gauche_manger[1]-1):
            gauche = (clic[0]+1,clic[1]-1)
            
        if encadre(bas_gauche_manger) and (echiquier[gauche[0]][gauche[1]] != 0)\
           and (echiquier[gauche[0]][gauche[1]][1] != couleur) and\
           echiquier[bas_gauche_manger[0]][bas_gauche_manger[1]] == 0:
            #si la case loin est vide et la case pres est de couleur oppose
            dames_manger += [(bas_gauche_manger),(gauche)]
            tab = [] #on enleve tout deplacement, manger devient obligatoire
            for i in range(0, len(dames_manger), 2):
                tab += [dames_manger[i]]
            
        bas_droite_manger = (clic[0]+2,clic[1]+2)
        if droite != (bas_droite_manger[0]-1, bas_droite_manger[1]-1):
            droite = (clic[0]+1, clic[1]+1)
            
        if encadre(bas_droite_manger) and (echiquier[droite[0]][droite[1]] != 0)\
           and (echiquier[droite[0]][droite[1]][1] != couleur) and\
           echiquier[bas_droite_manger[0]][bas_droite_manger[1]] == 0:
            #si la case loin est vide et la case pres est de couleur oppose
            dames_manger += [(bas_droite_manger),(droite)]
            tab = [] #on enleve tout deplacement, manger devient obligatoire
            for i in range(0, len(dames_manger), 2):
                tab += [dames_manger[i]]
        
    #coordonnes valides pour une dame:
    elif piece == "8":
        
        for i in range(0,8):
            haut_gauche = (clic[0]-1-i,clic[1]-1-i)
            if encadre(haut_gauche) and (echiquier[haut_gauche[0]][haut_gauche[1]] == 0) and dames_manger == []:
                tab.append(haut_gauche)
            
            haut_gauche_manger = (haut_gauche[0]-1,haut_gauche[1]-1)

            if encadre(haut_gauche_manger) and (echiquier[haut_gauche[0]][haut_gauche[1]] != 0)\
               and (echiquier[haut_gauche[0]][haut_gauche[1]][1] != couleur) and\
               echiquier[haut_gauche_manger[0]][haut_gauche_manger[1]] == 0:
                #si la case loin est vide et la case pres est de couleur oppose
                dames_manger += [(haut_gauche_manger),(haut_gauche)]
                tab = [] #on enleve tout deplacement, manger devient obligatoire
                for i in range(0, len(dames_manger), 2):
                    tab += [dames_manger[i]]
   
            if not encadre(haut_gauche) or echiquier[haut_gauche[0]][haut_gauche[1]] != 0:
                break
        
        for i in range(0,8):
            haut_droite = (clic[0]-1-i,clic[1]+1+i)
            if encadre(haut_droite) and (echiquier[haut_droite[0]][haut_droite[1]] == 0) and dames_manger == []:
                                        #si la case est vide 
                tab.append(haut_droite)
            
            haut_droite_manger = (haut_droite[0]-1,haut_droite[1]+1)

            if encadre(haut_droite_manger) and (echiquier[haut_droite[0]][haut_droite[1]] != 0)\
               and (echiquier[haut_droite[0]][haut_droite[1]][1] != couleur) and\
               echiquier[haut_droite_manger[0]][haut_droite_manger[1]] == 0:
                #si la case loin est vide et la case pres est de couleur oppose
                dames_manger += [(haut_droite_manger),(haut_droite)]
                tab = [] #on enleve tout deplacement, manger devient obligatoire
                for i in range(0, len(dames_manger), 2):
                    tab += [dames_manger[i]]
            
            if not encadre(haut_droite) or echiquier[haut_droite[0]][haut_droite[1]] != 0:
                break
        
        for i in range(0,8):
            bas_gauche = (clic[0]+1+i,clic[1]-1-i)
            if encadre(bas_gauche) and (echiquier[bas_gauche[0]][bas_gauche[1]] == 0) and dames_manger == []:
                tab.append(bas_gauche)
            
            bas_gauche_manger = (bas_gauche[0]+1,bas_gauche[1]-1)

            if encadre(bas_gauche_manger) and (echiquier[bas_gauche[0]][bas_gauche[1]] != 0)\
               and (echiquier[bas_gauche[0]][bas_gauche[1]][1] != couleur) and\
               echiquier[bas_gauche_manger[0]][bas_gauche_manger[1]] == 0:
                #si la case loin est vide et la case pres est de couleur oppose
                dames_manger += [(bas_gauche_manger),(bas_gauche)]
                tab = [] #on enleve tout deplacement, manger devient obligatoire
                for i in range(0, len(dames_manger), 2):
                    tab += [dames_manger[i]]
            
            if not encadre(bas_gauche) or echiquier[bas_gauche[0]][bas_gauche[1]] != 0:
                break
            
        for i in range(0,8):
            bas_droite = (clic[0]+1+i,clic[1]+1+i)
            if encadre(bas_droite) and (echiquier[bas_droite[0]][bas_droite[1]] == 0) and dames_manger == []:
                tab.append(bas_droite)
            
            bas_droite_manger = (bas_droite[0]+1,bas_droite[1]+1)

            if encadre(bas_droite_manger) and (echiquier[bas_droite[0]][bas_droite[1]] != 0)\
               and (echiquier[bas_droite[0]][bas_droite[1]][1] != couleur) and\
               echiquier[bas_droite_manger[0]][bas_droite_manger[1]] == 0:
                #si la case loin est vide et la case pres est de couleur oppose
                dames_manger += [(bas_droite_manger),(bas_droite)]
                tab = [] #on enleve tout deplacement, manger devient obligatoire
                for i in range(0, len(dames_manger), 2):
                    tab += [dames_manger[i]]
            
            if not encadre(bas_droite) or echiquier[bas_droite[0]][bas_droite[1]] != 0:
                break
        
    #On enleve le pieces avec la même couleur que case
    tab = collision(piece, couleur, tab)
    return tab

def collision(piece: str, couleur: str, tab: list) -> list:
    """Fonction qui vérifie si les cases ne sont pas de la même couleur du clic
    ou si elle est vide, alors on la met dans tab_non_collision"""
    global echiquier, roque
    
    tab_non_collision = []
    
    for i in range(0, len(roque), 4):
        if echiquier[roque[i][0]][roque[i][1]][0] == piece: #Si on fait un mouvement avec un roi
            tab_non_collision.append(roque[i+2]) #On laisse le joueur cliquer sur la tour
        elif echiquier[roque[i+2][0]][roque[i+2][1]][0] == piece: #Si on fait un mouvement avec une tour
            tab_non_collision.append(roque[i]) #On laisse le joueur cliquer sur le roi
            
    for case in tab:
        if encadre(case):
            piece_case = echiquier[case[0]][case[1]]
            if (piece_case == 0) or (piece_case[1] != couleur):
                #tab_non_collision prends les cases vides ou de couleur opposes
                tab_non_collision.append(case)
            
    return tab_non_collision

def promotion(case: tuple, couleur: str):
    """Lorsqu'il y a une promotion, on dessine les options et ou est la case a promouvoir"""
    if couleur == "b":
        ligne_couleur = 0
                    
    elif couleur == "r":
        ligne_couleur = 16
    
    #On dessine le pion a la case ou il etait
    pyxel.blt(case[1] * 16, case[0] * 16, 0, 0, ligne_couleur, 16, 16, 11)
    
    #On dessine les pieces a choisir
    pyxel.blt(16*2, 16*3, 0, 16, ligne_couleur, 16, 16, 11) #Cheval
    pyxel.blt(16*3, 16*3, 0, 16*2, ligne_couleur, 16, 16, 11) #Tour
    pyxel.blt(16*4, 16*3, 0, 16*3, ligne_couleur, 16, 16, 11) #Reine
    pyxel.blt(16*5, 16*3, 0, 16*4, ligne_couleur, 16, 16, 11) #Fou
    
    pyxel.text(16*2-3, 16*3-6, "Cliquer sur la piece", 0)

def update():
    global case_gauche, tab_case_droite, commencer, compteur_mouv, vainqueur, echiquier, jeu, en_passant,\
           mouvement_precedent, dames_manger, nb_pieceB, nb_pieceR, roque, prom_coord, prom_couleur
    
    if commencer == 0: #en attente d'une selection de mode
        echiquier, jeu = remplir_chiquier_initiallement(echiquier, jeu)
        
    elif commencer == 1:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            #Ici le joueur selectionne une case
            case_gauche = clic_case()
            piece_gauche = echiquier[case_gauche[0]][case_gauche[1]]
            #Piece de la case clique
            
            precedent = echiquier[mouvement_precedent[0]][mouvement_precedent[1]]
            
            tab_case_droite = valide(case_gauche, tab_case_droite)
            
            #Les mouvements possibles rentrent dans tab_case_droite
            if not (jeu == "dames" and dames_manger != []) and not (precedent == 0)\
               and not (piece_gauche == 0) and not(precedent[1] != piece_gauche[1]):
                case_gauche = ""
                tab_case_droite = []

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            #Ici le joueur selectionne où bouger la piece
            clic_temp = clic_case()
            for case_test in tab_case_droite:
                if clic_temp == case_test:
                    #La case est valide et on fait le mouvement
                    case = echiquier[case_gauche[0]][case_gauche[1]]
                    
                    if case[0] == "1":
                        if case[2] == "0": #Si c'est un pion qui n'a pas avance
                            if clic_temp == (case_gauche[0]+2, case_gauche[1])\
                                           or clic_temp == (case_gauche[0]-2, case_gauche[1]):
                                case = f"1{case[1]}1" #elle avance 2 cases au premier tour
                            else:
                                case = f"1{case[1]}2" #elle avance 1 case au premier tour
                        elif case[2] == "1": #Si c'est un pion qui a avance 2 fois au premier tour
                            case = f"1{case[1]}2" #il a avance normalement
                            
                        if en_passant != []: #regle en passant est applique
                            for i in range(0, len(en_passant), 2):
                                if clic_temp == en_passant[i]:
                                    echiquier[en_passant[i+1][0]][en_passant[i+1][1]] = 0
                    
                    if case[0] == "3" or case[0] == "6":
                        if case[2] == "0": #Si c'est un roi ou une tour qui na pas avance
                            case = f"{case[0]}{case[1]}1" #La case a avance
                        
                        #Partie 1 du roque, on mouvement l'autre case
                        for i in range(0, len(roque), 4):
                            #Pour la tour
                            if case[0] == "3":
                                roi = echiquier[roque[i][0]][roque[i][1]]
                                if roque[i] == clic_temp:
                                    echiquier[roque[i+1][0]][roque[i+1][1]] = roi
                                
                            #Pour le roi
                            if case[0] == "6":
                                tour = echiquier[roque[i+2][0]][roque[i+2][1]]
                                if roque[i+2] == clic_temp:
                                    echiquier[roque[i+3][0]][roque[i+3][1]] = tour
                      
                    if case[0] == "7" or case[0] == "8": #pour un jeu de dames
                        for i in range(0, len(dames_manger), 2):
                            if clic_temp == dames_manger[i]: #si on choisi une case mangeable
                                echiquier[dames_manger[i+1][0]][dames_manger[i+1][1]] = 0
                                #la piece saute est enleve
                                
                                #On compte le nombre de pieces enleves
                                if case[1] == "b":
                                    nb_pieceB += 1 #Nombre des pieces blue mange
                                    if nb_pieceB == 12:
                                        vainqueur = "Bleu"
                                        pyxel.play(0, 0, True)
                                        commencer = 2
  
                                if case[1] == "r":
                                    nb_pieceR += 1 #Nombre des pieces rose mange
                                    if nb_pieceR == 12:
                                        vainqueur = "Rose"
                                        pyxel.play(0, 0, True)
                                        commencer = 2
                                    
                    #Si on mange un roi
                    case_droite = echiquier[clic_temp[0]][clic_temp[1]]
                    if (case_droite != 0) and (case_droite[0] == "6") and (roque == []):
                        if case_droite[1] == "b": #Si le roi bleu est mange
                            vainqueur = "Rose"
                            pyxel.play(0, 0, True)
                        elif case_droite[1] == "r": #Si le roi rose est mange
                            vainqueur = "Bleu"
                            pyxel.play(0, 0, True)
                        commencer = 2 #Game Over
                        
                    echiquier[clic_temp[0]][clic_temp[1]] = case #mouvement (manger une piece)
                    
                    mouvement_precedent = (clic_temp[0],clic_temp[1]) #on garde le mouvement (en passant)
                    
                    echiquier[case_gauche[0]][case_gauche[1]] = 0 #(manger une piece)
                    
                    #Partie 2 du roque, on efface la piece mal place et on la place
                    for i in range(0, len(roque), 4): 
                        #Pour la tour
                        if case[0] == "3" and echiquier[roque[i+1][0]][roque[i+1][1]] == roi:
                            echiquier[roque[i+3][0]][roque[i+3][1]] = f"3{case[1]}1"
                            echiquier[clic_temp[0]][clic_temp[1]] = 0
                        #Pour le roi
                        if case[0] == "6" and echiquier[roque[i+3][0]][roque[i+3][1]] == tour:
                            echiquier[roque[i+1][0]][roque[i+1][1]] = f"6{case[1]}1"
                            echiquier[clic_temp[0]][clic_temp[1]] = 0

                    #On vide le variables de mouvement
                    case_gauche = ""
                    tab_case_droite = []
                    compteur_mouv += 1
                    
        for i in range(8):
            for j in range(8):
                piece = echiquier[i][j]
                #Promotion d'un pion a une reine
                if piece != 0 and piece[0] == "1":
                    if piece[1] == "b" and i == 7:
                        prom_coord = (i,j)
                        prom_couleur = piece[1]
                        commencer = 3
                    elif piece[1] == "r" and i == 0:
                        prom_coord = (i,j)
                        prom_couleur = piece[1]
                        commencer = 3
                        
                #Promotion d'une pierre a une dame
                if piece != 0 and piece[0] == "7":
                    if piece[1] == "b" and i == 7:
                        echiquier[i][j] = "8b"
                    elif piece[1] == "r" and i == 0:
                        echiquier[i][j] = "8r"
        
    elif commencer == 2: #game over, on attends la touche R
        if pyxel.btnp(pyxel.KEY_R):
            echiquier = [[0] * 8 for loop in range (8)]
            jeu = "en attente"
            compteur_mouv = 0
            commencer = 0
            mouvement_precedent = (0, 1)
    
    elif commencer == 3: #promotion, on attends un choix
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            prom_choisi = clic_case()
                
            if prom_choisi == (3, 2): #Si le joueur choisi un cheval
                echiquier[prom_coord[0]][prom_coord[1]] = f"2{prom_couleur}"
                commencer = 1 #Le jeu retourne
                 
            elif prom_choisi == (3, 3): #Si le joueur choisi une tour
                echiquier[prom_coord[0]][prom_coord[1]] = f"3{prom_couleur}1"
                commencer = 1 #Le jeu retourne
                
            elif prom_choisi == (3,4): #Si le joueur choisi une reine
                echiquier[prom_coord[0]][prom_coord[1]] = f"4{prom_couleur}"
                commencer = 1 #Le jeu retourne
                
            elif prom_choisi == (3,5): #Si le joueur choisi un fou
                echiquier[prom_coord[0]][prom_coord[1]] = f"5{prom_couleur}"
                commencer = 1 #Le jeu retourne
        
def draw():     
    if commencer == 0: #menu de selection
        pyxel.rect(0, 0, 64, 128, 6)
        pyxel.rect(64, 0, 64, 128, 8)
        
        pyxel.text(20, 50, "ECHECS", 7)
        pyxel.blt(24, 56, 0, 16, 16, 16, 16, 11)
        
        pyxel.text(86, 50, "DAMES", 7)
        pyxel.blt(88, 56, 0, 96, 0, 16, 16, 11)
        
    elif commencer == 1: #jeu
        echiquier_vide()

        if case_gauche != "":
            pyxel.rect(case_gauche[1] * 16, case_gauche[0] * 16, 16, 16, 5)
        for case_droite in tab_case_droite:
            pyxel.rect(case_droite[1] * 16, case_droite[0] * 16, 16, 16, 8)
    
        dessiner_piece(echiquier)
    
    elif commencer == 2: #ecran de game over
        echiquier_vide()
        pyxel.blt(36, 48, 0, 0, 32, 55, 32, 11) #Game Over
        if vainqueur == "Rose":
            pyxel.blt(20, 32, 0, 0, 64, 98, 16, 11) # Rose gagne
        if vainqueur == "Bleu":
            pyxel.blt(20, 32, 0, 0, 80, 98, 16, 11) # Bleu gagne
        pyxel.text(46, 80, f"En {compteur_mouv//2 + 1} rounds", 0)
        pyxel.text(40, 88, "R pour rejouer", 0)
    
    elif commencer == 3: #Ecran de promotion
        echiquier_vide()
        promotion(prom_coord, prom_couleur)
            
pyxel.run(update, draw)
