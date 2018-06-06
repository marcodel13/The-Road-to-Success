import re
import datetime
import operator

''' Return a sorted list of tuples where the first element is the timestamp (either month or week) and the second is data '''


def DefineTimestamps(time_span, file):

    dictionary = dict()

    for line in file:

        year = ' '.join(re.findall(r"'timestamp': '(\d+)-\d+-\d+", line))
        month = ' '.join(re.findall(r"'timestamp': '\d+-(\d+)-\d+", line))
        day = ' '.join(re.findall(r"'timestamp': '\d+-\d+-(\d+) ", line))

        if year != '2017': # i want adta only to the end of 2016

            if time_span == 'month':

                time_bin = year + month

                if time_bin not in dictionary:
                    dictionary[time_bin]=[line]
                else:
                    dictionary[time_bin].append(line)

            else:

                date = datetime.date(int(year), int(month), int(day))

                weeknumber = date.strftime("%V")
                time_bin = year + weeknumber

                if time_bin not in dictionary:
                    dictionary[time_bin] = [line]
                else:
                    dictionary[time_bin].append(line)

    sorted_list = sorted(dictionary.items(), key=operator.itemgetter(0))

    return sorted_list
