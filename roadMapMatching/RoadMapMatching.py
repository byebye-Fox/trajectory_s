import osmnx as ox
import pandas as pd
import networkx as nx
import numpy as np

def compute_shortest_path_len(road_network, pre_point, next_point):
    shortest_path_length = np.PINF
    shortest_path_length = np.PINF
    node_path = []
    if (pre_point['e_i'] == next_point['e_i']) \
            and not ((pre_point['oneway'])
                     and (pre_point['i_p_i'] != next_point['i_p_i'])
                     and (next_point['edge_progress'] - pre_point['edge_progress'] < 0)):
        shortest_path_length = abs(next_point['edge_progress'] - pre_point['edge_progress']) * pre_point['length']
        # print(pre_point['u'], pre_point['v'], pre_point['end_node'], next_point['end_node'])
    elif (0 == pre_point['end_node']) & (0 == next_point['end_node']):
        if pre_point['oneway'] & next_point['oneway']:
            try:
                temp_length = (pre_point['length'] * (1 - pre_point['edge_progress'])
                               + nx.shortest_path_length(road_network,
                                                         pre_point['v'], next_point['u'],
                                                         weight='length')
                               + next_point['length'] * next_point['edge_progress']
                               )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['v'], next_point['u']]
            except:
                pass
        elif ~pre_point['oneway'] & next_point['oneway']:
            # pre seg forward, next seg forward
            try:
                temp_length = (pre_point['length'] * (1 - pre_point['edge_progress'])
                               + nx.shortest_path_length(road_network,
                                                         pre_point['v'], next_point['u'],
                                                         weight='length')
                               + next_point['length'] * next_point['edge_progress']
                               )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['v'], next_point['u']]
            except:
                pass
            # pre seg backward, next seg forward
            try:
                temp_length = (pre_point['length'] * pre_point['edge_progress']
                               + nx.shortest_path_length(road_network,
                                                         pre_point['u'], next_point['u'],
                                                         weight='length')
                               + next_point['length'] * next_point['edge_progress']
                               )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['u'], next_point['u']]
            except:
                pass
        elif pre_point['oneway'] & ~next_point['oneway']:
            # pre seg forward, next seg forward
            try:
                temp_length = (pre_point['length'] * (1 - pre_point['edge_progress'])
                               + nx.shortest_path_length(road_network,
                                                         pre_point['v'], next_point['u'],
                                                         weight='length')
                               + next_point['length'] * next_point['edge_progress']
                               )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['v'], next_point['u']]
            except:
                pass
            # pre seg forward, next seg backward
            try:
                temp_length = (pre_point['length'] * (1 - pre_point['edge_progress'])
                               + nx.shortest_path_length(road_network,
                                                         pre_point['v'], next_point['v'],
                                                         weight='length')
                               + next_point['length'] * (1 - next_point['edge_progress'])
                               )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['v'], next_point['v']]
            except:
                pass
        elif ~pre_point['oneway'] & ~next_point['oneway']:
            # pre seg forward, next seg forward
            try:
                temp_length = (pre_point['length'] * (1 - pre_point['edge_progress'])
                               + nx.shortest_path_length(road_network,
                                                         pre_point['v'], next_point['u'],
                                                         weight='length')
                               + next_point['length'] * next_point['edge_progress']
                               )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['v'], next_point['u']]
            except:
                pass
            # pre seg backward, next seg forward
            try:
                temp_length = (pre_point['length'] * pre_point['edge_progress']
                               + nx.shortest_path_length(road_network,
                                                         pre_point['u'], next_point['u'],
                                                         weight='length')
                               + next_point['length'] * next_point['edge_progress']
                               )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['u'], next_point['u']]
            except:
                pass
            # pre seg forward, next seg backward
            try:
                temp_length = (
                        pre_point['length'] * (1 - pre_point['edge_progress'])
                        + nx.shortest_path_length(road_network, pre_point['v'], next_point['v'], weight='length')
                        + next_point['length'] * (1 - next_point['edge_progress'])
                )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['v'], next_point['v']]
            except:
                pass
            # pre seg backward, next seg backward
            try:
                temp_length = (
                        pre_point['length'] * pre_point['edge_progress']
                        + nx.shortest_path_length(road_network, pre_point['u'], next_point['v'], weight='length')
                        + next_point['length'] * (1 - next_point['edge_progress'])
                )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['u'], next_point['v']]
            except:
                pass
    elif (0 != pre_point['end_node']) & (0 == next_point['end_node']):
        if 1 == pre_point['end_node']:
            pre_node = 'u'
        elif 2 == pre_point['end_node']:
            pre_node = 'v'
        if next_point['oneway']:
            try:
                temp_length = (
                        nx.shortest_path_length(road_network, pre_point[pre_node], next_point['u'],
                                                weight='length')
                        + next_point['length'] * next_point['edge_progress']
                )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point[pre_node], next_point['u']]
            except:
                pass
        elif ~next_point['oneway']:
            # next seg forward
            try:
                temp_length = (
                        nx.shortest_path_length(road_network, pre_point[pre_node], next_point['u'],
                                                weight='length')
                        + next_point['length'] * next_point['edge_progress']
                )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point[pre_node], next_point['u']]
            except:
                pass
            # next seg backward
            try:
                temp_length = (
                        nx.shortest_path_length(road_network, pre_point[pre_node], next_point['v'],
                                                weight='length')
                        + next_point['length'] * (1 - next_point['edge_progress'])
                )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point[pre_node], next_point['v']]
            except:
                pass
    elif (0 == pre_point['end_node']) & (0 != next_point['end_node']):
        if 1 == next_point['end_node']:
            next_node = 'u'
        elif 2 == next_point['end_node']:
            next_node = 'v'
        if pre_point['oneway']:
            try:
                temp_length = (
                        pre_point['length'] * (1 - pre_point['edge_progress'])
                        + nx.shortest_path_length(road_network, pre_point['v'], next_point[next_node],
                                                  weight='length')
                )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['v'], next_point[next_node]]
            except:
                pass
        elif ~pre_point['oneway']:
            # next seg forward
            try:
                temp_length = (
                        pre_point['length'] * (1 - pre_point['edge_progress'])
                        + nx.shortest_path_length(road_network, pre_point['v'], next_point[next_node],
                                                  weight='length')
                )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['v'], next_point[next_node]]
            except:
                pass
            # next seg backward
            try:
                temp_length = (
                        pre_point['length'] * pre_point['edge_progress']
                        + nx.shortest_path_length(road_network, pre_point['u'], next_point[next_node],
                                                  weight='length')
                )
                if temp_length < shortest_path_length:
                    shortest_path_length = temp_length
                    node_path = [pre_point['u'], next_point[next_node]]
            except:
                pass
    elif (0 != pre_point['end_node']) & (0 != next_point['end_node']):
        if 1 == pre_point['end_node']:
            pre_node = 'u'
        elif 2 == pre_point['end_node']:
            pre_node = 'v'
        if 1 == next_point['end_node']:
            next_node = 'u'
        elif 2 == next_point['end_node']:
            next_node = 'v'
        try:
            temp_length = (
                nx.shortest_path_length(road_network, pre_point[pre_node], next_point[next_node],
                                        weight='length')
            )
            if temp_length < shortest_path_length:
                shortest_path_length = temp_length
                node_path = [pre_point[pre_node], next_point[next_node]]
        except:
            pass

    if len(node_path):
        node_path = nx.shortest_path(road_network, node_path[0], node_path[1], weight='length')
    return shortest_path_length, node_path

def Route_To_Points(G,route):

    x = []
    y = []

    for u, v in zip(route[:-1], route[1:]):
        # if there are parallel edges, select the shortest in length
        data = min(G.get_edge_data(u, v).values(), key=lambda d: d["length"])
        if "geometry" in data:
            # if geometry attribute exists, add all its coords to list
            xs, ys = data["geometry"].xy
            x.extend(xs)
            y.extend(ys)
        else:
            # otherwise, the edge is a straight line from node to node
            x.extend((G.nodes[u]["x"], G.nodes[v]["x"]))
            y.extend((G.nodes[u]["y"], G.nodes[v]["y"]))

    result = []
    for i in range(0, len(x)):
        result.append([y[i], x[i]])
    return result

def filePoints(network , filename):
    road_network = ox.load_graphml(network)
    road_path = pd.read_csv(filename)
    shenzhen_road_network = ox.truncate.truncate_graph_bbox(road_network,
                                                            road_path['y'].max() + 0.03,
                                                            road_path['y'].min() - 0.03,
                                                            road_path['x'].max() + 0.03,
                                                            road_path['x'].min() - 0.03)
    route = []
    for i in range(len(road_path.index))[1:]:
        # if 75 == i:
        #     print('cool')
        _, sub_path = compute_shortest_path_len(shenzhen_road_network, road_path.iloc[i - 1], road_path.iloc[i])
        # 返回的结果是两个，一个是距离，另一个是subpath
        if len(route) and len(sub_path) and (route[-1] == sub_path[0]):
            route.extend(sub_path[1:])
        else:
            route.extend(sub_path)

    result = Route_To_Points(shenzhen_road_network , route)
    return result

def oriTra(filenaem):
    orifile = pd.read_csv(filenaem)
    row = orifile.shape[0]
    result = {
        'rawpairs' : [],
        'oripairs' : []
    }
    for i in range(0 , row):
        onetip = orifile.iloc[i,:]
        orilng = onetip[5]
        orilat = onetip[6]
        rawlng = onetip[12]
        rawlat = onetip[13]
        result['rawpairs'].append([rawlat,rawlng])
        result['oripairs'].append([orilat , orilng])
    return result