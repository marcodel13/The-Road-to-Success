import re

''' Assing to each author a unique index.
    Returns the text in which names have been substituted and the list of the names.
    Note: the integers for each author corresponds to its integers in the list'''

def FromNamesToInt(file):

    names = []

    list = []

    for line in file:

        if "'author': None" not in line:

            author = (re.findall(r"'author': '(.*?)'",line))
            author = author[0]

            if author not in names:

                names.append(author)

                line = re.sub(author, str(names.index(author)), line)
                list.append(line)

            else:

                line = re.sub(author, str(names.index(author)), line)
                list.append(line)

    with open('names_int.txt', 'w') as names_int:
        for item in names:
            names_int.write('{0},{1}\n'.format(str(names.index(item)), item))

    return list, names