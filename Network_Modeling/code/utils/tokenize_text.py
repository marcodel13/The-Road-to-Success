import re

# file = open('/Users/marcodeltredici/workspace/PYCHARM/new_exp/experiment_2/network_modeling/data/fake-2009.txt').readlines()
# tws = ['the', 'a']

# for each line remove fields that are not title/body and return the tokenized text

# def ReturnTokenizedText(input_bin):
#
#     print('\nStart tokenization')
#
#     tok_text = []
#     authors = []
#
#     for line in input_bin:
#
#         if "'author': None" not in line:
#
#             author = ' '.join(re.findall(r"'author': '(.*?)'", line))
#             authors.append(author)
#
#             input_text = re.sub(r"\\", '', line)
#             input_text = re.sub(r"'\w+': ('\w+'|'\d+-\d+-\d+ \d+:\d+:\d+')", '', input_text)
#             input_text = input_text.lower()
#             # tokens = word_tokenize(input_text)
#
#             tok_text.append(input_text)
#
#     if len(tok_text) != len(authors):
#         print('PROBLEM WITH TOK AND AUTHOR LISTS: DIFFERENT LENGTH')
#
#     print('done')
#
#     return tok_text, authors


# file = open('/Users/marcodeltredici/workspace/PYCHARM/new_exp/experiment_2/network_modeling/data/fake-2009.txt').readlines()


# def ReturnTokenizedText_old_version(list_of_texts):
#
#     # print('\nStart tokenization')
#     tok_texts = []
#     authors = []
#
#     # print(input_text)
#     for item in list_of_texts:
#
#         if "'author': None" not in item:
#
#             author = ' '.join(re.findall(r"'author': '(.*?)'", item))
#             authors.append(author)
#
#             input_text = re.sub(r"\\", '', item)
#             input_text = re.sub(r"'\w+': ('\w+'|'\d+-\d+-\d+ \d+:\d+:\d+')", '', input_text)
#             input_text = input_text.lower()
#             input_text = re.sub(r"('body': |'title': )", '', input_text)
#             input_text = re.sub('[^A-Za-z0-9]+', ' ', input_text)
#             # print(input_text)
#             tok_sentence = input_text.split()
#             tok_texts.append(tok_sentence)
#
#     if len(tok_texts) != len(authors):
#         print('PROBLEM WITH TOK AND AUTHOR LISTS: DIFFERENT LENGTH')
#
#     # else:
#         # print('done')
#
#     return tok_texts, authors

# tt, au = ReturnTokenizedText_old_version(file)
# print(tt)
# print(au)


# print(input_text)

def ReturnTokenizedText(list_of_texts, tws):

    ''' remove lines you do not want to consider at all '''
    input_text = [line for line in list_of_texts if "'author': None" not in line and '[' not in line and "'timestamp': '2017" not in line]

    ''' extract the list of authors '''
    authors = [' '.join(re.findall(r"'author': '(.*?)'", item)) for item in input_text]

    ''' remove all the useless info'''
    # input_text = [re.sub(r"('id': |'body': |'title': |'timestamp': '\d+-\d+-\d+ \d+:\d+:\d+'|'author': '(.*?)'|\w{5,50}|\d+)", '', x).lower() for x in input_text]
    input_text = [re.sub(r"('id': |'body': |'title': |'timestamp': '\d+-\d+-\d+ \d+:\d+:\d+'|'author': '(.*?)'|\d+)", '',x).lower() for x in input_text]
    # input_text = [re.sub(r"('id': |'body': |'title': |'timestamp': '\d+-\d+-\d+ \d+:\d+:\d+'|'author': '(.*?)'|\d+)", '',x).lower() for x in input_text]

    ''' remove punctuation ans split '''
    input_text = [re.sub('[^\w]+', ' ', x).split() for x in input_text]

    # ''' keep only 1 < words <= 3'''
    # # input_text = [[x for x in sentence if 1 < len(x) <= 3] for sentence in input_text]

    ''' keep in the text only words that are in the list of '''
    input_text = [list(set(x).intersection(set(tws))) for x in input_text]

    # keep only the authors corresponding to posts/comments that (after filtering the text witht eh target words) are > 0
    # note: this code has to be run before modifying the input textitself (line below)
    authors = [x[1] for x in enumerate(authors) if len(input_text[x[0]]) > 0]

    # remove posts/comments that (after filtering the text witht eh target words) are > 0
    input_text = [x for x in input_text if len(x) > 0]

    return input_text, authors


# ReturnTokenizedText(file, tws)