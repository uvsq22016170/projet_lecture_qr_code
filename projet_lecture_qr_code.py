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
    coin = [[0]*7 for i in range (7)]
    cpt = 0
    for (m, n) in [(nbrCol(mat) - 7, nbrLig(mat) - 7), (nbrCol(mat) - 7, 0), (0, 0), (0, nbrLig(mat) - 7)]:
        for i in range (7):
            for j in range(7):
                coin[i][j] = mat[i + m][j + n]
        if cpt == 0 and coin == mat_coin:
            mat = rotate(mat)
        elif cpt > 0 and coin != mat_coin:
            for h in range (cpt):
                mat = rotate(mat)
        cpt += 1
    return mat


#szubyfhiaezyufhaziufeza

"""
racine=tk.Tk()

b_save=tk.Button(racine, text="sauvegarder")
b_charge=tk.Button(racine, text="charger")

b_save.pack(side="top", fill="x")
b_charge.pack(side="top", fill="x")

racine.mainloop()
"""