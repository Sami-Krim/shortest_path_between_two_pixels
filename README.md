# Shortest path between two pixels

This project involves working with a specific graph structure known as an image grid. Pixels within an image can be seen as vertices of a graph, and the neighbor relationship represents binary edge connections. These edges can be weighted by the intensity difference between adjacent pixels.

## Project Overview

The primary objectives include:

- Constructing a graph derived from an input image.
- Designing a graphical interface enabling users to designate two pixels as start and end points.
- Implementing Dijkstra's algorithm to determine the shortest path in this weighted, undirected graph between the selected vertices.
- Visualizing the calculated path over the image.

## Implementation Details

### Graph Structure

Vertices are represented by pixel indices (i, j), where i signifies the row and j signifies the column in the image matrix. The 4-connectedness defines neighboring vertices as (i+1, j), (i-1, j), (i, j+1), and (i, j-1).

### Language Choice

I have chosen Python as the language for implementation.

### Dependencies

To use this code, you'll need to have the following dependencies installed:

- [OpenCV](https://opencv.org/) - Open Source Computer Vision Library.
- [PyQt5](https://riverbankcomputing.com/software/pyqt/intro) - Python bindings for the Qt application framework.

### Usage Instructions

To utilize the provided code:

1. Clone or download this repository.
2. Ensure you have the necessary dependencies installed (OpenCV and PyQt5).
3. Run the `interface.py` file.
4. Use the file chooser within the interface to select an image.
5. Designate the start and end pixels within the selected image.
6. Observe the generated shortest path displayed over the image.
