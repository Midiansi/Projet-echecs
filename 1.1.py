# ECHEC

import pyxel

pyxel.init(128, 128, title="Échec")
pyxel.mouse(True)

pyxel.load("pieces.pyxres", True, True, True, True)
    
echiquier = [[0] * 8 for loop in range (8)]
jeu = "echecs"

#case_selectionne = tab[i][j]         #Case à echanger avec si vide
#case_a_echanger = {tab[i][j], piece} #Tuple qui garde l'information de la case cliquée en premier

def remplir_chiquier_initiallement(tab, jeu):
    """Prends un tableau vide et met les pieces conforme le jeu choisi"""
    
    if jeu == "echecs":
        for i in range(8):
            tab[i][1] = 1
            tab[i][6] = 1
            
#    if jeu == "dames":
            
    return tab
        
    
def echiquier_vide():
    """Dessine un échiquier vide au fond"""
    
    couleur_1 = 7
    couleur_2 = 4
    
    for i in range(8):
        for j in range(8):
            if i % 2 == 0:
                if j % 2 == 0:
                    pyxel.rect(i * 16, j * 16, 16, 16, couleur_1)
                else:
                    pyxel.rect(i * 16, j * 16, 16, 16, couleur_2)
            else:
                if j % 2 == 0:
                    pyxel.rect(i * 16, j * 16, 16, 16, couleur_2)
                else:
                    pyxel.rect(i * 16, j * 16, 16, 16, couleur_1)
                    
def dessiner_piece(tab):
    """Dessine une piece qui est dans tab
    0 est supposé une case vide"""
    
    for i in range(8):
        for j in range(8):
            case = tab[i][j]
            if case != 0: #Case non vide
                
                if case == 1: #Dessine un pion
                    pyxel.blt(i * 16, j * 16, 0, 0, 0, 16, 16, 11)
                    
                    
def update():
    remplir_chiquier_initiallement(echiquier, jeu)

def draw():
    echiquier_vide()
    
    dessiner_piece(echiquier)
    
            
pyxel.run(update, draw)