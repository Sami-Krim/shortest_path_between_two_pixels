from Vertex import *
import math

class Graph:
    def __init__(self) :
        """
        Initialise une liste pour sauvegarder les sommets du graphe.
        """
        self.vertices = list()

    def get_vertex(self, line_index, column_index):
        """
        Récupère un sommet dans le graphe en fonction de ses coordonnées de ligne et de colonne.

        Arguments:
            line_index: int - Index de ligne du sommet
            column_index: int - Index de colonne du sommet

        Retourne:
            Vertex: Le sommet correspondant aux coordonnées ou None s'il n'existe pas
        """
        for v in self.vertices:
            if(v.line == line_index and v.column == column_index):
                return v
        return None

    def add_vertex(self, line, column, intensity):
        """
        Ajoute un sommet au graphe s'il n'existe pas déjà.

        Arguments:
            line: int - Index de ligne du sommet
            column: int - Index de colonne du sommet
            intensity: dict - Dictionnaire représentant l'intensité du pixel au format RGB

        Retourne:
            bool: True si le sommet a été ajouté avec succès, False sinon
        """
        if (self.get_vertex(line, column) is None):
            self.vertices.append(Vertex(line, column, intensity))
            return True
        return False

    def add_edge(self, vertex1, vertex2):
        """
        Ajoute une arête entre deux sommets du graphe.

        Arguments:
            vertex1: Vertex - Premier sommet
            vertex2: Vertex - Deuxième sommet

        Retourne:
            bool: True si l'arête a été ajoutée avec succès, False sinon
        """
        if (isinstance(vertex1, Vertex) and isinstance(vertex2, Vertex)) :
            if (vertex1 in self.vertices and vertex2 in self.vertices) :
                # Les intensités des arêtes ont été normalisées pour éviter les erreurs d'overflow
                max_intensity = 255
                normalized_intensity_1 = {
                    "B": vertex1.intensity["B"] / max_intensity,
                    "G": vertex1.intensity["G"] / max_intensity,
                    "R": vertex1.intensity["R"] / max_intensity
                }
                normalized_intensity_2 = {
                    "B": vertex2.intensity["B"] / max_intensity,
                    "G": vertex2.intensity["G"] / max_intensity,
                    "R": vertex2.intensity["R"] / max_intensity
                }
                # L'intensité en RGB est sur 3 dimensions, donc on utilise la distance euclidienne pour avoir une seul valeur pour le poids de l'arête
                distance = math.sqrt(
                    (normalized_intensity_1["B"] - normalized_intensity_2["B"]) ** 2 +
                    (normalized_intensity_1["G"] - normalized_intensity_2["G"]) ** 2 +
                    (normalized_intensity_1["R"] - normalized_intensity_2["R"]) ** 2
                )
                vertex1.add_neighbor((vertex2, distance))
                vertex2.add_neighbor((vertex1, distance))
                return  True
        return False

    def dijkstra(self, start, finish):
        """
        Implémente l'algorithme de Dijkstra pour trouver le chemin le plus court entre deux sommets.

        Arguments:
            debut: Vertex - Sommet de départ
            fin: Vertex - Sommet d'arrivée

        Retourne:
            tuple: Le chemin le plus court sous forme de liste de sommets et la distance finale
        """
        # L'algorithme implémenté est basé sur l'algorithme de Dijkstra vu au cours
        distances = {vertex: float('inf') for vertex in self.vertices}
        fathers = {vertex : None for vertex in self.vertices}
        distances[start] = 0
        current_vertex = start
        visited_vertices = set()

        while current_vertex != finish:
            visited_vertices.add(current_vertex)
            for neighbor, weight in current_vertex.neighbors:
                distance = distances[current_vertex] + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    fathers[neighbor] = current_vertex

            unvisited_distances = {vertex: distances[vertex] for vertex in distances if vertex not in visited_vertices}
            
            if not unvisited_distances:
                break

            current_vertex = min(unvisited_distances, key=unvisited_distances.get)

            if distances[current_vertex] == float('inf'):
                break

        path = [finish]
        final_distance = distances[finish] * 255
        while fathers[finish] is not None:
            path.append(fathers[finish])
            finish = fathers[finish]

        path.reverse()
        return path, final_distance