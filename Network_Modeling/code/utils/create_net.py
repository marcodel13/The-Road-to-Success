import re
import argparse
import itertools
from collections import defaultdict
from os.path import basename
import networkx as nx


# input_file = open('/Users/marcodeltredici/workspace/DATA/LiverpoolFC/201505.txt').readlines()
# input_file = open('/Users/marcodeltredici/workspace/PYCHARM/new_exp/experiment_2/network_modeling/data/fake-2009.txt').readlines()

'''ONE HOP (INITIAL) VERSION'''
# def CreateLookUpTable(file):
#     '''
#     define a lookup table in which keys are ids and values are authors
#     :param file:
#     :return: lookuptable
#     '''
#
#     i = 0
#
#     # list_id_authors = []
#
#     dic_id_authors = dict()
#
#     print('\nStart creating lookup table')
#
#     for line in file:
#
#
#         # if "'author':" in line:
#
#         if "'author': None" in line:
#             author = ['None']
#             # outputfile.write(str(author) + '\n')
#             # list_authors.append(author)
#             # i += 1
#
#         else:
#             author = (re.findall(r"'author': '(.*?)'",line))
#             # outputfile.write(str(author[0]) + '\n')
#             # list_authors.append(author[0])
#             # i += 1
#
#         id = (re.findall(r"'id': '(.*?)'", line))
#
#         # key is id, v is author
#         if id[0] not in dic_id_authors:
#             dic_id_authors[id[0]] = [author[0]]
#         else:# this part is useless because ids are always unique
#             dic_id_authors[id[0]].append(author[0])
#
#     print('done')
#     print('\nRemove None authors')
#
#     cleaned_dic = dict()
#
#     for key in dic_id_authors:
#         if 'None' not in dic_id_authors[key]:
#             cleaned_dic[key]=dic_id_authors[key]
#
#     print('done')
#     return cleaned_dic
#
# def CreateNet(file, lookup_dic):
#     '''
#     take as inout the lookup table. loop over the input data and instantiate edge between author in line and author of the parent comment/post
#     :param file:
#     :param lookup_dic:
#     :return: net
#     '''
#     print('\nBuilding the net')
#
#     net = nx.Graph()
#
#     print('Looping over lines...')
#
#     for line in file:
#
#         # identify the author
#
#         if "'author': None" not in line:
#
#             author = (re.findall(r"'author': '(.*?)'", line))
#             author = author[0]
#
#         # identify the parent id
#
#         if "'parent_id': " in line:
#             parent = (re.findall(r"'parent_id': '(.*?)'", line))
#             parent = parent[0]
#
#         else:
#             parent = 'no_parent'
#
#         # look up for the author of the parent message
#
#         if parent in lookup_dic:
#
#             # add or instantiate edges (note: direction is not taken into account)
#             if net.has_edge(author, lookup_dic[parent][0]):
#                 net[author][lookup_dic[parent][0]]['weight'] += 1
#             else:
#                 if author != lookup_dic[parent][0]:
#                     net.add_edge(author, lookup_dic[parent][0], weight=1)
#
#     print('\nDone!')
#
#
#     return net
#
# def ComputeNetStats(net):
#
#     order = net.order()
#     size = net.size()
#
#     try:
#         average_degree = round(net.size() / net.order(), 3)
#     except ZeroDivisionError:
#         average_degree = 0
#
#     try:
#         average_clustering_coefficient = nx.average_clustering(net)
#     except ZeroDivisionError:
#         average_clustering_coefficient = 0
#
#     density = round(nx.density(net), 3)
#
#     return order, size, average_degree, average_clustering_coefficient, density

# CreateNet(input_file, CreateLookUpTable(input_file))


'''NEW VERSION --> MORE HOP'''
def CreateLookUpTable(file):
    '''
    define a lookup table in which keys are ids and values are authors
    :param file:
    :return: lookuptable
    '''

    i = 0

    dic_id_authors = dict()

    # print('\nStart creating lookup table')

    for line in file:

        if "'author': None" not in line:

            author = (re.findall(r"'author': '(.*?)'",line))
            # author = author[0]
            # author = int(author[0])
            try:
                author = int(author[0])
            except ValueError:
                author = author[0]

            id = (re.findall(r"'id': '(.*?)'", line))

            if "'parent_id': " in line:
                parent = (re.findall(r"'parent_id': '(.*?)'", line))
                parent = parent[0]

            else:
                parent = 'no_parent'

            # key is id, v is author
            if id[0] not in dic_id_authors:
                dic_id_authors[id[0]] = [(author,parent)]

    # print('done')
    # print('\nRemove None authors')

    cleaned_dic = dict()

    for key in dic_id_authors:
        if 'None' not in dic_id_authors[key]:
            cleaned_dic[key]=dic_id_authors[key]

    # print('done')
    return cleaned_dic

def CreateNet(file, lookup_dic):
    '''
    take as inout the lookup table. loop over the input data and instantiate edge between author in line and author of the parent comment/post
    :param file:
    :param lookup_dic:
    :return: net
    '''
    # print(lookup_dic)

    # print('\nBuilding the net')

    net = nx.Graph()

    # print('Looping over lines...')

    for line in file:

        # identify the author

        if "'author': None" not in line:

            author = (re.findall(r"'author': '(.*?)'", line))
            # author = author[0]
            # author = int(author[0])
            try:
                author = int(author[0])
            except ValueError:
                author = author[0]


            # identify the parent id

            if "'parent_id': " in line:
                parent = (re.findall(r"'parent_id': '(.*?)'", line))
                parent = parent[0]

            else:
                parent = 'no_parent'

            # look up for the author of the parent message

            if parent in lookup_dic:

                # print('author', author)

                # add or instantiate edges for the first hop (note: direction is not taken into account)

                first_hop_author = lookup_dic[parent][0][0]
                # print('first_hop_author', first_hop_author)
                first_hop_parent = lookup_dic[parent][0][1]
                # print('first_hop_parent',first_hop_parent)


                if net.has_edge(author, first_hop_author):
                    net[author][lookup_dic[parent][0][0]]['weight'] += 1
                else:
                    if author != first_hop_author: # this line is to avoid self links
                        net.add_edge(author, first_hop_author, weight=1)
                    # else:
                        # break
                        # continue

                # add or instantiate edges for the second hop
                if first_hop_parent in lookup_dic:

                    second_hop_author = lookup_dic[first_hop_parent][0][0]
                    second_hop_parent = lookup_dic[first_hop_parent][0][1]
                    # print('second_hop_author', second_hop_author)
                    # print('second_hop_parent', second_hop_parent)

                    if net.has_edge(author, second_hop_author):
                        net[author][second_hop_author]['weight'] += 1
                    else:
                        if author != second_hop_author:  # this line is to avoid self links
                            # print('author, second_hop_author', author, second_hop_author)
                            net.add_edge(author, second_hop_author, weight=1)
                        # else:
                        #     break
                else:
                    # print('no second hop')
                    continue

                # add or instantiate edges for the third hop
                try:

                    if second_hop_parent in lookup_dic:

                        third_hop_author = lookup_dic[second_hop_parent][0][0]
                        # print('third_hop_author', third_hop_author)
                        if net.has_edge(author, third_hop_author):
                            net[author][third_hop_author]['weight'] += 1
                        else:
                            if author != third_hop_author:  # this line is to avoid self links
                                net.add_edge(author, third_hop_author, weight=1)
                    else:
                        # print('no second hop')
                        continue

                except UnboundLocalError:
                    # print('no third hop')
                    continue


                # print('\n')
    # print('\nDone!')

    # print(net.edges(data=True))


    return net

def ComputeNetStats(net, list_of_results):
    
    list_of_results.append("\nNETWORK DATA:")
    
    order = net.order()
    size = net.size()

    try:
        average_degree = round(net.size() / net.order(), 3)
    except ZeroDivisionError:
        average_degree = 0

    try:
        average_clustering_coefficient = nx.average_clustering(net)
    except ZeroDivisionError:
        average_clustering_coefficient = 0

    density = round(nx.density(net), 3)

    list_of_results.append("Order (number of nodes)= {0}".format(str(order)))
    list_of_results.append("Size (number of edges)= {0}".format(str(size)))
    list_of_results.append("Average degree(Size/Order)= {0}".format(str(average_degree)))
    list_of_results.append("Average clustering coefficient (measure of cliqueness: 0=star, 1=clique)= {0}".format(str(average_clustering_coefficient)))
    list_of_results.append("Density= {0}".format(str(density)))

    return list_of_results
