from tkinter import *
from map_tk import *
from random import *
from djikstra import *
from astar import *
"""
map de 20 *20
"""
root=Tk()
root.geometry('1000x1000')
#canvas pour avoir map
canva=Canvas(root,bg='blue',width=999,height=999)
canva.pack(side='left')
#liste des carre map
liste_square_map_id=[]
liste_cout=[]
#map n*n
n=20
""" generation de matrice """
liste_cout=generation_matrice(n)
print("liste_ cout ",liste_cout)
""" creation de map """
liste_square_map_id=creation_map(liste_square_map_id,canva,liste_cout,n)
#liste de liste

#liste de liste
liste_square_map=generation_matrice_carre(n)

""" point d arrive point de depart"""
arrive=randint(0,400)
depart=randint(0,400)

""" change la couleur du carre arrive depart"""
mettre_couleur_dep_ar(liste_square_map_id,depart,arrive,canva,n)

"""djikstra"""
liste=djikstra(liste_cout,liste_square_map_id,depart,arrive)

tracer_dijkstra(liste,canva)
""" astar"""
#liste=astar(liste_cout,liste_square_map_id,depart,arrive)

#tracer_astar(liste,canva)


root.mainloop()
