import os
import re
import sys
import random
random.seed(10)


def read_data(location: str) -> list:
    """Scans through the specified data folder and reads in all the data
    that is stored in the appropriate files.

    :param location: location of the folder
    :return: all combined data
    """
    final_data = []
    temp = []
    id_counter = 0
    id_regex = re.compile(r'[0-9]+')

    if 'VaccinationCorpus' in location:
        # shuffle the file order with a random number
        directory = sorted(os.scandir(location), key=lambda e: 0.49995030888562586)
    else:
        # keep the directory sorted
        directory = sorted(os.scandir(location), key=lambda e: e.name)

    for entry in directory:
        file_data = []
        if entry.name.endswith('.conll') or entry.name.endswith('features') or entry.name.endswith('.conll-3') and entry.is_file():
            with open(entry.path, encoding='utf8') as file:
                # Create a dictionary of all AR id's and give it a new unique value
                in_file = file.readlines()
                in_file.append('\n')
                for line in in_file:
                    if line == '\n':
                        file_data.append(temp)
                        temp = []
                    else:
                        temp.append(line.rstrip().split('\t'))
                id_dict, id_counter = create_id_dict(file_data, id_counter)

                # Convert AR id's to be unique over all files
                for line in in_file:
                    if line == '\n':
                        final_data.append(temp)
                        temp = []
                    else:
                        line = line.rstrip().split('\t')
                        if re.findall(id_regex, line[-1]):
                            for found_id in re.findall(id_regex, line[-1]):
                                repl_id = r'(?<![0-9])' + found_id + '(?![0-9])'
                                line[-1] = re.sub(repl_id, str(id_dict[found_id]), line[-1])
                        temp.append(line)

    # for i in final_data:
    #     for j in i:
    #         print(j)

    return final_data


def create_id_dict(file_data, id_counter):
    """Creates a dictionary to give each AR ID (key) a new unique value (value).

    :param: file_data: the data in one file
    :param: id_counter: a counter that increments over all files
    :return: a dictionary with unique ID for each AR ID
    """
    id_dict = {}
    id_regex = re.compile(r'[0-9]+')
    for sentence in file_data:
        for token in sentence:
            if re.findall(id_regex, token[-1]):
                for found_id in re.findall(id_regex, token[-1]):
                    if found_id not in id_dict:
                        id_dict[found_id] = id_counter
                        id_counter += 1
    return id_dict, id_counter


def extract_tokens_labels(all_data: list, argv: str) -> list:
    """Extracts all tokens and corresponding labels per token.

    :param all_data: data from all files
    :param argv: name of the dataset folder
    :return: sentences of tuples of a token and its label(s)
    """
    # Find the tokens: (?:[A-Za-z-[0-9])+
    # Find blanco tokens: (?:B-|I-)(?:CUE|CONTENT|SOURCE)
    token_re = re.compile(r'(?:B|I)-[A-Z]+-[0-9]+')
    tokens_labels = []
    for sentence in all_data:
        temp = []
        for token in sentence:
            if 'PARC3.0' in argv or 'POLNEAR' in argv:
                if '_' in token[-1]:
                    label = token[-1].replace('_', '').split()
                    temp.append((token[8], label))
                else:
                    temp.append((token[8], []))
            elif 'VaccinationCorpus' in argv:
                label = re.findall(token_re, token[-1])
                temp.append((token[3], label))
        tokens_labels.append(temp)
    return tokens_labels


def structure_data(tokens_labels: list, argv: str) -> list:
    """Structure the data so that a model can be trained on it. This means
    that each token can only have 1 label and tokens with no label are labeled
    as 'O'.

    :param tokens_labels: tokens and corresponding labels
    :param argv: name of the dataset folder
    :return: structured data
    """
    clean_data = []
    nested_regex = re.compile(r'[A-Za-z\-]+-NE-[0-9]+')
    label_regex = re.compile(r'(?:B-|I-)(?:CUE|CONTENT|SOURCE)')
    id_regex = re.compile(r'[0-9]+')

    if 'PARC3.0' in argv or 'POLNEAR' in argv:
        for sentence in tokens_labels:
            temp = []
            for label_tokens in sentence:
                tokens = label_tokens[1]
                filtered_token = [i for i in tokens if not nested_regex.match(i)]
                if filtered_token != []:
                    match = re.match(label_regex, filtered_token[0]) or 'O'
                    if match != 'O':
                        match = match[0] + '-' + str(id_regex.search(filtered_token[0])[0])
                    temp.append((label_tokens[0], match))
                else:
                    temp.append((label_tokens[0], 'O'))
            clean_data.append(temp)

    elif 'VaccinationCorpus' in argv:
        for sentence in tokens_labels:
            first_token = ''
            temp = []
            for i in sentence:
                if first_token == '':
                    if i[1] != []:
                        if len(first_token) > 1:
                            first_token = i[1][0]
                        else:
                            first_token = i[1]
                if i[1] != [] and i[1][0][-2:] == first_token[0][-2:]:
                    match = i[1][0]
                    if match is not None:
                        temp.append((i[0], match))
                    else:
                        temp.append((i[0], 'O'))
                else:
                    temp.append((i[0], 'O'))
            clean_data.append(temp)

    return clean_data


def remove_multi_ars(data):
    ar_id = re.compile(r'[0-9]+')
    label_regex = re.compile(r'(?:B-|I-)(?:CUE|CONTENT|SOURCE)')
    ar_sent_count = {}
    removed_data = []
    for sentence in data:
        found_ids = []
        for token_label in sentence:
            if token_label[1] != 'O':
                label_id = ar_id.search(token_label[1])[0]
                if label_id not in found_ids:
                    found_ids.append(label_id)
        for id in found_ids:
            if id not in ar_sent_count:
                ar_sent_count[id] = 1
            else:
                ar_sent_count[id] += 1

    for sentence in data:
        temp = []
        for token_label in sentence:
            if token_label[1] != 'O':
                clean_label = label_regex.search(token_label[1])[0]
                label_id = ar_id.search(token_label[1])[0]
                if ar_sent_count[label_id] > 3:
                    temp.append((token_label[0], 'O'))
                else:
                    temp.append((token_label[0], clean_label))
            else:
                temp.append((token_label[0], 'O'))
        removed_data.append(temp)

    # for i, sent in enumerate(data):
    #     print(data[i])
    #     print(removed_data[i])
    return removed_data


def main(argv: str) -> list:
    # parc loc: "../Data/PARC3.0/PARC_tab_format/dev"
    # polnear loc: "../Data/POLNEAR_enriched/dev"
    # vaccination loc: "../Data/VaccinationCorpus/testing"

    all_data = read_data(argv)
    tokens_labels = extract_tokens_labels(all_data, argv)
    clean_data = structure_data(tokens_labels, argv)
    removed_data = remove_multi_ars(clean_data)

    return removed_data



if __name__ == "__main__":
    main(sys.argv[1])
