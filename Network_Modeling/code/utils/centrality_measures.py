import networkx as nx
import operator
import numpy as np

# def ComputeCentralityMeasures(centrality_measure, net, list_of_authors):
#
#     try:
#         if centrality_measure == 'degree':
#             centrality = sorted(nx.degree_centrality(net).items(), key=operator.itemgetter(1), reverse=True)
#
#         if centrality_measure == 'betweenness':
#             centrality = sorted(nx.betweenness_centrality(net).items(), key=operator.itemgetter(1), reverse=True)
#
#         if centrality_measure == 'closeness':
#             centrality = sorted(nx.closeness_centrality(net).items(), key=operator.itemgetter(1), reverse=True)
#
#     except IndexError:
#         print('IndexError')
#
#     # *** check the degreee of centrality of users who use the target word ***
#
#     print('\nChecking the degree of centrality for users that used the target word...')
#
#     values_centrality_users_that_used_the_target_word = []
#     # values_centrality_other_users = []
#
#     for element in centrality:
#         if element[0] in list_of_authors:
#             values_centrality_users_that_used_the_target_word.append(element[1])
#
#     # compute mean centrality value for users who used the target word
#     mean_centrality_users_that_used_the_target_word = np.mean(values_centrality_users_that_used_the_target_word)
#     # compute std centrality value for users who used the target word
#     std_centrality_users_that_used_the_target_word = np.std(values_centrality_users_that_used_the_target_word)
#
#     print('done')
#
#     # get the min and max values of centrality
#     try:
#         max_centrality_value = centrality[0][1]
#         min_centrality_value = centrality[-1][1]
#     except IndexError:
#         print('IndexError')
#
#     # return centrality, mean_centrality_users_that_used_the_target_word, std_centrality_users_that_used_the_target_word, max_centrality_value, min_centrality_value


def ComputeCentralityMeasures(centrality_measure, net):

    if centrality_measure == 'degree':
        centrality = sorted(nx.degree_centrality(net).items(), key=operator.itemgetter(1), reverse=False)
        centrality = [(x[0],round(x[1],2)) for x in centrality]
        return centrality
    if centrality_measure == 'betweenness':
        # number_of_nodes = len(nx.nodes(net))
        # print('tot number of nodes:', number_of_nodes)
        # print('20%:', int((number_of_nodes*20)/100))
        centrality = sorted(nx.betweenness_centrality(net).items(), key=operator.itemgetter(1), reverse=False)
        return centrality
    if centrality_measure == 'closeness':
        centrality = sorted(nx.closeness_centrality(net).items(), key=operator.itemgetter(1), reverse=False)
        return centrality
    if centrality_measure == 'eigenvector':
        centrality = sorted(nx.eigenvector_centrality_numpy(net).items(), key=operator.itemgetter(1), reverse=False)
        return centrality


    # # *** check the degreee of centrality of users who use the target word ***
    #
    # print('\nChecking the degree of centrality for users that used the target word...')
    #
    # values_centrality_users_that_used_the_target_word = []
    # # values_centrality_other_users = []
    #
    # for element in centrality:
    #     if element[0] in list_of_authors:
    #         values_centrality_users_that_used_the_target_word.append(element[1])
    #
    # # compute mean centrality value for users who used the target word
    # mean_centrality_users_that_used_the_target_word = np.mean(values_centrality_users_that_used_the_target_word)
    # # compute std centrality value for users who used the target word
    # std_centrality_users_that_used_the_target_word = np.std(values_centrality_users_that_used_the_target_word)
    #
    # print('done')
    #
    # # get the min and max values of centrality
    # try:
    #     max_centrality_value = centrality[0][1]
    #     min_centrality_value = centrality[-1][1]
    # except IndexError:
    #     print('IndexError')


