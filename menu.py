import tkinter as tk
import numpy as np
from tkinter import  filedialog
from save import lire_matrice
from save import ecrire_matrice
from map import generation_matrice_terrain
from dijkstra import dijkstra, a_star
from bezier import trace_beizier, get_info
from utils import rgb_to_hex, circle_to_oval, get_info_matrice, green_to_brown_gradient_maping
from map import min_max_matrix
from chenille_2D import Chenille_2D
# Variable Gloables
matrice   = np.matrix([[np.inf, 3., 5., 5., 8., 6., 7., 3., 3., np.inf],
           [4., 5., 5., 5., 6., 6., 7., 3., 3., np.inf],
           [5., 4., 4., 4., 6., 7., 8., 7., 3., np.inf],
           [6., 5., 5., 4., 3., 6., 9., 8., 7., 7.],
           [7., 7., 7., 6., 6., 6., 7., 8., 7., 7.],
           [6., 7., 7., 7., 7., 5., 7., 4., 3., np.inf],
           [8., 7., 8., 7., 7., 6., 6., np.inf, np.inf, np.inf],
           [4., 5., 5., 8., 8., 6., 6., 6., 4., np.inf],
           [3., 5., 5., 6., 6., 6., 6., 5., 4., np.inf],
           [np.inf, 4., 4., 5., 5., 6., 6., 6., 5., 3.]])


taille_matrice = 10
borne = 10
flat_niv = 1
obstacle_bool = False
seuil_obstacle = 0
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
trajet = []
trajet_dijkstra = []
id_dijkstra = []
trajet_a_star = []
id_a_star = []
#####################
mobile_2D = None
#####################
texte_aide = """Barre d'outils:
    -Ouvir -> Pour selectionner et charger une matrice
    -Sauver -> Sauvegarder la matrice affichée à l'écran
    -Paramètres -> Permet de modifier les paramètres de génération de matrice et de choisir l'algorithme de recherche de chemin
    -Générer -> Génère une matrice aléatoire avec les paramètres actuels
    -Aide -> Affiche l'aide

La matrice: Selon l'intensité le carré est plus ou moins noir, si valeur infini donc obstacle alors couleur bleue 'eau'

Selection point de départ et d'arrivée: Le clic gauche LMB permet de sélectionner les deux points dans la matrice signalés à l'écran 
par deux ronds rouge, on ne peut pas sélectionner des valeurs obstacles

Désélection: Le clic droit de la souris permet désélectionner les points de départ et d'arrivée

Ajout d'obstacles: Sans passer par les paramètres on peut rajouter directement des obstacles avec le bouton du milieu de la souris MMB
(seulement si aucun point n'est sélectionné)    
Quitter: Quitte le programme
    
Chemin: Début de l'algorithme de recherche de chemin, Inactif si les deux points ne sont pas sélectionnés
    """





def maj_min_max():
    """
    Mise à jour des valeurs minimales et maximales de la matrice
    """
    global min_value, max_value
    min_value, max_value = min_max_matrix(matrice)
    get_info_matrice(min_value, max_value, matrice)


# Fonction pour les boutons
def ouvrir_matrice():
    """
    Ouvre une matrice à partir d'un fichier d'une matrice
    """
    global matrice
    if (path:= filedialog.askopenfilename()):
        matrice = lire_matrice(path)
        actu_matrice()

def sauver_matrice():
    """
    Sauvegarde la matrice courante
    """
    
    if((path:= filedialog.asksaveasfilename())):
        ecrire_matrice(matrice, path)

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
    win_2.title("Generation de matrice")
    #Parametre pour la generation de la matrice
    tk.Scale(win_2, label="Taille de la matrice", from_=5, to_=50, variable=n , length="10c", orient="horizontal").pack(side="top")
    tk.Scale(win_2, label="Borne supérieur des valeurs", from_=2, to_=1000, variable=born,length="10c", orient="horizontal").pack(side="top")
    tk.Scale(win_2, label="Taux d’aplatissement des valeurs", from_=0, to_=10, variable=flat, length="10c", orient="horizontal").pack(side="top")
    tk.Checkbutton(win_2, text= "Présence d'obstacles", variable=obs).pack(side="top")
    tk.Scale(win_2, label="Seuil des d’obstacles", from_=0, to_=50, variable=cran, length="10c", orient="horizontal").pack(side="top")
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
    global matrice, taille_matrice, borne, flat_niv, obstacle_bool, seuil_obstacle, algo_chemin
    # Generation de la nouvelle matrice
    algo_chemin = alg
    #Si aucun paramètre de creation de matrice n'a été changé alors on ne génère pas de nouvelle matrice
    if(taille_matrice, borne, flat_niv, obstacle_bool, seuil_obstacle) != (taille, borne_sup, flatness, a_obstacle, cran_obstacle):
        matrice = generation_matrice_terrain(taille, 1, borne_sup, flatness, a_obstacle, cran_obstacle )
        #print(matrice)
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
    global matrice
    matrice = generation_matrice_terrain(taille_matrice, 1, borne, flat_niv, obstacle_bool, seuil_obstacle )
    actu_matrice()


def actu_matrice():
    """
    Actualise la matrice afficher à l'écran
    """
    print(matrice)
    global depart, arrivee, depart_id, arrivee_id, cote
    depart, arrivee,depart_id, arrivee_id = None, None, None, None
    maj_min_max()
    # Taille des carrés en fonction de la taille de la matrice
    l, c = matrice.shape
    cote = 500/l
    Canva.delete(tk.ALL)
    ht = cote*l
    wt = cote*l
    Canva.config(width=wt, height=ht)
    maj_min_max()
    for i in range(l):
        for j in range(c):
            #couleur = get_color(matrice[i,j])
            if(flag:= (val := matrice[i,j]) == np.inf):
                couleur = "#0033CC"
            else :
                couleur = green_to_brown_gradient_maping(val)
    # Les obstacles et valeurs finis ne sont pas traités de la même manière
            if(flag):
                Canva.create_rectangle(i*cote, j*cote,i*cote+cote, j*cote+cote, fill= couleur, tags=("inf", str((i,j))))
            else:
                Canva.create_rectangle(i*cote, j*cote,i*cote+cote, j*cote+cote, fill= couleur, tags=("point", str((i,j))))
    bouton_chemin.config(state="disabled")
    bouton_animation.config(state="disabled")

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
    Canva.tag_unbind("point", "<2>")

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
    if(depart != (i,j)):
        arrivee = (i,j)
        # Calcul de points pour créer un cercle au centre du carré
        xy_xy = circle_to_oval(i*cote+cote/2, j*cote+cote/2, 0.25*cote)
        arrivee_id = Canva.create_oval(*xy_xy, fill="red",tags=("arrivee", str((i,j))))
        Canva.tag_unbind("point", "<1>")
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
    Canva.delete("dij")
    Canva.delete("a_")
    
    depart_id = None
    arrivee_id = None
    Canva.tag_bind("point","<1>", selec_depart)
    Canva.tag_bind("point", "<2>", ajout_obstacle)
    bouton_chemin.config(state="disabled")
    bouton_animation.config(state="disabled")

def ajout_obstacle(event = None):
    """
    Ajout d'obstacle directement sur le terrain
    """
    global matrice
    id = Canva.find_withtag("current")
    tags = Canva.gettags(id)
    coords = tags[1].split(',')
    # Car coords ressemble à "(x, y)""
    i = int(coords[0][1:])
    j = int(coords[1][1:-1])
    Canva.delete(id)
    Canva.create_rectangle(i*cote, j*cote,i*cote+cote, j*cote+cote, fill= rgb_to_hex(*(50,50,255)), tags=("inf", str((i,j))))
    matrice[i,j] = np.inf

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

def chemin(event = None):
    """
    Affiche les point de controle pour bezier calculés
    par l'algorithme du plus court chemin
    """
    global trajet_dijkstra, id_dijkstra, id_a_star, trajet_a_star
    algo_chemin = algo.get() 
    trajet_dijkstra = dijkstra(matrice, depart, arrivee)
    trajet_a_star = a_star(matrice, depart, arrivee)
    # Traçage des chemins en caché
    for point in range(1,len(trajet_dijkstra)-1):
        i, j = trajet_dijkstra[point]
        xy_xy = circle_to_oval(i*cote+cote/2, j*cote+cote/2, 0.125*cote)
        id_dijkstra.append(Canva.create_oval(*xy_xy, fill="blue", state="hidden", tags=("dij", str((i,j)))))
    for point in range(1,len(trajet_a_star)-1):
        i, j = trajet_a_star[point]
        xy_xy = circle_to_oval(i*cote+cote/2, j*cote+cote/2, 0.125*cote)
        id_a_star.append(Canva.create_oval(*xy_xy, fill="purple", state="hidden", tags=("a_", str((i,j)))))
    # On affiche le chemin sélectionné
    if(algo_chemin):
        print("A*")
        Canva.itemconfig("a_", state='normal')
    else:
        print("Dijkstra")
        Canva.itemconfig("dij", state='normal')
    
    bouton_chemin.config(state="disabled")
    bouton_animation.config(state="normal")


def cacher_chemin(event = None):
    """
    Cache le chemin qui n'est pas sélectionné
    """
    if(algo.get()):
        Canva.itemconfig("a_", state='normal')
        Canva.itemconfig("dij", state='hidden')
        print("A*")
    
    else:
        Canva.itemconfig("dij", state='normal')
        Canva.itemconfig("a_", state='hidden')
        print("Dijkstra")
    
def animation_2D(event = None):
    """
    Lance le mobile 2D sur le canvas dans tkinter
    """
    global trajet, mobile_2D
    bouton_animation.config(state='disabled')
    bouton_stop.config(state='normal')
    if(algo.get()):
        trajet = trajet_a_star
    
    else:
        trajet = trajet_dijkstra
    get_info(Canva, cote)
    print(trajet)
    mobile_2D = Chenille_2D(*trajet[0], 10, Canva, cote)
    # Permet la destruction du mobile 2D
    try:
        trace_beizier(trajet, 100, mobile_2D)
    except IndexError:
        print("Mobile 2D détruit")
    bouton_animation.config(state='normal')
    bouton_stop.config(state='disabled')
    
def stop(event= None):
    """
    Détruit le mobile 2D pour mettre fin à l'animation
    """
    global mobile_2D
    mobile_2D.delete()
    bouton_stop.config(state='disabled')
    bouton_animation.config(state='normal')

# Initialisation des fenêtres
win = tk.Tk()
win.title("Plan du terrain")
top_frame = tk.Frame(win)

# Si 0 Dijsktra si 1 A*
algo = tk.IntVar(win, 0)
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
bouton_chemin = tk.Button(bottom_frame, text= "Chemin", state="disabled", width=20, height= 5, command=chemin)
# Quitter
bouton_quitter = tk.Button(bottom_frame, text= "Quitter", width=20, height= 5, command=lambda:exit(0))
# Lancement du mobile 2D
bouton_animation = tk.Button(bottom_frame, text= "Animation", state="disabled", width=20, height= 5, command=animation_2D)
# Bouton Stop
bouton_stop = tk.Button(bottom_frame, text= "Stop", state="disabled", width=20, height= 5, command=stop)
# Radio button
radio_frame = tk.Frame(bottom_frame, width=20)
tk.Radiobutton(radio_frame, padx=10, pady=30, text="Dijkstra", indicatoron=0, command =cacher_chemin, variable=algo, value= 0).pack(side="left")
tk.Radiobutton(radio_frame, padx=10, pady=30,text="A*",indicatoron=0, variable=algo, command =cacher_chemin, value= 1).pack(side="left")
# Disposition des Widgets
bouton_charger.pack(side="left", expand=True)
bouton_sauver.pack(side="left", expand=True)
bouton_modif.pack(side="left", expand=True)
bouton_gen.pack(side="left", expand=True)
aide.pack(side="right",expand=True)
top_frame.pack(side="top", fill=tk.X)
Canva.pack(side="top")

bouton_chemin.pack(side="right")
bouton_animation.pack(side="right")
bouton_stop.pack(side="right")
radio_frame.pack(side ="right")
bouton_quitter.pack(side="left")
bottom_frame.pack(side="bottom", fill=tk.X)


# Bindings
Canva.tag_bind("point", "<1>", selec_depart)
Canva.bind_all("<3>", deselec)
Canva.tag_bind("point","<2>", ajout_obstacle)
actu_matrice()

tk.mainloop()

exit(0)
