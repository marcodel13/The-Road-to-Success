import networkx as nx
import operator
import numpy as np
import matplotlib.pyplot as plt
import os


def RetrieveWeakTies(edge_list, net, subreddit):

    '''using the methodology introduced by Onnella et al. 2007, compute the strength of each tie (edge)
       If strength == 0, it is an edge connecting two user that do not have common neighbors, and therefore a week ties.
       If strength == 1, the two users completely share their neighbors, and the edge has the maximum possible value of strength'''

    number_of_TE = 0
    for edge in edge_list:
        try:
            o = len(sorted(nx.common_neighbors(net, edge[0], edge[1]))) / (((net.degree(edge[0]) - 1) + (net.degree(edge[1]) - 1)) - len(sorted(nx.common_neighbors(net, edge[0], edge[1]))))
            net[edge[0]][edge[1]]['strength'] = round(o, 3)
            # print('ok')
        except ZeroDivisionError:
            net[edge[0]][edge[1]]['strength'] = 0
            # print('ZDE')
        except TypeError:
            net[edge[0]][edge[1]]['strength'] = 0
            number_of_TE += 1

    nodes_strength_dic = dict()
    for edge in net.edges(data=True):

        if edge[0] in nodes_strength_dic:
            nodes_strength_dic[edge[0]].append(net[edge[0]][edge[1]]['strength'])

        if edge[0] not in nodes_strength_dic:
            nodes_strength_dic[edge[0]]=[net[edge[0]][edge[1]]['strength']]

        if edge[1] in nodes_strength_dic:
            nodes_strength_dic[edge[1]].append(net[edge[0]][edge[1]]['strength'])

        if edge[1] not in nodes_strength_dic:
            nodes_strength_dic[edge[1]] = [net[edge[0]][edge[1]]['strength']]

    argmax_nodes_strength_dic = dict()

    for node in nodes_strength_dic:
        argmax_nodes_strength_dic[node] = max(nodes_strength_dic[node])

    sorted_argmax_nodes_strength_list = sorted(argmax_nodes_strength_dic.items(), key=operator.itemgetter(1))

    all_ties = []
    for item in argmax_nodes_strength_dic:
        all_ties.append(argmax_nodes_strength_dic[item])

    if not os.path.exists('../all_ties/{0}/'.format(subreddit)):
        os.makedirs('../all_ties/{0}/'.format(subreddit))
    with open('../all_ties/{0}/all_max_ties_{0}.txt'.format(subreddit),'a') as all_max_ties:
        all_max_ties.write(str(all_ties) + '\n')

    return sorted_argmax_nodes_strength_list, nodes_strength_dic