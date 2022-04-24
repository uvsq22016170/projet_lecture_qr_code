#Importation des modules
import tkinter as tk
import PIL as pil
from PIL import Image
from PIL import ImageTk 
from tkinter import filedialog
import tkinter.messagebox as mb

#Fonctions
def nbrCol(mat):
    return len(mat[0])

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
    return mat

def charger(filename):
    global photo
    global img
    global canvas
    global dessin
    img = pil.Image.open(filename)
    photo = ImageTk.PhotoImage(img)   
    canvas = tk.Canvas(racine, width = img.size[0] + 2, height = img.size[1] + 2)
    dessin = canvas.create_image(2,2,anchor = tk.NW, image=photo)
    canvas.grid(row=6, column=3, rowspan=9)

def zoom(mat):
    mat_zoom = [[0 for i in range (nbrCol(mat) * 2)] for j in range (nbrLig(mat) * 2)]
    #créer une matrice de largeur et hauteur deux fois plus grande 
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            mat_zoom[2*i][2*j] = mat[i][j]
            mat_zoom[2*i+1][2*j] = mat[i][j]
            mat_zoom[2*i][2*j+1] = mat[i][j]
            mat_zoom[2*i+1][2*j+1] = mat[i][j]
    return mat_zoom

def rotate(mat):
    mat_rota = [[0 for i in range (nbrLig(mat))] for j in range (nbrCol(mat))]
    for i in range(nbrLig(mat_rota)):
        for j in range(nbrCol(mat_rota)):
            mat_rota[i][j] = mat[-j-1][i]
    return mat_rota

def genere_coin():
    l1 = [0] * 7
    l2 = [0] + [1] * 5 + [0]
    l3 = [0,1] + [0] * 3 + [1,0]
    return [l1, l2, l3, l3, l3, l2, l1]

def verif_coin(QR):
    coin_QR = genere_coin()
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
    return QR

def verif_ligne_colonne(QR):
    l1 = [i % 2 for i in range (13)] 
    l2 = [0] * 13
    for i in range(6, 19):
        l2[i-6]=QR[6][i]
    if l2 != l1:
        mb.showerror("Erreur", "Le QR code n'a pas le bon format")
        return False
    for j in range(6, 19):
        l2[j-6]=QR[j][6]
    if l2 != l1:
        mb.showerror("Erreur", "Le QR code n'a pas le bon format")
        return False
    return True

def decode_Hamming74(bits):
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

def code_Hamming74(bits):
    v1 = (bits[0] + bits[1] + bits[3])%2
    v2 = (bits[0] + bits[2] + bits[3])%2
    v3 = (bits[1] + bits[2] + bits[3])%2
    return [bits[0], bits[1], bits[2], bits[3], v1, v2, v3]

def lecture(QR):
    bloc = []
    L_QR = []
    type_donnees = QR[24][8]
    nbr_bloc_bin = ""
    for n in range (13, 18):
        nbr_bloc_bin += str(QR[n][0])
    nbr_bloc = int(nbr_bloc_bin, 2)
    print("Nombre de blocs utilisés : " + str(nbr_bloc))
    for i in range (nbrLig(QR) - 1, 8, -2):
        if i % 4 == 0:
            m = nbrCol(QR) - 1
            n = nbrCol(QR) - 15
            p = -1
        else :
            m = nbrCol(QR) - 14
            n = nbrCol(QR)
            p = 1
        for j in range (m, n, p):
            bloc.extend([QR[i][j], QR[i-1][j]])
            if len(bloc) == 14 :
                L_QR.append(bloc)
                bloc = []
                if nbrLig(L_QR) == nbr_bloc:
                    return L_QR, type_donnees
    return L_QR, type_donnees

def decodage(LQR_et_type):
    L_QR = LQR_et_type[0]
    type_donnees = LQR_et_type[1]
    txt = ""
    if type_donnees == 1:
        for i in range (nbrLig(L_QR)):
            l = decode_Hamming74 (L_QR[i][:7]) + decode_Hamming74 (L_QR[i][7:])
            txt += chr(int("".join(map(str, l)), 2))
        return txt
    else :
        for i in range (nbrLig(L_QR)):
            l = decode_Hamming74 (L_QR[i][:7]) + decode_Hamming74 (L_QR[i][7:])
            txt += hex(int("".join(map(str, l)), 2))[2:4]
        return txt

def genere_filtre(QR):
    if (QR[23][8], QR[22][8]) == (1,0):
        return [[(j+i)%2 for i in range (nbrLig(QR))]for j in range (nbrCol(QR))]
    elif (QR[23][8], QR[22][8]) == (0,1):
        return [[j%2 for i in range (nbrLig(QR))]for j in range (nbrCol(QR))]
    elif (QR[23][8], QR[22][8]) == (1,1):
        return [[i%2 for i in range (nbrLig(QR))]for j in range (nbrCol(QR))]

def enlever_filtre(QR):
    filtre = genere_filtre(QR)
    if filtre == None:
        return QR
    for i in range (9,nbrLig(QR)):
        for j in range (11, nbrCol(QR)):
            QR[i][j] = QR[i][j]^filtre[i][j]
    return QR

def lire ():
    filename = filedialog.askopenfile(mode='rb', title='Choose a file')
    QR = verif_coin(loading(filename))
    if verif_ligne_colonne(QR) :
        l_contenu.config(text = "Contenu du QR code : " + decodage(lecture(enlever_filtre(QR))))

def encodage(msg):
    L_QR = []
    for x in msg:
        if v_type.get() == "1":
            c = format(ord(x), "b")
            for n in range(8 - len(c)):
                c = "0" + c
            L_QR.extend(code_Hamming74(list(map(int, c))[:4]) + code_Hamming74(list(map(int, c))[4:]))
        else:
            try :
                c = format(int(x,16), "b")
            except :
                mb.showerror("Erreur", "Le message saisi n'est pas de l'hexadécimal")
                return False
            for n in range(4 - len(c)):
                c = "0" + c
            L_QR.extend(code_Hamming74(list(map(int, c))))
    return L_QR

def ecriture_donnes (QR, msg):
    QR[24][8] = int(v_type.get())
    nbr_bloc_bin = list(map(int, format(len(msg), "b")))
    for n in range(5 - len(nbr_bloc_bin)):
                nbr_bloc_bin = [0] + nbr_bloc_bin
    for n in range (13, 18):
        QR[n][0] = nbr_bloc_bin[n - 13]
    QR[22][8] = int(v_filtre.get()[1])
    QR[23][8] = int(v_filtre.get()[4])
    return QR

def ecriture_msg(L_QR, QR):
    cpt = 0
    for i in range (24, 8, -2):
        if i % 4 == 0:
            m = 24
            n = 10
            p = -1
        else :
            m = 11
            n = 25
            p = 1
        for j in range (m, n, p):
            QR[i][j] = L_QR[cpt]
            QR[i-1][j] = L_QR[cpt+1]
            cpt += 2
            if cpt >= len(L_QR):
                return QR
    return QR

def ecrire ():
    msg = e_msg.get()
    if len(msg) > 16 or len(msg) == 0:
        mb.showwarning("Attention", "La taille maximum du message doit être comprise entre 1 et 16 caractères")
        return
    if v_type.get() == "0" and len(msg)%2 == 1:
        mb.showwarning("Attention", "Un message en hexadécimal doit avoir une taille paire")
        return
    QR = ecriture_donnes(loading("frame.png"), msg)
    if encodage(msg) == False:
        return
    QR = ecriture_msg(encodage(msg), QR)
    saving(QR, "qr_code_genere" + "_"*bool(len(e_nom.get())) + e_nom.get() + ".png")
    QR_temp = zoom(zoom(QR))
    saving(QR_temp, "temp.png")
    charger("temp.png")

racine=tk.Tk()
racine.title("Lecture et écriture de QR codes")
l_titre_lecture = tk.Label(racine, text="Lecture de QR codes")
b_lire=tk.Button(racine, text="Lire un QR code", command = lire)
l_contenu = tk.Label(racine, text="Contenu du QR code : ")
l_separation1 = tk.Label(racine, text="")
l_titre_ecriture = tk.Label(racine, text="Ecriture de QR codes")
l_separation2 = tk.Label(racine, text="                 ")
l_info_ecriture1 = tk.Label(racine, text="Informations à écrire dans le QR code : ")
l_info_ecriture2 = tk.Label(racine, text="QR code créé : ")
e_msg = tk.Entry(racine)
l_type = tk.Label(racine, text="Format des données :")
v_type = tk.StringVar()
v_type.set(1)
rb_ascii = tk.Radiobutton(racine, variable=v_type, text="Ascii", value=1)
rb_hexa = tk.Radiobutton(racine, variable=v_type, text="Hexadécimal", value=0)
l_filtre = tk.Label(racine, text="Filtre :")
v_filtre = tk.StringVar()
v_filtre.set((0, 0))
rb_aucun = tk.Radiobutton(racine, variable=v_filtre, text="Pas de filtre", value=(0, 0))
rb_damier = tk.Radiobutton(racine, variable=v_filtre, text="Damier", value=(0, 1))
rb_horizontal = tk.Radiobutton(racine, variable=v_filtre, text="Lignes horizontales alternées", value=(1, 0))
rb_vertical = tk.Radiobutton(racine, variable=v_filtre, text="Lignes verticales alternées", value=(1, 1))
l_nom = tk.Label(racine, text="Nom du QR code : ")
e_nom = tk.Entry(racine)
b_ecrire=tk.Button(racine, text="Créer le QR code", command = ecrire)

l_titre_lecture.grid(columnspan=2)
b_lire.grid(row=1, sticky="nsw")
l_contenu.grid(row=2, sticky="nsw")
l_separation1.grid(row=3)
l_titre_ecriture.grid(row=4, columnspan=2)
l_separation2.grid(row=5, column=2)
l_info_ecriture1.grid(row=5, sticky="nsw")
e_msg.grid(row=5, column=1, sticky="nsw")
l_info_ecriture2.grid(row=7, column=3, sticky="nsw")
l_type.grid(row=6, sticky="nsw")
rb_ascii.grid(row=7, sticky="nsw", ipadx = 10)
rb_hexa.grid(row=8, sticky="nsw", ipadx = 10)
l_filtre.grid(row=9, sticky="nsw")
rb_aucun.grid(row=10, sticky="nsw", ipadx = 10)
rb_damier.grid(row=11, sticky="nsw", ipadx = 10)
rb_horizontal.grid(row=12, sticky="nsw", ipadx = 10)
rb_vertical.grid(row=13, sticky="nsw", ipadx = 10)
l_nom.grid(row=14, sticky="nsw")
e_nom.grid(row=14, column=1, sticky="nsw")
b_ecrire.grid(row=15, sticky="nsw")

racine.mainloop()