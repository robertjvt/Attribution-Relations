import os
import re
from collections import Counter


def read_data(location: str) -> list:
    temp = []
    file_data = []
    with os.scandir(location) as directory:
        for entry in directory:
            if entry.name.endswith('.conll') or entry.name.endswith('features') or entry.name.endswith('.conll-3') and entry.is_file():
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


def count_sent_and_ars(data):
    id = re.compile(r'[0-9]+')
    sent_counter = 0
    ar_type_counter = {'CUE': 0, 'CUE+SOURCE': 0, 'CUE+SOURCE+CONTENT': 0, 'CUE+CONTENT': 0}
    for file in data:
        unique_ars = {}
        for sentence in file:
            sent_counter += 1
            for token in sentence:
                labels = token[-1].replace('_', '').split()
                if labels != []:
                    if '#' in labels[0] or ':' in labels[0]:
                        labels[0] = labels[0].replace(':', '#')
                        labels = labels[0].split('#')
                for label in labels:
                    ar_id = re.findall(id, label) or None
                    if ar_id != None:
                        ar_id = ar_id[0]

                    if ar_id not in unique_ars:
                        unique_ars[ar_id] = [0, 0, 0]

                    if 'CUE' in label.upper():
                        unique_ars[ar_id][0] += 1
                    elif 'SOURCE' in label.upper():
                        unique_ars[ar_id][1] += 1
                    elif 'CONTENT' in label.upper():
                        unique_ars[ar_id][2] += 1

        for key, value in unique_ars.items():
            if value[0] >= 1 and value[1] == 0 and value[2] == 0:
                ar_type_counter['CUE'] += 1
            elif value[0] >= 1 and value[1] >= 1 and value[2] == 0:
                ar_type_counter['CUE+SOURCE'] += 1
            elif value[0] >= 1 and value[1] >= 1 and value[2] >= 1:
                ar_type_counter['CUE+SOURCE+CONTENT'] += 1
            elif value[0] >= 1 and value[1] == 0 and value[2] >= 1:
                ar_type_counter['CUE+CONTENT'] += 1
    print('sent counter:', sent_counter)
    print(ar_type_counter)


def multi_sentence_ar(data):
    ar_id = re.compile(r'[0-9]+')
    total_multi_sent = {}
    total_sentence_lengths = {}

    for file in data:
        total_found = []
        total_lengths = []
        for sentence in file:
            found_labels = []
            found_lengths = []
            for token in sentence:
                for i in re.findall(ar_id, token[-1]):
                    if i not in found_labels:
                        found_labels.append(i)
                        found_lengths.append(len(sentence))
            total_found.append(found_labels)
            total_lengths.append(found_lengths)

        count_multi = {}
        count_lengths = {}
        for x, found_ids in enumerate(total_found):
            for i, id in enumerate(found_ids):
                if id not in count_multi:
                    count_multi[id] = 1
                    count_lengths[id] = [total_lengths[x][i]]
                else:
                    count_multi[id] += 1
                    count_lengths[id].append(total_lengths[x][i])

        for key, value in count_multi.items():
            if value not in total_sentence_lengths:
                total_sentence_lengths[value] = [sum(count_lengths.get(key)), 1]
            else:
                total_sentence_lengths[value][0] += sum(count_lengths.get(key))
                total_sentence_lengths[value][1] += 1

        for key, value in count_multi.items():
            if value not in total_multi_sent:
                total_multi_sent[value] = 1
            else:
                total_multi_sent[value] += 1

    final_total_sentence_lengths = {}
    for key, value in total_sentence_lengths.items():
        final_total_sentence_lengths[key] = round((value[0] / value[1], 3)

    return total_multi_sent, final_total_sentence_lengths


def main():
    all = True
    parc_dev = read_data('../Data/PARC3.0/PARC_tab_format/dev')
    polnear_dev = read_data('../Data/POLNEAR_enriched/dev')
    vaccorp_dev = read_data('../Data/VaccinationCorpus/testing')
    dev = parc_dev + polnear_dev + vaccorp_dev

    if all:
        parc_test = read_data('../Data/PARC3.0/PARC_tab_format/test')
        parc_train = read_data('../Data/PARC3.0/PARC_tab_format/train')
        parc = parc_dev + parc_test + parc_train

        polnear_test = read_data('../Data/POLNEAR_enriched/test')
        polnear_train = read_data('../Data/POLNEAR_enriched/train')
        polnear = polnear_dev + polnear_train + polnear_test

        vaccorp = read_data('../Data/VaccinationCorpus')

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
        #print(extract_pos_tags(parc))
        #print(extract_pos_tags(polnear))
        #print(extract_pos_tags(vaccorp))

        # AR types and sentence counter
        #count_sent_and_ars(parc)
        #count_sent_and_ars(polnear)
        #count_sent_and_ars(vaccorp)

        # Count ARs spanning over multiple sentences
        print(multi_sentence_ar(parc))
        print(multi_sentence_ar(polnear))
        print(multi_sentence_ar(vaccorp))


main()
