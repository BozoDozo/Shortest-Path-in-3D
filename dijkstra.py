#construction du graphe sous forme de dico
#pour avoir les voisins

#exemple une map de forme
#  1 2 3
#  4 5 6
#  7 8 9
#donne dico{ '1':('3','4')}
#les 1 3 4 corresponde a des sommet les 10 5 coressponde a leur cout

#on a donc une matrice 3*3 pour les construction

#de plus il nous faut je pense un deuxieme dico
#pour que le 1 dans notre exemple corresponde des valeur i et j pour
# retrouver le cout dans notre matricce
def voisin(matrice):
    n=len(matrice)
    dico={}
    numero_poly=0
    for i in range(n):
        for j in range(n):
                numero_poly=i*n+j
                if i=0 and j=0
                dico[numero_poly]={numero_poly+1,numero_poly+n,numero_poly+n+1}
def djikstra(matrice,somde,somear):
    #matrice de cout,sommde= sommet de depart,sommear au sommet arrivé
    #en sortie on aura une liste du plus court chemin

     val_inf=0
     dico_voisin=voisin(matrice)
     for cle in dico_voisin :
         print(cle)
