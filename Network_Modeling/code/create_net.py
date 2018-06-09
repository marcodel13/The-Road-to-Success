import argparse
import networkx as nx
import numpy as np
import os
import re
import math

''' IMPORT '''

from utils.create_net import CreateLookUpTable, CreateNet, ComputeNetStats
from utils.define_time_bins import DefineTimestamps
from utils.tokenize_text import ReturnTokenizedText
from utils.retrieve_weak_ties import RetrieveWeakTies
from utils.centrality_measures import ComputeCentralityMeasures
from utils.plot_net import PlotNet



''' GET ARGS '''

def Parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-data_path', type = str, help = "Specify data path")
    parser.add_argument('-subreddit', type = str, help = "Specify subreddit name")
    parser.add_argument('-time_span', type = str, help = "[month|week]", default='month')
    parser.add_argument('-centrality', type = str, help = "Centrality measure. [degree|betweenness|closeness|eigenvector]", default='none')
    parser.add_argument('-min_number_of_users', type=int, help="min number of users for a time bin to be considered", default='200')
    parser.add_argument('-plot_net', type = bool, help = "plot the net for each month", default=False)
    return parser.parse_args()


''' FUNCTIONS '''

def Main(args, list_of_time_bins):
    results_lists = []
    frequencies_per_time_bin = []
    time_bins_for_plotting = []
    max_strenght_users_that_used_the_target_word_for_plotting = []
    average_ties_strength_users_that_used_the_target_word_for_plotting = []

    list_of_words = open('../../Innovations_Detection/results/' + args.subreddit + '/' + args.subreddit + '_all_forms_simple_spread.txt').readlines()

    num_of_time_bins = len([float(x) for x in re.findall(r"\[(.+)\]", list_of_words[0])[0].split(',')])
    list_of_words = [line.split()[0] for line in list_of_words]

    dic_all_words_max = dict()
    dic_all_words_average = dict()
    dic_all_words_median = dict()

    dic_very_first_values = dict()

    for word in list_of_words:
        dic_all_words_max[word]=[]
        dic_all_words_average[word] = []
        dic_all_words_median[word] = []
        dic_very_first_values[word] = []

    list_of_time_bins = list_of_time_bins[-num_of_time_bins:]

    for time_bin in list_of_time_bins:

        timestamp = time_bin[0]
        data = time_bin[1]
        authors = [re.findall(r"'author': '(.*?)'", x) for x in data]
        authors = [x[0] for x in authors if len(x)>0]
        unique_authors = list(set(authors))

        print('\nTime bin {0}'.format(timestamp))
        print('number of unique authors: {0}'.format(len(unique_authors)))

        time_bins_for_plotting.append(timestamp)
        time_bin_list = []
        time_bin_list.append("time_bin {0}".format(str(timestamp)))

        net = CreateNet(data, CreateLookUpTable(data))

        time_bin_list = ComputeNetStats(net, time_bin_list)

        ''' using the methodology introduced by Onnella 2007, compute the strenght of the ties for each user'''

        list_authors_and_ties_strenght, nodes_strength_dic = RetrieveWeakTies(nx.edges(net),net, args.subreddit)
        try:
            max_strength_overall_ties_strength = sorted(list_authors_and_ties_strenght, key=lambda x: x[1], reverse=True)[0][1]
        except IndexError:
            print('error!')

        ''' compute the relevant centrality measure '''
        if args.centrality != 'none':
            list_authors_and_centrality = ComputeCentralityMeasures(args.centrality, net)
            if not os.path.exists('../all_ties/{0}/'.format(args.subreddit)):
                os.makedirs('../all_ties/{0}/'.format(args.subreddit))
            with open('../all_ties/{0}/all_ties_{0}_{1}.txt'.format(args.subreddit, args.centrality), 'a') as all_centrality_ties:
                all_centrality_ties.write(str([x[1] for x in list_authors_and_centrality]) + '\n')
            try:
                max_strength_overall_centrality = sorted(list_authors_and_centrality, key=lambda x: x[1], reverse=True)[0][1]
            except IndexError:
                print('error!')

        tok_text, authors = ReturnTokenizedText(data, list_of_words)
        new_dict = dict()
        for line in enumerate(tok_text):
            for item in line[1]:
                if item not in new_dict:
                    new_dict[item]=[authors[line[0]]]
                else:
                    if authors[line[0]] not in new_dict[item]:
                        new_dict[item].append(authors[line[0]])
        for word in list_of_words:
            if word not in new_dict:
                new_dict[word]=[]

        if args.centrality == 'none':
            list_authors_and_target_measure = list_authors_and_ties_strenght
            max_strength_overall = max_strength_overall_ties_strength
        else:
            list_authors_and_target_measure = list_authors_and_centrality
            max_strength_overall = max_strength_overall_centrality

        for word,list_of_authors_that_used_tw in new_dict.items():
            dict_word = dict()
            dict_word[word]=[]
            for aut in list_of_authors_that_used_tw:
                dict_word[word].append([x[1] for x in list_authors_and_target_measure if x[0] == aut])
            sorted_ties_strength_users_that_used_the_target_word = sorted(sum(dict_word[word], []))
            unsorted_ties_strength_users_that_used_the_target_word = sum(dict_word[word], [])

            for item in unsorted_ties_strength_users_that_used_the_target_word:
                dic_very_first_values[word].append(item)

            average_ties_strength_users_that_used_the_target_word = float('%.2f' % round(np.mean(sorted_ties_strength_users_that_used_the_target_word), 2))
            if math.isnan(average_ties_strength_users_that_used_the_target_word):
                average_ties_strength_users_that_used_the_target_word = 0
            dic_all_words_average[word].append(average_ties_strength_users_that_used_the_target_word)

            median_ties_strength_users_that_used_the_target_word = np.median(sorted_ties_strength_users_that_used_the_target_word)
            if math.isnan(median_ties_strength_users_that_used_the_target_word):
                median_ties_strength_users_that_used_the_target_word = 0
            dic_all_words_median[word].append(median_ties_strength_users_that_used_the_target_word)

            try:
                max_strenght_users_that_used_the_target_word = float('%.2f' % round(sorted_ties_strength_users_that_used_the_target_word[-1] / max_strength_overall, 2))
            except (IndexError,ZeroDivisionError):
                max_strenght_users_that_used_the_target_word = 0

            dic_all_words_max[word].append(max_strenght_users_that_used_the_target_word)
            time_bin_list.append(
                "\nWord: {0}\nTies strength users that used the target word: {1}\nAverage ties strength users that used the target word: {2}\nMax strenght users that used the target word: {3}".format(
                    word,
                    str(unsorted_ties_strength_users_that_used_the_target_word),
                    str(average_ties_strength_users_that_used_the_target_word),
                    str(max_strenght_users_that_used_the_target_word)))
        time_bin_list.append("\n********************")
        results_lists.append(time_bin_list)

        if args.plot_net:
            PlotNet(net, timestamp, list_authors_and_ties_strenght, args.subreddit)

    def Check_with_innovations_file(dic):
        with open('../../Innovations_Detection/results/' + args.subreddit + '/' + args.subreddit + '_all_forms_simple_spread.txt') as diss_file:
            diss_file = diss_file.readlines()
            for line in diss_file:
                word = line.split()[0]
                traj_spread = [float(x) for x in re.findall(r"\[(.+)\]", line)[0].split(',')]
                if word in dic:
                    i = 0
                    while i < len(traj_spread):
                        if traj_spread[i]==0:
                            dic[word][i] = 0
                        i+=1
        return dic

    dic_all_words_average = Check_with_innovations_file(dic_all_words_average)
    dic_all_words_max = Check_with_innovations_file(dic_all_words_max)
    dic_all_words_median = Check_with_innovations_file(dic_all_words_median)
    # print('\nDone with {0}'.format(timestamp))

    if not os.path.exists('../results/{0}/'.format(args.subreddit)):
        os.makedirs('../results/{0}/'.format(args.subreddit))

    def Reorder_dic(list_of_words, dictionary):

        reordered_list = []

        for word in list_of_words:
            for key in dictionary:
                if word == key:
                    reordered_list.append((word, dictionary[word]))
        return reordered_list

    dic_very_first_values = Reorder_dic(list_of_words, dic_very_first_values)
    dic_all_words_average = Reorder_dic(list_of_words, dic_all_words_average)
    dic_all_words_median = Reorder_dic(list_of_words, dic_all_words_median)
    dic_all_words_max = Reorder_dic(list_of_words, dic_all_words_max)

    if args.centrality == 'none':
        with open('../results/{0}/results_{0}.txt'.format(args.subreddit),'w') as results:
            results.write('Overall frequency target word= {0}\n\n********************'.format(str(sum(frequencies_per_time_bin))) + '\n')
            for time_bin in sorted(results_lists):
                results.write('\n')
                for element in time_bin:
                    results.write(str(element) + '\n')
        with open('../results/{0}/all_words_average_{0}.txt'.format(args.subreddit),'w') as awa:
            for item in dic_all_words_average:
                awa.write('{0} {1}\n'.format(str(item[0]), item[1]))
        with open('../results/{0}/all_words_max_{0}.txt'.format(args.subreddit),'w') as awm:
            for item in dic_all_words_max:
                awm.write('{0} {1}\n'.format(str(item[0]), item[1]))
        with open('../results/{0}/all_words_median_{0}.txt'.format(args.subreddit),'w') as awme:
            for item in dic_all_words_median:
                awme.write('{0} {1}\n'.format(str(item[0]), item[1]))
        with open('../results/{0}/very_first_values_{0}.txt'.format(args.subreddit), 'w') as results:
            for item in dic_very_first_values:
                try:
                    results.write('{0}: {1}\n'.format(str(item[0]), str(item[1][0])))
                except IndexError:
                    print('error!', item)
    else:
        with open('../results/{0}/results_{0}_centrality_{1}.txt'.format(args.subreddit, args.centrality),'w') as results:
            results.write('Overall frequency target word= {0}\n\n********************'.format(str(sum(frequencies_per_time_bin))) + '\n')
            for time_bin in sorted(results_lists):
                results.write('\n')
                for element in time_bin:
                    results.write(str(element) + '\n')
        with open('../results/{0}/all_words_average_{0}_centrality_{1}.txt'.format(args.subreddit, args.centrality), 'w') as awa:
            for item in dic_all_words_average:
                awa.write('{0} {1}\n'.format(str(item[0]), item[1]))
        with open('../results/{0}/all_words_max_{0}_centrality_{1}.txt'.format(args.subreddit, args.centrality), 'w') as awm:
            for item in dic_all_words_max:
                print(item)
                awm.write('{0} {1}\n'.format(str(item[0]), item[1]))
        with open('../results/{0}/all_words_median_{0}_centrality_{1}.txt'.format(args.subreddit, args.centrality), 'w') as awme:
            for item in dic_all_words_median:
                awme.write('{0} {1}\n'.format(str(item[0]), item[1]))
        with open('../results/{0}/very_first_values_{0}_centrality_{1}.txt'.format(args.subreddit, args.centrality), 'w') as results:
            for item in dic_very_first_values:
                try:
                    results.write('{0}: {1}\n'.format(str(item[0]), str(item[1][0])))
                except IndexError:
                    print('error!', item)

''' RUN THE CODE '''

if __name__ == "__main__":
    args = Parse_args()
    Main(args, DefineTimestamps(args.time_span, open('{0}/{1}_complete.txt'.format(args.data_path,args.subreddit)).readlines()))
















