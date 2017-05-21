from map import Map
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np
from scipy.spatial import Delaunay

pts = np.array([[random.random(), random.random()] for i in range(10)])
delTri = Delaunay(pts)
print(delTri.vertices)

G = Map(40, 3, 2, 10, 10, 5, 0)
#pos_dict = {G.map.nodes()[i]: G.map.node[i]['pos'] for i in range(78)}
nx.draw_networkx(G.map, with_labels=False)
plt.show()
