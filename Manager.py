import cv2 as cv
from Graph import Graph

def load_graph(image_path):
    # Lire l'image en utilisant OpenCV et la redimensionner à une taille fixe (21x21 pixels)
    img = cv.imread(image_path)
    height, width = (21, 21)
    image = cv.resize(img, (height, width))

    # Créer une instance de la classe Graph pour représenter l'image sous forme de graphe
    image_graph = Graph()

    # Parcourir chaque pixel de l'image redimensionnée
    for i in range(width):
        for j in range(height):
            # Extraire les intensités de couleur RGB pour chaque pixel
            colors = ["B", "G", "R"]
            intensity = dict(zip(colors, image[j, i]))
            
            # Ajouter un sommet au graphe représentant la position du pixel et ses intensités de couleur
            image_graph.add_vertex(i, j, intensity)

    # Parcourir chaque sommet dans le graphe pour créer des arêtes entre les pixels voisins
    for vertex in image_graph.vertices:
        # Vérifier les voisins verticals
        for i in [-1, 1]:
            if 0 <= vertex.line + i < height:
                neighbor = image_graph.get_vertex(vertex.line + i, vertex.column)
                if neighbor:
                    # Ajouter des arêtes entre les sommets s'ils ne sont pas déjà connectés
                    if not vertex.isNeighbor(neighbor) and not neighbor.isNeighbor(vertex):
                        image_graph.add_edge(vertex, neighbor)

        # Vérifier les voisins horizontals
        for j in [-1, 1]:
            if 0 <= vertex.column + j < width:
                neighbor = image_graph.get_vertex(vertex.line, vertex.column + j)
                if neighbor:
                    # Ajouter des arêtes entre les sommets s'ils ne sont pas déjà connectés
                    if not vertex.isNeighbor(neighbor) and not neighbor.isNeighbor(vertex):
                        image_graph.add_edge(vertex, neighbor)
    
    return image_graph