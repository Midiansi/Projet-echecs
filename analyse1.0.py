tab = [[0] * 8 for loop in range (8)]

for i in range(8):
    tab[1][i] = "1b" #ligne de pions bleu
    tab[6][i] = "1r" #ligne de pions roses
            
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

def materiel(tab: list, couleur: str):
    """
    fait la somme des valeurs des pieces de l'echiquier pour une couleur
    """
    if couleur == "b":   
        pb= 0
        for i in range(8):
            for j in range(8):
                if tab[i][j] == "1b":
                    pb += 1
                    
        cb= 0
        for i in range(8):
            for j in range(8):
                if tab[i][j] == "2b":
                    pb += 1
        cb *= 3
        
        fb= 0
        for i in range(8):
            for j in range(8):
                if tab[i][j] == "3b":
                    fb += 1
        fb *= 3
        
        tb= 0
        for i in range(8):
            for j in range(8):
                if tab[i][j] == "4b":
                    tb += 1
        tb *= 5
        
        db= 0
        for i in range(8):
            for j in range(8):
                if tab[i][j] == "5b":
                    db += 1
        db *= 9
                    
        mb = pb + cb + fb + tb + db
        
        return mb
    
    if couleur == "n":   
        pn= 0
        for i in range(8):
            for j in range(8):
                if tab[i][j] == "1r":
                    pn += 1
        cn= 0
        for i in range(8):
            for j in range(8):
                if tab[i][j] == "2r":
                    cn += 1
        cn *= 3
        
        fn = 0
        for i in range(8):
            for j in range(8):
                if tab[i][j] == "3r":
                    fn += 1
        fn *= 3
        
        tn= 0
        for i in range(8):
            for j in range(8):
                if tab[i][j] == "4r":
                    tn += 1
        tn *= 5
        
        dn= 0
        for i in range(8):
            for j in range(8):
                if tab[i][j] == "5r":
                    dn += 1
        dn *= 9
        
        mn = pn + cn + fn + tn + dn
        
        return mn

assert materiel(tab, "b") == 39
print(materiel(tab, "n"))

def evaluer(echiquier:list, couleur: str) -> int:
    """
    evalue quantitativment l'echiquier
    """
    
    
    
    
        
