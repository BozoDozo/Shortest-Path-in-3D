from ast import Global
from select import select
import tkinter as tk
from tkinter import  filedialog
from turtle import left
from save import lire_matrice
from save import ecrire_matrice
from map import generation_matrice_terrain
from map import min_max_matrix
from typing import Union, List, Tuple

# Variable Gloables
Matrice = [[float('inf'), 3, 5, 5, 8, 6, 7, 3, 3, float('inf')],
           [4, 5, 5, 5, 6, 6, 7, 3, 3, float('inf')],
           [5, 4, 4, 4, 6, 7, 8, 7, 3, float('inf')],
           [6, 5, 5, 4, 3, 6, 9, 8, 7, 7],
           [7, 7, 7, 6, 6, 6, 7, 8, 7, 7],
           [6, 7, 7, 7, 7, 5, 7, 4, 3, float('inf')],
           [8, 7, 8, 7, 7, 6, 6, float('inf'), float('inf'), float('inf')],
           [4, 5, 5, 8, 8, 6, 6, 6, 4, float('inf')],
           [3, 5, 5, 6, 6, 6, 6, 5, 4, float('inf')],
           [float('inf'), 4, 4, 5, 5, 6, 6, 6, 5, 3]]


taille_matrice = 10
borne = 10
flat_niv = 1
obstacle_bool = False
seuil_obstacle = 0
# Si 0 Dijsktra si 1 A*
algo_chemin = 0
#####################
min_value = 0
max_value = 10
#####################
Canva = None
cote = 50
#####################
depart = None
arrivee = None
depart_id = None
arrivee_id = None

texte_aide = """Barre d'outils:
    -Ouvir -> Pour selectionner et charger une matrice
    -Sauver -> Sauvegarder la matrice affichée à l'écran
    -Paramètres -> Permet de modifier les paramètres de génération de matrice et de choisir l'algorithme de recherche de chemin
    -Générer -> Génère une matrice aléatoire avec les paramètres actuels
    -Aide -> Affiche l'aide

La Matrice: Selon l'intensité le carré est plus ou moins noir, si valeur infini donc obstacle alors couleur bleue 'eau'

Selection point de départ et d'arrivée: Le clic gauche LMB permet de sélectionner les deux points dans la matrice signalés à l'écran 
par deux ronds rouge, on ne peut pas sélectionner des valeurs obstacles

Désélection: Le clic droit de la souris permet désélectionner les points de départ et d'arrivée

Ajout d'obstacles: Sans passer par les paramètres on peut rajouter directement des obstacles avec le bouton du milieu de la souris MMB
    
Quitter: Quitte le programme
    
Chemin: Début de l'algorithme de recherche de chemin, Inactif si les deux points ne sont pas sélectionnés
    """
# Fonction Utilitaires
def maj_min_max():
    """
    Mise à jour des valeurs minimales et maximales de la matrice
    """
    global min_value, max_value
    min_value, max_value = min_max_matrix(Matrice)

def normalisation(valeur: Union[int,float] ) -> float:
    """
    Normalise d'une valeur en fonction du minimum et du maximum
    """
    return (valeur-min_value)/(max_value-min_value)


def hex_to_rgb(value: str):
    """Return (red, green, blue) for the color given as #rrggbb."""
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(red: int, green: int, blue: int):
    """Return color as #rrggbb for the given color values."""
    return '#%02x%02x%02x' % (red, green, blue)

def shade_color(color: Tuple[int, int, int], factor:int):
        """
        Retourne la couleur rgb assombri ou éclaircir
        """
        shaded_color= []
        for c in color:
            x = int(c * factor)
            if(x > 255):
                x = 255
            if(x < 0):
                x = 0
            shaded_color.append(x)
        return shaded_color

def get_color(val: Union[int, float]) -> str:
    """
    Récupère la couleur en niveau de gris
    pour une intensité donnée
    """
    if(val == float('inf')):
        color = (50,50,255)
    else:
        norm = normalisation(val)
        color = shade_color((255, 255, 255), 1-norm)
    return rgb_to_hex(*color)

def circle_to_oval(x: int, y: int, r: int):
    return (x-r, y-r, x+r, y+r)
# Fonction pour les boutons
def ouvrir_fichier():
    """
    Renvoie le chemin du fichier sélectionné
    """
    return filedialog.askopenfilename()

def sauver_matrice():
    """
    Sauvegarde la matrice courante
    """
    ecrire_matrice(Matrice, filedialog.asksaveasfilename())

def ouvrir_matrice():
    """
    Ouvre une matrice
    """
    global Matrice
    if((path := ouvrir_fichier()) != ""):
        Matrice = lire_matrice(path)
        actu_matrice()

def modif_parametre():
    """
    Modifie les paramètres de generation de matrice
    et en génère une nouvelle
    """
    # Initialisation des valeurs des tirettes aux paramètres globaux et du choix de l'algo
    # de recherche du plus court chemin
    win_2 = tk.Toplevel(win)
    n =  tk.IntVar(win_2, taille_matrice)
    born = tk.IntVar(win_2, borne)
    flat = tk.IntVar(win_2, flat_niv)
    obs = tk.IntVar(win_2, obstacle_bool)
    cran = tk.IntVar(win_2, seuil_obstacle)
    algo = tk.IntVar(win_2, algo_chemin)
    win_2.title("Generation de Matrice")
    #Parametre pour la generation de la matrice
    tk.Scale(win_2, label="Taille de la matrice", from_=5, to_=50, variable=n , length="10c", orient="horizontal").pack(side="top")
    tk.Scale(win_2, label="Borne supérieur des valeurs", from_=2, to_=100, variable=born,length="10c", orient="horizontal").pack(side="top")
    tk.Scale(win_2, label="Taux d’aplatissement des valeurs", from_=0, to_=10, variable=flat, length="10c", orient="horizontal").pack(side="top")
    tk.Checkbutton(win_2, text= "Présence d'obstacles", variable=obs).pack(side="top")
    tk.Scale(win_2, label="Seuil des d’obstacles", from_=0, to_=5, variable=cran, length="10c", orient="horizontal").pack(side="top")
    # Choix Algo chemin
    radio_frame = tk.Frame(win_2)
    radio_frame.pack(side="top")
    tk.Radiobutton(radio_frame, text="Dijkstra", indicatoron=0, variable=algo, value= 0).pack(side="left")
    tk.Radiobutton(radio_frame, text="A*", indicatoron=0, variable=algo, value= 1).pack(side="left")
    
    
    # Génération de la matrice avec les nouveaux paramètres entrés
    tk.Button(win_2,text="Valider",command=lambda:nouvelle_matrice_modifie(n.get(), born.get(), flat.get(), bool(obs.get()), cran.get(), algo.get(), win_2)).pack(side="bottom")

def nouvelle_matrice_modifie( taille : int, borne_sup: int, flatness: int, a_obstacle: bool, cran_obstacle: int, alg: int, win: tk.Toplevel = None,):
    """
    Mise à jour des paramètres globaux et génération d'une nouvelle matrice
    """
    global Matrice, taille_matrice, borne, flat_niv, obstacle_bool, seuil_obstacle, algo_chemin
    # Generation de la nouvelle matrice
    algo_chemin = alg
    #Si aucun paramètre de creation de matrice n'a été changé alors on ne génère pas de nouvelle matrice
    if(taille_matrice, borne, flat_niv, obstacle_bool, seuil_obstacle) != (taille, borne_sup, flatness, a_obstacle, cran_obstacle):
        Matrice = generation_matrice_terrain(taille, 1, borne_sup, flatness, a_obstacle, cran_obstacle )
        #print(Matrice)
        # Mise à jour des paramètres globaux
        taille_matrice, borne, flat_niv, obstacle_bool, seuil_obstacle = taille, borne_sup, flatness, a_obstacle, cran_obstacle
        #print(taille,  borne_sup, flatness,a_obstacle, cran_obstacle)
        # Destruction de la boîte de modification de matrice
        actu_matrice()
    if(win):
        win.destroy()

def nouvelle_matrice():
    """
    Génération d'une nouvelle matrice
    """
    global Matrice
    Matrice = generation_matrice_terrain(taille_matrice, 1, borne, flat_niv, obstacle_bool, seuil_obstacle )
    actu_matrice()


def actu_matrice():
    """
    Actualise la matrice afficher à l'écran
    """
    global depart, arrivee, depart_id, arrivee_id, cote
    depart, arrivee,depart_id, arrivee_id = None, None, None, None
    maj_min_max()
    # Taille des carrés en fonction de la taille de la matrice
    cote = 500/len(Matrice[0])
    #print(len(Matrice))
    #print(cote)
    Canva.delete(tk.ALL)
    ht = cote*len(Matrice[0])
    wt = cote*len(Matrice[0])
    Canva.config(width=wt, height=ht)
    for i in range(len(Matrice[0])):
        for j in range(len(Matrice)):
            couleur = get_color(Matrice[i][j])
    # Les obstacles et valeurs finis ne sont pas traités de la même manière
            if(Matrice[i][j] == float("inf")):
                Canva.create_rectangle(i*cote, j*cote,i*cote+cote, j*cote+cote, fill= couleur, tags=("inf", str((i,j))))
            else:
                Canva.create_rectangle(i*cote, j*cote,i*cote+cote, j*cote+cote, fill= couleur, tags=("point", str((i,j))))

# Fonction Selection de points

def print_tags(event = None):
    """
    Imprime les tags du widget courant
    """
    id = Canva.find_withtag("current")
    tags = Canva.gettags(id)
    print(tags)

def selec_depart(event = None):
    """
    Sélectionne le point de départ
    """
    global depart_id, depart
    id = Canva.find_withtag("current")
    tags = Canva.gettags(id)
    coords = tags[1].split(',')
    # Car coords ressemble à "(x, y)"
    i = int(coords[0][1:])
    j = int(coords[1][1:-1])
    depart = (i,j)
    # Calcul de points pour créer un cercle au centre du carré
    xy_xy = circle_to_oval(i*cote+cote/2, j*cote+cote/2, 0.25*cote)
    depart_id = Canva.create_oval(*xy_xy, fill="red",tags=("depart", str((i,j))))
    Canva.tag_unbind("point","<1>")
    Canva.tag_bind("point","<1>",selec_arrivee)

def selec_arrivee(event = None):
    """
    Sélectionne le point d'arrivée
    """
    global arrivee_id, arrivee
    id = Canva.find_withtag("current")
    tags = Canva.gettags(id)
    coords = tags[1].split(',')
    # Car coords ressemble à "(x, y)"
    i = int(coords[0][1:])
    j = int(coords[1][1:-1])
    arrivee = (i,j)
    # Calcul de points pour créer un cercle au centre du carré
    xy_xy = circle_to_oval(i*cote+cote/2, j*cote+cote/2, 0.25*cote)
    arrivee_id = Canva.create_oval(*xy_xy, fill="red",tags=("arrivee", str((i,j))))
    Canva.tag_unbind("point", "<1>")
    Canva.tag_unbind("point", "<2>")
    bouton_chemin.config(state="normal")

def deselec(event = None):
    """
    Désélectionne le point de départ et le point d'arrivée
    """
    global depart, arrivee, depart_id, arrivee_id
    depart = None
    arrivee = None
    if(depart_id):
        Canva.delete(depart_id)
    if(arrivee_id):
        Canva.delete(arrivee_id)
    depart_id = None
    arrivee_id = None
    Canva.tag_bind("point","<1>", selec_depart)
    Canva.tag_bind("point", "<2>", ajout_obstacle)
    bouton_chemin.config(state="disabled")

def ajout_obstacle(event = None):
    """
    Ajout d'obstacle directement sur le terrain
    """
    id = Canva.find_withtag("current")
    tags = Canva.gettags(id)
    print(tags)
    coords = tags[1].split(',')
    # Car coords ressemble à "(x, y)""
    i = int(coords[0][1:])
    j = int(coords[1][1:-1])
    Canva.delete(id)
    Canva.create_rectangle(i*cote, j*cote,i*cote+cote, j*cote+cote, fill= rgb_to_hex(*(50,50,255)), tags=("inf", str((i,j))))

def afficher_aide(event = None):
    """
    Affiche l'aide
    """
    aide_win = tk.Toplevel(win)
    aide_win.title("Aide")
    text_frame = tk.Frame(aide_win)
    frame_button = tk.Frame(aide_win)
    texte = tk.Text(text_frame)
    texte.insert(tk.END, texte_aide)
    texte.pack(side="top", expand=True, fill="both")
    text_frame.pack(fill="both",expand=True)
    frame_button.pack(side="bottom",fill =tk.Y)
    tk.Button(frame_button,text="Ok",command=aide_win.destroy)

# Initialisation des fenêtres
win = tk.Tk()
win.title("Plan du terrain")
top_frame = tk.Frame(win)

# Chargement d'une matrice à partir d'un fichier texte
bouton_charger = tk.Button(
    top_frame, text="Ouvrir", width=20, command=ouvrir_matrice)
# Sauvegarde de la matrice courante
bouton_sauver = tk.Button(
    top_frame, text="Sauver", width=20, command=sauver_matrice)
# Modification des paramètres de la matrice
bouton_modif = tk.Button(
top_frame, text="Paramètres", width=20, command=modif_parametre)
# Génération d'une nouvelle matrice avec les paramètres actuels
bouton_gen = tk.Button(
    top_frame, text="Générer", width=20, command=nouvelle_matrice)

#Aide
aide = tk.Button(top_frame, text="Aide", width=20, command=afficher_aide)
Canva = tk.Canvas(win)

bottom_frame = tk.Frame(win)
# Lancement de la recherche de chemin
bouton_chemin = tk.Button(bottom_frame, text= "Chemin", state="disabled", width=20, height= 5)
bouton_quitter = tk.Button(bottom_frame, text= "Quitter", width=20, height= 5, command=lambda:exit(0))

# Disposition des Widgets
bouton_charger.pack(side="left", expand=True)
bouton_sauver.pack(side="left", expand=True)
bouton_modif.pack(side="left", expand=True)
bouton_gen.pack(side="left", expand=True)
aide.pack(side="right",expand=True)
top_frame.pack(side="top", fill=tk.X)
Canva.pack(side="top")

bouton_chemin.pack(side="right")
bouton_quitter.pack(side="left")
bottom_frame.pack(side="bottom", fill=tk.X)


# Bindings
Canva.tag_bind("point", "<1>", selec_depart)
Canva.bind_all("<3>", deselec)
Canva.tag_bind("point","<2>", ajout_obstacle)
actu_matrice()

tk.mainloop()

exit(0)
