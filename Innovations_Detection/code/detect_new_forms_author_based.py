import re
import collections
import operator
import numpy as np
import argparse
from scipy import stats
import os
import pandas as pd

from utils.define_time_bins import DefineTimestamps


''' GET ARGS '''

def Parse_args():

    parser = argparse.ArgumentParser()
    parser.add_argument('-data_path', type=str, help="Specify data path")
    parser.add_argument('-subreddit', type = str, help = "Specify subreddit name")
    parser.add_argument('-time_span', type = str, help = "[month|week]", default='month')
    parser.add_argument('-threshold', type=int, help="min number of occurrences (abs freq) for a word to be considered", default='10')
    parser.add_argument('-min_number_of_users', type=int, help="min number of users for a time bin to be considered", default='200')
    parser.add_argument('-max_len_acronyms', type=int, help="max len for a word to be considered", default='4')
    parser.add_argument('-neologisms', type=str, help="", default=True)
    parser.add_argument('-external_list_of_neologisms', type=str, help="", default=True)

    return parser.parse_args()

''' FUNCTIONS '''

''' clean each line of the input text '''
def CleanText(input_file):
    input_text = [line for line in input_file if "'author': None" not in line and '[' not in line and "'timestamp': '2017" not in line]
    input_text = [re.sub(r"'(subreddit|id|link_id|parent_id)': ('[^\s]+')", '', x) for x in input_text]
    input_text = [re.sub(r'(https?:\/\/[^\s]+|\\n)', '', x).lower() for x in input_text]
    print('Done cleaning')
    return input_text

''' create a vocabulary for the whole dataset '''
def CreateVoc(cleaned_list_of_texts):

    if args.external_list_of_neologisms == False:
        input_text = re.sub(r"('body': |"
                            r"'author': '(.*?)'|"
                            r"\w{'args.max_len_acronyms',50}"
                            r"|\d+|"
                            r")", '', ' '.join(cleaned_list_of_texts))
        count_overall_occurrences = collections.Counter(re.sub('[^\w]+', ' ', input_text).split())
        beg = re.findall(r' [\!|\'|\"|\(|\)|\,|\.|\:|\;\?](\w+)', input_text)
        end = re.findall(r'(\w+)[\!|\'|\"|\(|\)|\,|\.|\:|\;\?]', input_text)
        beg_end = beg + end
        beg_end = [x for x in beg_end if x.isalpha() and 1 < len(x) <= args.max_len_acronyms]
        count_occurrences_beg_end = collections.Counter(beg_end)
        acronyms_voc = [k for k,v in count_occurrences_beg_end.items() if v >= args.threshold]
        final_acronyms_voc = []
        for word in acronyms_voc:
            if count_occurrences_beg_end[word] / count_overall_occurrences[word] >= 0.5:
                final_acronyms_voc.append(word)
        print('Voc ready')
        return final_acronyms_voc

    else:
        print('Using external list of acronyms')

        input_text = re.sub(r"'(author|subreddit|id|link_id|parent_id)': ('[^\s]+'|None)", '', ' '.join(cleaned_list_of_texts))
        input_text = re.sub(r"'(body|title)': ", '', input_text)
        input_text = re.sub(r"'timestamp': '\d+-\d+-\d+ \d+\:\d+:\d+'", '', input_text)
        input_text = re.sub(r"[\!|\'|\"|\(|\)|\[|\]|\{|\}|\,|\.|\:|\;\?|\`|\\|\/]", ' ', input_text)

        print('input text ready')

        ''' count overall occurrences'''

        count_overall_occurrences = collections.Counter(re.sub('[^\w]+', ' ', input_text).split())

        print('count overall occurrences ready', len(count_overall_occurrences))

        filtered_count_overall_occurrences = dict()
        for k in count_overall_occurrences:
            if count_overall_occurrences[k] > args.threshold:
                filtered_count_overall_occurrences[k]=count_overall_occurrences[k]

        print('filtering done')

        list_acronyms = open('./utils/list_acronyms.txt').read().split('\n')

        final_acronyms_voc = []

        for acr in list_acronyms:
            if acr in filtered_count_overall_occurrences:
                final_acronyms_voc.append(acr)

        print('final list ready, len final list of acr', len(final_acronyms_voc))

        print('Voc ready')
        return final_acronyms_voc

''' check the number of authors that used each word in the vocabulary in every time bin '''
def CheckWordTrajectory(time_bins, voc):
    new_voc = dict()
    freq_voc = dict()
    with open('./utils/5000_most_freq_words') as common_words:
        common_words = common_words.read().split('\n')
        for word in voc:
            if word not in common_words:
                new_voc[word] = []
                freq_voc[word] = []

    list_of_time_bins = []
    number_of_time_bins = 0

    for bin in time_bins:
        timestamp = bin[0]
        data = bin[1]
        authors = [re.findall(r"'author': '(.*?)'", x)[0] for x in data]
        unique_authors = list(set(authors))
        if len(timestamp) > 0:
            if len(unique_authors) >= args.min_number_of_users:
                number_of_time_bins += 1
                print('\nTime bin {0}'.format(timestamp))
                print('number of unique authors: {0}'.format(len(unique_authors)))
                list_of_time_bins.append(timestamp)
                input_text = re.sub(r"'(author|subreddit|id|link_id|parent_id)': ('[^\s]+'|None)", '',' '.join(data))
                input_text = re.sub(r"'(body|title)': ", '', input_text)
                input_text = re.sub(r"'timestamp': '\d+-\d+-\d+ \d+\:\d+:\d+'", '', input_text)
                input_text = re.sub(r"[\!|\'|\"|\(|\)|\[|\]|\{|\}|\,|\.|\:|\;\?|\`|\\|\/]", ' ', input_text)

                d = collections.Counter(input_text.split())
                number_tokens_time_bin = sum([v for k, v in d.items() if v >= args.threshold])
                print('number_tokens_time_bin', number_tokens_time_bin)

                for k in freq_voc:
                    if k in d:
                        freq_voc[k].append(d[k])
                    else:
                        freq_voc[k].append(float(0))

                new_data = [list(set([x for x in re.sub('[^\w]+', ' ', txt).split()]).intersection(set(voc))) for txt in data]
                dic_words_authors = dict()
                for i, x in enumerate(new_data):
                    for k in x:
                        if k not in dic_words_authors:
                            dic_words_authors[k] = [authors[i]]
                        else:
                            if authors[i] not in dic_words_authors[k]:
                                dic_words_authors[k].append(authors[i])

                dic_words_faction_of_authors = {k: len(v)/len(unique_authors) for (k,v)  in dic_words_authors.items()}
                for k in new_voc:
                    new_voc[k].append(dic_words_faction_of_authors.get(k, 0))

    print('Words trajectories checked')

    print('number_of_time_bins', number_of_time_bins)

    if args.time_span == 'month':
        listofzeros = [0] * 3
        listofzeros2 = [0] * int(number_of_time_bins/4)

    if args.time_span == 'week':
        listofzeros = [0] * (6*4)
        listofzeros2 = listofzeros * 4

    neologisms_voc = dict()
    filtered_freq_voc = dict()

    for element in new_voc:
        if new_voc[element][0:len(listofzeros)] == listofzeros \
                and new_voc[element][0:len(listofzeros2)] != listofzeros2:
            neologisms_voc[element]=new_voc[element]
            filtered_freq_voc[element]=freq_voc[element]

    if args.neologisms == True:
        return neologisms_voc, list_of_time_bins, filtered_freq_voc
    else:
        return new_voc, list_of_time_bins, freq_voc

''' filter the results using common words in COCA '''
def FilterOutCommonWords(list_of_results):
    print('Filtering with COCA')
    final_list = []
    common_words = open('./utils/5000_most_freq_words').read().split('\n')
    for item in list_of_results:
        if item[0] not in common_words:
            final_list.append(item)
    return final_list

''' Final Measure '''
def Final_Measure(list_of_trajectories):

    print('\nCompute relevant measures')
    traj_dic = dict()
    all_measures_dic = dict()
    for term in list_of_trajectories:

        trimmed_trajectory = np.trim_zeros(list_of_trajectories[term], 'f')
        bin_trajectory = range(0,len(trimmed_trajectory))
        if len(trimmed_trajectory) == len(bin_trajectory) and len(trimmed_trajectory) > 1:
            spearman_value, p_value = stats.spearmanr(trimmed_trajectory, bin_trajectory)
            change = abs(np.mean(trimmed_trajectory[-6:]) - np.mean(trimmed_trajectory[:6]))
            not_abs_change = np.mean(trimmed_trajectory[-6:]) - np.mean(trimmed_trajectory[:6])
            slope = (np.mean(trimmed_trajectory[-6:]) - np.mean(trimmed_trajectory[:6])) / (bin_trajectory[-1] - bin_trajectory[0])
            spearman_by_change = float(spearman_value * change)
            readable_frequencies = [float(x)for x in list_of_trajectories[term]]
            traj_dic[term] = (readable_frequencies)
            all_measures_dic[term] = [spearman_value, p_value, not_abs_change, slope, spearman_by_change]
        else:
            print('error!', term, 'length of the trimmed trajectory=', len(trimmed_trajectory))

    sorted_persistent_dic = sorted(traj_dic.items(), key=operator.itemgetter(1), reverse=True)
    final_list = FilterOutCommonWords(sorted_persistent_dic)
    all_measures_dic = pd.DataFrame.from_dict(all_measures_dic, orient='index')
    all_measures_dic.columns = ['spearman', 'p_value', 'change', 'slope', 'spearman*abs-change']

    return final_list, all_measures_dic

''' Main '''
def main():
    cleaned_list_of_texts = CleanText(open('{0}/{1}_complete.txt'.format(args.data_path, args.subreddit)).readlines())
    vocabulary = CreateVoc(cleaned_list_of_texts)
    list_of_trajectories, list_time_bins, list_of_frequencies = CheckWordTrajectory(
        DefineTimestamps(args.time_span, cleaned_list_of_texts), vocabulary)
    final_spread, all_measures_dic = Final_Measure(list_of_trajectories)
    reordered_list_of_frequencies = []
    for item in final_spread:
        for k in list_of_frequencies:
            if item[0] == k:
                reordered_list_of_frequencies.append((k, list_of_frequencies[k]))
    return final_spread, reordered_list_of_frequencies, all_measures_dic


''' RUN THE CODE '''

if __name__ == "__main__":
    args = Parse_args()

    final_spread, list_of_frequencies, all_measures_dic = main()

    if not os.path.exists('../results/{0}/'.format(args.subreddit)):
        os.makedirs('../results/{0}/'.format(args.subreddit))

    with open('../results/{0}/{0}_all_forms_simple_spread.txt'.format(args.subreddit), 'w') as res_ss:
        for value in final_spread:
            res_ss.write('{0} {1}\n'.format(value[0], value[1]))

    if not os.path.exists('../frequencies/{0}/'.format(args.subreddit)):
        os.makedirs('../frequencies/{0}/'.format(args.subreddit))

    with open('../frequencies/{0}/{0}_all_forms_frequencies_abs.txt'.format(args.subreddit), 'w') as res_ss:
        for t in list_of_frequencies:
            res_ss.write('{0}, {1}\n'.format(t[0], t[1]))

    all_measures_dic.to_csv('../results/{0}/{0}_relevants_measures.csv'.format(args.subreddit), sep=',')

    print('Finito!')




