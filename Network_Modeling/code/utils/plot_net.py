import networkx as nx
import matplotlib.pyplot as plt
import pylab
import numpy as np

# def PlotNet(net, list_of_authors, subreddit_name, time_bin, target_word, time_span):
#
#     print('\nPreparing the data for plotting...')
#
#
#     edges, weights = zip(*nx.get_edge_attributes(net, 'weight').items())
#
#     colors = dict()
#     sizes = dict()
#
#     for node in nx.nodes(net):
#         if node in list_of_authors:
#             # colors[node] = 'red'
#             # sizes[node] = 200
#             colors[node] = 'grey'
#             sizes[node] = 5
#
#         else:
#             colors[node] = 'grey'
#             sizes[node] = 5
#
#     colors = [colors.get(node) for node in net.nodes()]
#     sizes = [sizes.get(node) for node in net.nodes()]
#
#     degrees = sorted(net.degree().values(), reverse=True)
#
#     # plot degrees distribution
#     plt.plot(degrees)
#     plt.savefig("../plots/degrees_distribution/degrees_{0}_{1}_{2}_{3}.png".format(subreddit_name, time_span, str(time_bin[0]), target_word))
#     plt.close()
#
#     # plot weigths distribution
#     plt.plot(sorted(weights, reverse=True))
#     plt.savefig("../plots/ties_stregth_distribution/degrees_{0}_{1}_{2}_{3}.png".format(subreddit_name, time_span, str(time_bin[0]), target_word))
#     plt.close()
#
#
#
#     print('done')
#
#     print('\nDrawing the net...')
#     nx.draw_networkx(net, node_size=sizes, with_labels=False, node_color=colors, alpha=0.5,
#                      width=1, edgelist=edges, edge_color=weights, edge_cmap=plt.cm.Blues)
#
#     # nx.draw_networkx(G, , edgelist=edges, edge_color=weights, width=10.0, edge_cmap=plt.cm.Blues)
#
#     print('done')
#
#     print('\nPlotting the net...')
#     F = pylab.gcf()
#     DefaultSize = F.get_size_inches()
#     F.set_size_inches((DefaultSize[0] * 2, DefaultSize[1] * 2))
#     # Size = F.get_size_inches()
#     F.savefig("../plots/nets/net_{0}_{1}_{2}_{3}.png".format(subreddit_name, time_span, str(time_bin[0]), target_word))
#
#     plt.close()
#     print('done')



# def PlotNet(net, time_bin, list_authors_and_ties_strenght, subreddit_name):
#
#     # print('\nPreparing the data for plotting...')
#
#     # edges, weights = zip(*nx.get_edge_attributes(net, 'weight').items())
#     # print(edges)
#     # colors = dict()
#     # sizes = dict()
#     ties_values = dict()
#
#     for node in nx.nodes(net):
#         for author in list_authors_and_ties_strenght:
#             if node == author[0]:
#                 ties_values[node]=float(author[1])
#     #     if node in list_of_authors:
#             # colors[node] = 'red'
#     #         # sizes[node] = 200
#     #         colors[node] = 'grey'
#     #         sizes[node] = 5
#     #
#     #     else:
#     #         colors[node] = 'grey'
#     #         sizes[node] = 5
#
#     # colors = [colors.get(node) for node in net.nodes()]
#     # sizes = [sizes.get(node) for node in net.nodes()]
#     # ties_values = [ties_values.get(node) for node in net.nodes()]
#     # degrees = sorted(net.degree().values(), reverse=True)
#
#     '''
#     # plot degrees distribution
#     # plt.plot(degrees)
#     # plt.savefig("../plots/degrees_distribution/degrees_{0}_{1}_{2}_{3}.png".format(subreddit_name, time_span, str(time_bin[0]), target_word))
#     # plt.close()
#
#     # plot weigths distribution
#     # plt.plot(sorted(weights, reverse=True))
#     # plt.savefig("../plots/ties_stregth_distribution/degrees_{0}_{1}_{2}_{3}.png".format(subreddit_name, time_span, str(time_bin[0]), target_word))
#     # plt.close()
#
#     # print('done')
#     '''
#
#     print('\nDrawing the net...')
#
#     pos = nx.random_layout(net)# the only usefule ones are random and spring
#
#     nx.draw_networkx(net,
#                      pos=pos,
#                      # node_size=sizes,
#                      with_labels=True,
#                      labels=ties_values,
#                      node_color=[ties_values.get(node) for node in net.nodes()],
#                      cmap=plt.cm.Reds
#                      # alpha=0.5,
#                      # width=1,
#                      # edgelist=edges,
#                      # edge_color=weights,
#                      # edge_cmap=plt.cm.Blues
#                      )
#
#     # nx.draw_networkx(G, , edgelist=edges, edge_color=weights, width=10.0, edge_cmap=plt.cm.Blues)
#
#     print('done')
#
#     print('\nPlotting the net...')
#     F = pylab.gcf()
#     DefaultSize = F.get_size_inches()
#     F.set_size_inches((DefaultSize[0] * 2, DefaultSize[1] * 2))
#     # Size = F.get_size_inches()
#     # F.savefig("../plots/nets/net_{0}_{1}_{2}_{3}.png".format(subreddit_name, time_span, str(time_bin[0]), target_word))
#     F.savefig("../plots/nets/net_{0}_{1}.png".format(subreddit_name, time_bin))
#
#     plt.close()
#     print('done')




G=nx.Graph()

G.add_edge('a','b')
G.add_edge('a','c')

d = {'a': 1}

def PlotNet(net, dic_authors_and_ties_strenght, subreddit_name):

    # print('\nPreparing the data for plotting...')

    # edges, weights = zip(*nx.get_edge_attributes(net, 'weight').items())
    # print(edges)
    # colors = dict()
    # sizes = dict()
    ties_values = dict()

    for node in nx.nodes(net):
        for author in dic_authors_and_ties_strenght:
            if node == author:
                ties_values[node]=float(d[author])
        # if node in list_of_authors:
        #     colors[node] = 'red'
        #     sizes[node] = 200
            # colors[node] = 'grey'
    #         sizes[node] = 5
    #
    #     else:
    #         colors[node] = 'grey'
    #         sizes[node] = 5

    # colors = [colors.get(node) for node in net.nodes()]
    # sizes = [sizes.get(node) for node in net.nodes()]
    # ties_values = [ties_values.get(node) for node in net.nodes()]
    # degrees = sorted(net.degree().values(), reverse=True)

    '''
    # plot degrees distribution
    # plt.plot(degrees)
    # plt.savefig("../plots/degrees_distribution/degrees_{0}_{1}_{2}_{3}.png".format(subreddit_name, time_span, str(time_bin[0]), target_word))
    # plt.close()

    # plot weigths distribution
    # plt.plot(sorted(weights, reverse=True))
    # plt.savefig("../plots/ties_stregth_distribution/degrees_{0}_{1}_{2}_{3}.png".format(subreddit_name, time_span, str(time_bin[0]), target_word))
    # plt.close()

    # print('done')
    '''

    print('\nDrawing the net...')

    pos = nx.random_layout(net)# the only usefule ones are random and spring

    nx.draw_networkx(net,
                     pos=pos,
                     # node_size=sizes,
                     with_labels=True,
                     labels=ties_values,
                     node_color=[ties_values.get(node) for node in net.nodes()],
                     cmap=plt.cm.Reds
                     # alpha=0.5,
                     # width=1,
                     # edgelist=edges,
                     # edge_color=weights,
                     # edge_cmap=plt.cm.Blues
                     )

    # nx.draw_networkx(G, , edgelist=edges, edge_color=weights, width=10.0, edge_cmap=plt.cm.Blues)

    print('done')

    print('\nPlotting the net...')
    F = pylab.gcf()
    DefaultSize = F.get_size_inches()
    F.set_size_inches((DefaultSize[0] * 2, DefaultSize[1] * 2))
    # Size = F.get_size_inches()
    # F.savefig("../plots/nets/net_{0}_{1}_{2}_{3}.png".format(subreddit_name, time_span, str(time_bin[0]), target_word))
    F.savefig("./net_{0}.png".format(subreddit_name))

    plt.close()
    print('done')



PlotNet(G, d, 'graph_for_paper')