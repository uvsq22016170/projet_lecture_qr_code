#Importation des modules
import PIL as pil
from PIL import Image
from PIL import ImageTk 
import tkinter as tk

#Fonctions
def nbrCol(matrice):
    return(len(matrice[0]))

def nbrLig(matrice):
    return len(matrice)

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
    global mat_coin
    l1 = [0] * 7
    l2 = [0] + [1] * 5 + [0]
    l3 = [0,1] + [0] * 3 + [1,0]
    mat_coin = [l1, l2, l3, l3, l3, l2, l1]

def verif_coin(mat):
    cpt = 1
    coin = [[0]*7 for i in range (7)]
    for (m, n) in [(0, nbrCol(mat) - 7), (0, 0), (nbrLig(mat) - 7, 0)]:
        for i in range (7):
            for j in range(7):
                coin[i][j] = mat[i + m][j + n]
        if coin != mat_coin:
            for k in range (cpt):
                mat = rotate(mat)
            return(mat)
        cpt += 1
    return(mat)

def correction(bits):
    c1 = (bits[3] + bits[4] + bits[6]) % 2
    c2 = (bits[3] + bits[5] + bits[6]) % 2
    c3 = (bits[4] + bits[5] + bits[6]) % 2
    if c1 != bits[0] and c2 != bits[1] and c3 == bits[2]:
        if bits[3] == 0:
            bits_corr = [1] + bits[4:]
        else :
            bits_corr = [0] + bits[4:]
    elif c1 != bits[0] and c2 == bits[1] and c3 != bits[2]:
        if bits[4] == 0:
            bits_corr = bits[3] + [1] + bits[5:]
        else :
            bits_corr = bits[3] + [0] + bits[5:]
    elif c1 == bits[0] and c2 != bits[1] and c3 != bits[2]:
        if bits[5] == 0:
            bits_corr = bits[3:5] + [1] + bits[6]
        else :
            bits_corr = bits[3:5] + [0] + bits[6]
    elif c1 != bits[0] and c2 != bits[1] and c3 != bits[2]:
        if bits[6] == 0:
            bits_corr = bits[3:6] + [1]
        else :
            bits_corr = bits[3:6] + [0]
    return bits_corr

print(correction([1, 1, 1, 1, 1, 0, 1]))


"""
racine=tk.Tk()

b_save=tk.Button(racine, text="sauvegarder")
b_charge=tk.Button(racine, text="charger")

b_save.pack(side="top", fill="x")
b_charge.pack(side="top", fill="x")

racine.mainloop()
"""