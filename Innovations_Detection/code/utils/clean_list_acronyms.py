import re
input = open('list_acronyms_draft.txt').read().split('\n')

output = []

for item in input:
    # print(item)
    item = item.split(':')[0].strip()
    # print(item)
    item = re.sub(r'[\!|\'|\"|\(|\)|\,|\.|\:|\;|\?|\/]','', item).lower()
    if len(item.split(' ')) == 1:
        output.append(item)


# output = list(set(output))
filtered_output = []
for item in output:
    if item not in filtered_output:
        filtered_output.append(item)

with open('list_acronyms.txt', 'w') as res:
    for item in filtered_output:
        res.write(str(item) + '\n')
