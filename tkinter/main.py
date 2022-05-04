from tkinter import *
from map_tk import *
from random import *
from djikstra import *
from astar import *
from bezier import *

"""
map de 20 *20
"""
def liste_de_point(liste):
    global n
    liste_point=[]
    for i in range(len(liste)):
        xd=liste[i]//n
        yd=liste[i]%n
        liste_point.append([xd,yd])

root=Tk()
root.geometry('1000x1000')
#canvas pour avoir map
canva=Canvas(root,width=500,height=500)

canva.pack(side='left')
bouton_b=Button(text="bezier",command=lambda : animation(canva,root)).pack(side="left")
#liste des carre map
liste_square_map_id=[]
liste_cout=[]


""" generation de matrice de cout  """
n=10
borne_valeur_depart=1
borne_valeur_fini=10
liste_cout=generation_matrice_carre_aleatoire(n,borne_valeur_depart,borne_valeur_fini)
print("ma liste cout: \n",liste_cout)

""" creation des poly de map  """
liste_square_map_id=creation_map(liste_square_map_id,canva,liste_cout,n)
print("\n ma liste id de poly \n",liste_square_map_id)


#on fair ca car on peut pas traite des id de su
liste_square_map=generation_matrice_carre(n)
print("\n liste square \n",liste_square_map)

""" point d arrive point de depart"""
arrive=randint(0,(n*n)-1)
depart=randint(0,(n*n)-1)

""" change la couleur du carre arrive depart"""
mettre_couleur_dep_ar(liste_square_map_id,depart,arrive,canva,n)

"""djikstra"""
liste_dji=djikstra(liste_cout,liste_square_map_id,depart,arrive)
print("\n chemin djikstra \n",liste_dji)
tracer_dijkstra(liste_dji,canva)

"""bezier"""
it=100
liste_coors_dji=liste_coor_djikstra(liste_dji)
liste_point=trace_beizier(liste_coors_dji,it,canva)

print("\n point de bezier\n",liste_point)

""" astar"""
#liste=astar(liste_cout,liste_square_map_id,depart,arrive)

#tracer_astar(liste,canva)
print("fini")

root.mainloop()
