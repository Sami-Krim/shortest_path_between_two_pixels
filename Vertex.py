class Vertex:
    def __init__(self, line, column, intensity) :
        """
        Initialise un objet Vertex représentant un pixel dans le graphe.

        Arguments:
            line; int - Le numéro de ligne du pixel.
            column: int - Le numéro de colonne du pixel.
            intensite: dict - Dictionnaire représentant l'intensité du pixel au format BGR.
        """
        self.line = line
        self.column = column
        self.intensity = intensity
        self.neighbors = list()

    def add_neighbor(self, vertex):
        """
        Ajoute un sommet voisin au sommet actuel.

        Arguments:
            vertex: Vertex - Le sommet voisin à ajouter
        """
        self.neighbors.append(vertex)

    def get_vertex(self):
        """
        Renvoie une représentation sous forme de chaîne de caractères du sommet.

        Retourne:
            str: Une chaîne représentant le sommet
        """
        return (f"Vertex({self.line}, {self.column}) : {self.intensity}")
    
    def equal_vertices(self, vertex):
        """
        Vérifie si deux sommets sont identiques en fonction de leurs valeurs de ligne et de colonne.

        Arguments:
            vertex: Vertex - Le sommet à comparer

        Retourne:
            bool: True si les deux sommets ont la même ligne et colonne, False sinon
        """
        return (self.line == vertex.line and self.column == vertex.column)

    def isNeighbor(self, vertex):
        """
        Vérifie si un sommet donné est un voisin du sommet actuel.

        Arguments:
            vertex: Vertex - Le sommet à vérifier pour la relation de voisinage

        Retourne:
            bool: True si le sommet donné est un voisin, False sinon
        """
        for v in self.neighbors:
            if(v[0].equal_vertices(vertex)):
                return True
        return False