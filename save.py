import numpy as np


def ecrire_matrice(mat: np.matrix, path: str = "output.txt"):
    """
    Ecrit une matrice dans un fichier texte avec le formatage
    suivant:
    chaque ligne de la matrice est représenté par une ligne
    dans le texte avec chaque élément séparé d'un espace
    """
    f = open(path, 'w')
    # On parcourt la matrice ligne par ligne et colone par colone
    l, c = mat.shape
    for i in range(l):
        for j in range(c):
            f.write(f"{mat[i,j]} ")
        # On saute la ligne pour passer a la nouvelle
        f.write('\n')
    f.close()


def lire_matrice(path: str = "output.txt") -> np.matrix:
    """
    Lit un fichier écrit par la fonction ecrire_matrice et renvoie
    la matrice avec les valeurs associés
    """
    f = open(path, 'r')
    # On parcours toute les lignes du fichiers textes on enlève de la
    # la ligne le dernier élément qui est \n, on transforme la ligne
    # en une liste de chaîne de caractères si un élément est égal alors "inf"
    # On le transforme en un objet flottant inf sinon on transforme le nombre
    # en valeurs entières
    mat = [n[:-1].split() for n in f.readlines()]
    l = len(mat)
    c = len(mat[0])
    for i in range(l):
        for j in range(c):
            if(mat[i][j] == "inf"):
                mat[i][j] = np.inf
            else:
                mat[i][j] = float(mat[i][j])
    f.close()
    print(mat)
    return np.matrix(mat)


if __name__ == "__main__":

    mat = [[1, 2, 33], [4, 58, float('inf')], [7, 8, 9]]
    ecrire_matrice(mat, "test.txt")
