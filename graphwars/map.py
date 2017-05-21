import networkx as nx
import random
import numpy as np
from scipy.spatial import Delaunay


class Map:

    def __init__(self, map_size, dim_of_bases, num_players, buff_size,
                 buff_E, size_connectors, resources_dict):
        self.resources = resources_dict
        self.map, self.node_data = Map.generate_map(map_size, dim_of_bases, 
                            num_players, 
                            buff_size, buff_E, size_connectors)

    def generate_delaunay_main(N):
        pts = np.array([[random.random(), random.random()] for i in range(N)])
        delTri = Delaunay(pts)
        edges = set()
        for n in range(delTri.nsimplex):
            edge = sorted([delTri.vertices[n,0], delTri.vertices[n,1]])
            edges.add((edge[0], edge[1]))
            edge = sorted([delTri.vertices[n,0], delTri.vertices[n,2]])
            edges.add((edge[0], edge[1]))
            edge = sorted([delTri.vertices[n,1], delTri.vertices[n,2]])
            edges.add((edge[0], edge[1]))

        G = nx.Graph(list(edges))
        crdnts = pts[delTri.vertices]
        type_dict = {G.nodes()[i]: 'main' for i in range(N)}
        coors = np.empty(N, dtype = np.ndarray)
        for n in range(delTri.nsimplex):
            for i in range(3):
                idx = G.nodes().index(delTri.vertices[n,i])
                coors[idx] = crdnts[n, i]

        coordinate_dict = {G.nodes()[i]: coors[i] for i in range(N)}
        nx.set_node_attributes(G, 'type', type_dict)
        nx.set_node_attributes(G, 'pos', coordinate_dict)

        return G

    def generate_base(n1, n2, player_ID, map_position):
        G = nx.grid_2d_graph(n1, n2)
        type_dict = {G.nodes()[i]: ('base', player_ID) for i in range(n1*n2)}
        nx.set_node_attributes(G, 'type', type_dict)
        pos_dict = {}
        for node in G.nodes(): 
            i = node[0]
            j = node[1]
            if map_position == 'N':
                pos_dict[node] = [i/(2 * n2) + 0.25 , j/(2 * n1) + 1.5]
            if map_position == 'E':
                pos_dict[node] = [i/(2 * n2) + 1.5 , j/(2 * n1) + 0.25]
            if map_position == 'S':
                pos_dict[node] = [i/(2 * n2) + 0.25 , -j/(2 * n1) - 0.5]
            if map_position == 'W':
                pos_dict[node] = [-i/(2 * n2) - 0.5 , j/(2 * n1) + 0.25]
        nx.set_node_attributes(G, 'pos', pos_dict)
        return G

    def generate_buffer_zone(N, E, player_ID, map_position):
        p = 2 * E/(N * (N-1))
        G = nx.erdos_renyi_graph(N, p)
        type_dict = {G.nodes()[i]: ('buffer', player_ID) for i in range(N)}
        nx.set_node_attributes(G, 'type', type_dict)
        pos_dict = {}
        for node in G.nodes():
            i = random.random()/2
            j = random.random()
            if map_position == 'N':
                pos_dict[node] = [j, i + 1]
            if map_position == 'E':
                pos_dict[node] = [i+1,j]
            if map_position == 'S':
                pos_dict[node] = [j, -i]
            if map_position == 'W':
                pos_dict[node] = [-i, j]
        nx.set_node_attributes(G, 'pos', pos_dict)
        return G

    def generate_map(map_size, dim_of_bases,
                     num_bases, buff_size, buff_E,
                     size_connectors):

        main = Map.generate_delaunay_main(map_size)
        full_G = main
        player_pos = {0:'N', 1:'S', 2:'E', 3:'W'}
        for player in range(num_bases):
            player_base = Map.generate_base(dim_of_bases, dim_of_bases, 
                                            player, player_pos[player])
            player_buffer = Map.generate_buffer_zone(buff_size, buff_E, 
                                            player, player_pos[player])
            full_base = nx.disjoint_union(player_base, player_buffer)
            full_G = nx.disjoint_union(full_G, full_base)
        data_nodes = {}
        data_nodes['main'] = []
        data_nodes['base_1'] = []
        data_nodes['base_2'] = []
        data_nodes['base_3'] = []
        data_nodes['base_0'] = []
        data_nodes['buff_1'] = []
        data_nodes['buff_2'] = []
        data_nodes['buff_3'] = []
        data_nodes['buff_0'] = []
        for node in full_G.nodes():
            node_type = full_G.node[node]['type']
            if node_type == 'main':
                data_nodes['main'].append(node)
            for i in range(4):
                if node_type == ('base', i):
                    data_nodes['base_' + str(i)].append(node)
                if node_type == ('buffer', i):
                    data_nodes['buff_' + str(i)].append(node)

        return full_G, data_nodes
