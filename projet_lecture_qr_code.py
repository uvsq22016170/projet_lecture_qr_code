#Importation des modules
import tkinter as tk
import PIL as pil
from PIL import Image
from PIL import ImageTk 
from tkinter import filedialog

#Fonctions
def nbrCol(mat):
    return(len(mat[0]))

def nbrLig(mat):
    return len(mat)

def saving(mat, filename):#sauvegarde l'image contenue dans matpix dans le fichier filename
							 #utiliser une extension png pour que la fonction fonctionne sans perte d'information
    toSave=pil.Image.new(mode = "1", size = (nbrCol(mat),nbrLig(mat)))
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            toSave.putpixel((i,j),mat[j][i])
    toSave.save(filename)

def loading(filename):#charge le fichier image filename et renvoie une matrice de 0 et de 1 qui représente 
					  #l'image en noir et blanc
    toLoad=pil.Image.open(filename)
    mat=[[0]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j]= 0 if toLoad.getpixel((j,i)) == 0 else 1
    return(mat)

def rotate(mat):
    mat_rota = [[0 for i in range (nbrLig(mat))] for j in range (nbrCol(mat))]
    for i in range(nbrLig(mat_rota)):
        for j in range(nbrCol(mat_rota)):
            mat_rota[i][j] = mat[-j-1][i]
    return mat_rota

def genere_coin():
    global coin_QR
    l1 = [0] * 7
    l2 = [0] + [1] * 5 + [0]
    l3 = [0,1] + [0] * 3 + [1,0]
    coin_QR = [l1, l2, l3, l3, l3, l2, l1]

def verif_coin(QR):
    genere_coin()
    cpt = 1
    coin = [[0]*7 for i in range (7)]
    for (m, n) in [(0, nbrCol(QR) - 7), (0, 0), (nbrLig(QR) - 7, 0)]:
        for i in range (7):
            for j in range(7):
                coin[i][j] = QR[i + m][j + n]
        if coin != coin_QR:
            for k in range (cpt):
                QR = rotate(QR)
            return(QR)
        cpt += 1
    return(QR)

def verif_ligne_colonne(QR):
    l1 = [i % 2 for i in range (13)] 
    l2 = [0] * 13
    for i in range(6, 19):
        l2[i-6]=QR[6][i]
    if l2 != l1:
        print("Erreur: Le QR code n'a pas le bon format")
        pass
    for j in range(6, 19):
        l2[j-6]=QR[j][6]
    if l2 != l1:
        print("Erreur: Le QR code n'a pas le bon format")
        pass

def decode_Hamming74 (bits):
    c1 = bits[4] != (bits[0] + bits[1] + bits[3])%2
    c2 = bits[5] != (bits[0] + bits[2] + bits[3])%2
    c3 = bits[6] != (bits[1] + bits[2] + bits[3])%2
    if c1 and c2 and c3:
        bits[3] = (bits[3] + 1) % 2
    elif c1 and c2:
        bits[0] = (bits[0] + 1) % 2
    elif c1 and c3:
        bits[1] = (bits[1] + 1) % 2
    elif c2 and c3:
        bits[2] = (bits[2] + 1) % 2
    return [bits[0], bits[1], bits[2], bits[3]]

def code_Hamming74 (bits):
    v1 = (bits[0] + bits[1] + bits[3])%2
    v2 = (bits[0] + bits[2] + bits[3])%2
    v3 = (bits[1] + bits[2] + bits[3])%2
    return [bits[0], bits[1], bits[2], bits[3], v1, v2, v3]

def lecture (QR):
    bloc = []
    L_QR = []
    cpt = 0
    type_donnees = QR[24][8]
    for i in range (nbrLig(QR) - 1, 8, -2):
        if cpt % 2 == 0:
            m = nbrCol(QR) - 1
            n = nbrCol(QR) - 15
            p = -1
        else :
            m = nbrCol(QR) - 14
            n = nbrCol(QR)
            p = 1
        for j in range (m, n, p):
            if len(bloc) == 14 :
                if bloc == [1]*14:
                    return(L_QR, type_donnees)
                L_QR.append(bloc)
                bloc = []
            bloc.extend([QR[i][j], QR[i-1][j]])
        if bloc == [1]*14:
            return(L_QR, type_donnees)
        L_QR.append(bloc)
        bloc = []
        cpt += 1
    return L_QR, type_donnees

def decodage (LQR_et_type):
    L_QR = LQR_et_type[0]
    type_donnees = LQR_et_type[1]
    txt = ""
    if type_donnees == 1:
        for i in range (nbrLig(L_QR)):
            l = decode_Hamming74 (L_QR[i][:7]) + decode_Hamming74 (L_QR[i][7:])
            l.reverse()
            txt += chr(int("".join(map(str, l)), 2))
        return txt
    else :
        for i in range (nbrLig(L_QR)):
            l = decode_Hamming74 (L_QR[i][:7]) + decode_Hamming74 (L_QR[i][7:])
            l.reverse()
            txt += hex(int("".join(map(str, l)), 2))[2:4]
        return txt

def enlever_filtre(QR):
    if (QR[23][8], QR[22][8]) == (0,0):
        return QR
    elif (QR[23][8], QR[22][8]) == (1,0):
        filtre = [[(j+i)%2 for i in range (nbrLig(QR))]for j in range (nbrCol(QR))]
    elif (QR[23][8], QR[22][8]) == (0,1):
        filtre = [[j%2 for i in range (nbrLig(QR))]for j in range (nbrCol(QR))]
    elif (QR[23][8], QR[22][8]) == (1,1):
        filtre = [[i%2 for i in range (nbrLig(QR))]for j in range (nbrCol(QR))]
    for i in range (9,nbrLig(QR)):
        for j in range (11, nbrCol(QR)):
            QR[i][j] = QR[i][j]^filtre[i][j]
    return QR

def lire():
    filename = filedialog.askopenfile(mode='rb', title='Choose a file')
    label_lu.config(text = decodage(lecture(enlever_filtre(verif_coin(loading(filename))))))

racine=tk.Tk()

b_lire=tk.Button(racine, text="Lire un QR code", command = lire)
label_lu = tk.Label(racine)

b_lire.pack(side="top", fill="x")
label_lu.pack(side = "bottom", fill = "x")

racine.mainloop()