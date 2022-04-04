
def init_dijkstra(n, depart):
    """
    Créé la matrice de coût déroulé
    chaque élément possède un couple
    le coût et le sommet précédent
    """
    liste_cout = [[float('inf'),depart] for x_y in range (n * n)]
    liste_cout[depart] = [-1, 1]
