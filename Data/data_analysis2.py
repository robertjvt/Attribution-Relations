import os
import re
from collections import Counter




def read_data(location: str) -> list:
    temp = []
    file_data = []
    with os.scandir(location) as directory:
        for entry in directory:
            if entry.name.endswith('.conll') or entry.name.endswith('features') and entry.is_file():
                with open(entry.path, encoding='utf8') as file:
                    data = []
                    in_file = file.readlines()
                    in_file.append('\n')
                    for line in in_file:
                        if line == '\n':
                            data.append(temp)
                            temp = []
                        else:
                            temp.append(line.rstrip().split('\t'))
                    file_data.append(data)
    return file_data

def extract_nested(data):
    ar_id = re.compile(r'[0-9]+')
    total_nested_ars = 0
    for file in data:
        nested_ar_ids = []
        for sentence in file:
            for token in sentence:
                labels = token[-1].replace('_', '').split()
                for label in labels:
                    if '-NE-' in label or '#' in label:
                        if re.findall(ar_id, label)[0] not in nested_ar_ids:
                            nested_ar_ids.append(re.findall(ar_id, label)[0])
        total_nested_ars += len(nested_ar_ids)
    return total_nested_ars


def extract_ar_types(data):
    total_counter = Counter()
    for file in data:
        total_tokens = []
        for sentence in file:
            for token in sentence:
                labels = token[-1].replace('_', '').split()
                if labels != []:
                    if '#' in labels[0] or ':' in labels[0]:
                        labels[0] = labels[0].replace(':', '#')
                        labels = labels[0].split('#')
                for label in labels:
                    if label[0] == 'B':
                        if label[0:4] == 'B-CO':
                            total_tokens.append(label[0:9])
                        elif label[0:4] == 'B-SO':
                            total_tokens.append(label[0:8])
                        elif label[0:4] == 'B-CU':
                            total_tokens.append(label[0:5])
        total_counter += Counter(total_tokens)
    return total_counter


def generate_label_top10(data):
    blanco_token = re.compile(r'(?:B-|I-)(?:CUE|CONTENT|SOURCE)')
    cues = []
    sources = []
    contents = []
    for file in data:
        for sentence in file:
            for token in sentence:
                labels = token[-1].replace('_', '').split()
                if labels != []:
                    if '#' in labels[0] or ':' in labels[0]:
                        labels[0] = labels[0].replace(':', '#')
                        labels = labels[0].split('#')

                if len(token) == 12 or len(token) == 20:
                    word = token[8]
                elif len(token) == 11:
                    word = token[3]

                for label in labels:
                    if '_' in token[-1]:
                        print(token)
                        print(label)
                        if len(re.findall(blanco_token, label)) != 0:
                            label = re.findall(blanco_token, label)[0]
                            if label == 'B-CUE' or label == 'I-CUE':
                                cues.append(word)
                            elif label == 'B-SOURCE' or label == 'I-SOURCE':
                                sources.append(word)
                            elif label == 'B-CONTENT' or label == 'I-CONTENT':
                                contents.append(word)
    return Counter(cues).most_common(15), Counter(sources).most_common(15), Counter(contents).most_common(15)


def extract_pos_tags(data):
    blanco_token = re.compile(r'(?:B-|I-)(?:CUE|CONTENT|SOURCE)')
    cues = []
    sources = []
    contents = []
    for file in data:
        for sentence in file:
            for token in sentence:
                labels = token[-1].replace('_', '').split()
                if labels != []:
                    if '#' in labels[0] or ':' in labels[0]:
                        labels[0] = labels[0].replace(':', '#')
                        labels = labels[0].split('#')

                if 'wsj_' in token[0]:
                    word = token[10]
                elif '.txt.xml' in token[0]:
                    word = token[10]
                elif len(token) == 11:
                    word = token[5]

                for label in labels:
                    if '_' in token[-1]:
                        if len(re.findall(blanco_token, label)) != 0:
                            label = re.findall(blanco_token, label)[0]
                            if label == 'B-CUE' or label == 'I-CUE':
                                cues.append(word)
                            elif label == 'B-SOURCE' or label == 'I-SOURCE':
                                sources.append(word)
                            elif label == 'B-CONTENT' or label == 'I-CONTENT':
                                contents.append(word)
    return Counter(cues).most_common(15), Counter(sources).most_common(15), Counter(contents).most_common(15)


def main():
    all = True
    parc_dev = read_data('PARC3.0/PARC_tab_format/dev')
    polnear_dev = read_data('POLNEAR_enriched/dev')
    vaccorp_dev = read_data('VaccinationCorpus/testing')

    if all:
        parc_test = read_data('PARC3.0/PARC_tab_format/test')
        parc_train = read_data('PARC3.0/PARC_tab_format/train')
        parc = parc_dev + parc_test + parc_train

        polnear_test = read_data('POLNEAR_enriched/test')
        polnear_train = read_data('POLNEAR_enriched/train')
        polnear = polnear_dev + polnear_train + polnear_test

        vaccorp = read_data('VaccinationCorpus')

        # Extract the amount of nested ARs
        #print(extract_nested(vaccorp))
        #print(extract_nested(parc))

        # Extract the amount of AR types for each type
        #print(extract_ar_types(parc))
        #print(extract_ar_types(polnear))
        #print(extract_ar_types(vaccorp))

        # Extract the top 10 words for each AR label
        #print(generate_label_top10(parc))
        #print(generate_label_top10(polnear))
        #print(generate_label_top10(vaccorp))

        # Extract POS tags per AR label
        print(extract_pos_tags(parc))
        print(extract_pos_tags(polnear))
        print(extract_pos_tags(vaccorp))

main()