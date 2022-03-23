import os
import re
from collections import Counter


def read_data(location):
    final_data = []
    with os.scandir(location) as directory:
        for entry in directory:
            if entry.name.endswith('.conll-2') and entry.is_file():
                with open(entry.path, encoding='utf8') as file:
                    file_temp = []
                    sent_temp = []
                    in_file = file.readlines()
                    for line in in_file:
                        line = line.rstrip().split('\t')
                        if line != ['']:
                            token = line[3]
                            label = ' '.join(line[10:])
                            sent_temp.append((token, label))
                        else:
                            file_temp.append(sent_temp)
                            sent_temp = []
                    final_data.append(file_temp)
    return final_data


def count_ars(data):
    ar_id = re.compile(r'[0-9]+')
    ar_counter = 0
    for file in data:
        found_ids = []
        for sent in file:
            for token, label in sent:
                found_ars = re.findall(ar_id, label)
                for ar in found_ars:
                    if ar not in found_ids:
                        found_ids.append(ar)
        ar_counter += sum(Counter(found_ids).values())
    return ar_counter


def count_nested_ars(data):
    ar_id = re.compile(r'[0-9]+')
    ar_counter = 0
    for file in data:
        found_ids = []
        for sent in file:
            for token, label in sent:
                if '#' in label:
                    if label.count('#') == 1:
                        found_ars = re.findall(ar_id, label)[1]
                    elif label.count('#') == 2:
                        findall = re.findall(ar_id, label)
                        found_ars = findall[1] + findall[2]
                    for ar in found_ars:
                        if ar not in found_ids:
                            found_ids.append(ar)
        ar_counter += sum(Counter(found_ids).values())
    return ar_counter


def main():
    run_on_all_data = True
    if run_on_all_data:
        location = "../Data/VaccinationCorpus"
    else:
        location = "../Data/VaccinationCorpus/testing"
    data = read_data(location)

    run_all_functions = False
    if run_all_functions:
        print(count_ars(data))
        print(count_nested_ars(data))


if __name__ == "__main__":
    main()