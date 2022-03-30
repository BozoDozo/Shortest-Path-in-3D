def tukey2(matrice):
    n = len(matrice)

    mat_median = [[0 for x in range(n)] for y in range (n)]

    # TRAITEMENT DES CAS PARTICULIERS

    #Coin supérieur gauche
    mat_median[0][0] = median([matrice[0][0], matrice[0][1],
                                matrice[1][0], matrice[1][1]])

    #Coin inférieur droit
    mat_median[n-1][n-1] = median([matrice[n-1][n-1], matrice [n-2][n-2],
                                    matrice[n-1][n-2], matrice[n-2][n-1]])

    #Coin supérieur droit
    mat_median[0][n-1] = median([matrice[0][n-1], matrice[0][n-2],
                                        matrice[1][n-2], matrice[1][n-1]])

    #Coin inférieur gauche
    mat_median[n-1][0] = median([matrice [n-1][0], matrice[n-2][0],
                                        matrice[n-2][1], matrice[n-1][1]])

    #Bordure haute
    for(j in range(1, n-1)):
        mat_median[0][j] = median([matrice[0][j], matrice[0][j-1],matrice[0][j+1],
                                matrice[1][j], matrice[1][j-1],matrice[1][j+1]])

    #Bordure basse
    for(j in range(1, n-1)):
        mat_median[n-1][j] = median([matrice[n-1][j], matrice[n-1][j-1],
                matrice[n-1][j+1], matrice[n-2][j], matrice[n-2][j-1],
                    matrice[n-2][j+1]])

    #Bordure gauche
    for(i in range(1, n-1)):
        mat_median[i][0] = median([matrice[i][0], matrice[i-1][0],
                matrice[i+1][0], matrice[i][1], matrice[i-1][1],
                    matrice[i+1][1]])

    #Bordure droite
    for(i in range(1, n-1)):
            mat_median[i][n-1] = median([matrice[i][n-1], matrice[i-1][n-1],
                    matrice[i+1][n-1], matrice[i][n-2], matrice[i-1][n-2],
                        matrice[i+1][n-2]])

    #Cas général
    for(i in range(2, n-2)):
        for(j in range(2, n-2)):
            mat_median[i][j] = median([matrice[i][j], matrice[i][j-1],
                            matrice[i][j+1], matrice[i-1][j],
                            matrice[i-1][j-1], matrice[i-1][j+1],
                            matrice[i+1][j], matrice[i+1][j-1],
                            matrice[i+1][j+1]])

    return mat_median









        diago


    def voisin_coin_sup_gauche(matrice, rayon=1):
        """
        Renvoie la liste des voisins du coin supérieur gauche avec un rayon
        """

        vec = []

        for i in range(0, rayon+1):
            for j in range(0, rayon+1):
                vec.append(matrice[i][j])

        return vec

    def voisin_coin_sup_droit(matrice, rayon=1):
        """
        Renvoie la liste des voisins du coin supérieur droit avec un rayon
        """
        n = len(matrice)

        vec = []

        for i in range(0, rayon+1):
            for j in range(0, rayon+1):
                vec.append(matrice[i][n-1-j])

        return vec

    def voisin_coin_inf_droit(matrice, rayon = 1):
            """
            Renvoie la liste des voisins du coin inférieur droit avec un rayon
            """
            n = len(matrice)
            vec = []
            for i in range(0, rayon+1):
                for j in range(0, rayon+1):
                    vec.append(matrice[n-1-i][j])

            return vec

    def voisin_coin_inf_gauche(matrice, rayon = 1):
            """
            Renvoie la liste des voisins du coin inférieur droit avec un rayon
            """
            n = len(matrice)
            vec = []
            for i in range(0, rayon+1):
                for j in range(0, rayon+1):
                    vec.append(matrice[i][n-1-j])

            return vec

    def vosin_bordure_haute(matrice, curr, rayon = 1):
        """
        Renvoie la liste des voisins sur la bordure haute excepté les coins
        """
        vec = []
        for l in range(0, rayon+1):
            for j in range(-rayon, rayon+1) :
                vec.append(matrice[l][curr + j])

        return vec

    def voisin_bordure_basse(matrice, curr, rayon = 1):
        """
        Renvoie la liste des voisins d'un élément sur la bordure haute
        """
        vec = []
        for l in range(0, rayon+1):
            for j in range(-rayon, rayon+1) :
                vec.append(matrice[n-1-l][curr + j])

        return vec

    def voisin_bordure_gauche(matrice, curr, rayon=1):
        """
        Renvoie la liste des voisins d'un élément sur la bordure gauche
        """
        vec = []
        for c in range(0, rayon+1):
            for j in range(-rayon, rayon+1) :
                vec.append(matrice[c][curr + j])

        return vec

    def voisin_bordure_droite(matrice, curr, rayon=1):
        """
        Renvoie la liste des voisins d'un élément sur la bordure droite
        """
        vec = []
        for c in range(0, rayon+1):
            for j in range(-rayon, rayon+1) :
                vec.append(matrice[c][curr + j])

        return vec

    def voisin_bordure_droite(matrice, curr, rayon=1):
        """
        Renvoie la liste des voisins d'un élément sur la bordure gauche
        """
        vec = []
        for c in range(0, rayon+1):
            for j in range(-rayon, rayon+1) :
                vec.append(matrice[n-1-c][curr + j])

        return vec
