python code to detect spreading acronyms in corpora.

usage example:

python3 detect_new_forms_author_based.py -data /Users/marcodeltredici/workspace/DATA/data_exp_2/beer/beer_complete.txt -subreddit beer -external_list_of_neologisms True

new form without data path

python3 detect_new_forms_author_based.py -subreddit beer -external_list_of_neologisms True

for fake

python3 detect_new_forms_author_based.py -subreddit fake -threshold 0 -min_number_of_users 0 -neologisms no -external_list_of_neologisms True



external list of acronyms comes from here: https://www.noslang.com

