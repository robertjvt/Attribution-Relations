import os
import re
import sys


def read_data(location: str) -> list:
    """Scans through the specified data folder and reads in all the data
    that is stored in the appropriate files.

    :param location: location of the folder
    :return: all combined data
    """
    data = []
    temp = []
    with os.scandir(location) as directory:
        for entry in directory:
            if entry.name.endswith('.conll') or entry.name.endswith('features') or entry.name.endswith('.conll-3') and entry.is_file():
                with open(entry.path, encoding='utf8') as file:
                    in_file = file.readlines()
                    in_file.append('\n')
                    for line in in_file:
                        if line == '\n':
                            data.append(temp)
                            temp = []
                        else:
                            temp.append(line.rstrip().split('\t'))
    return data


def extract_tokens_labels(all_data: list, argv: str) -> list:
    """Extracts all tokens and corresponding labels per token.

    :param all_data: data from all files
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

    if 'PARC3.0' in argv or 'POLNEAR' in argv:
        for sentence in tokens_labels:
            temp = []
            for label_tokens in sentence:
                tokens = label_tokens[1]
                filtered_token = [i for i in tokens if not nested_regex.match(i)]
                if filtered_token != []:
                    match = re.match(label_regex, filtered_token[0]) or 'O'
                    temp.append((label_tokens[0], match[0]))
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
                    match = re.match(label_regex, i[1][0])
                    if match is not None:
                        temp.append((i[0], match[0]))
                    else:
                        temp.append((i[0], 'O'))
                else:
                    temp.append((i[0], 'O'))
            clean_data.append(temp)

    return clean_data


def main(argv: str) -> list:
    # parc loc: "../Data/PARC3.0/PARC_tab_format/dev"
    # polnear loc: "../Data/POLNEAR_enriched/dev"
    # vaccination loc: "../Data/VaccinationCorpus/testing"

    all_data = read_data(argv)
    tokens_labels = extract_tokens_labels(all_data, argv)
    clean_data = structure_data(tokens_labels, argv)
    return clean_data



if __name__ == "__main__":
    main(sys.argv[1])
