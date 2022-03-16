import os
import re
import string

from collections import Counter

def read_data(location: str) -> list:
    data = []
    temp = []
    with os.scandir(location) as directory:
        for entry in directory:
            if entry.name.endswith('.conll') or entry.name.endswith('features') and entry.is_file():
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


def count_ars(location):
    ar_id = re.compile(r'[0-9]+')
    nested_ar_reg = re.compile(r'NE-[0-9]+')
    # total_ars counts the unique id's in each file
    total_ars = 0
    nested_ars = 0
    # Print total_articles to view amount of articles per location
    total_articles = 0
    with os.scandir(location) as directory:
        for entry in directory:
            if entry.name.endswith('.conll') or entry.name.endswith('features') and entry.is_file():
                data = []
                temp = []
                total_articles += 1
                with open(entry.path, encoding='utf8') as file:
                    in_file = file.readlines()
                    in_file.append('\n')
                    for line in in_file:
                        if line == '\n':
                            data.append(temp)
                            temp = []
                        else:
                            temp.append(line.rstrip().split('\t'))

                ar_id_counts = []
                nested_ar_id_counts = []
                for sentence in data:
                    for token in sentence:
                        found = re.findall(ar_id, token[-1])
                        found_ne = re.findall(nested_ar_reg, token[-1])
                        specific_ids = []
                        if found_ne != []:
                            for nested in found_ne:
                                for i in re.findall(ar_id, nested):
                                    specific_ids.append(i)
                        for id in found:
                            ar_id_counts.append(id)
                        for nested_id in specific_ids:
                            nested_ar_id_counts.append(nested_id)

                for key in Counter(ar_id_counts):
                    total_ars += 1

                for key in Counter(nested_ar_id_counts):
                    nested_ars += 1
    #print(nested_ars)
    return total_ars


def count_total_words_tokens(data, dataset):
    token_count = 0
    punct_count = 0
    word_count = 0
    exclude = set(string.punctuation)
    for line in data:
        for token in line:
            if dataset == 'parc' or dataset == 'polnear':
                tokenz = token[8]
            elif dataset == 'vaccorp':
                tokenz = token[3]

            if tokenz not in exclude:
                word_count += 1
            else:
                punct_count += 1
            token_count += 1

    return token_count, word_count, punct_count


def count_ars2(location: str) -> list:
    data = []
    temp = []
    with os.scandir(location) as directory:
        for entry in directory:
            if entry.name.endswith('.conll') or entry.name.endswith('features') and entry.is_file():
                file_data = []
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



def main():
    parc_dev = read_data('PARC3.0/PARC_tab_format/dev')
    parc_test = read_data('PARC3.0/PARC_tab_format/test')
    parc_train = read_data('PARC3.0/PARC_tab_format/train')
    parc = parc_dev + parc_test + parc_train
    print(parc_dev[0])

    polnear_dev = read_data('POLNEAR_enriched/dev')
    polnear_test = read_data('POLNEAR_enriched/test')
    #polnear_train = read_data('POLNEAR_enriched/train')
    #polnear = polnear_dev + polnear_test + polnear_train
    print(polnear_dev[0])

    vaccorp_dev = read_data('VaccinationCorpus/testing')
    vaccorp = read_data('VaccinationCorpus')
    print(vaccorp[0])

    # Count total ARs in each dataset
    print("Total ARs in PARC3.0:")
    print(count_ars('PARC3.0/PARC_tab_format/dev') + count_ars('PARC3.0/PARC_tab_format/test') + count_ars('PARC3.0/PARC_tab_format/train'))
    print("Total ARs in POLNEAR:")
    #print(count_ars('POLNEAR_enriched/dev') + count_ars('POLNEAR_enriched/test') + count_ars('POLNEAR_enriched/train'))
    print("Total ARs in VaccinationCorpus:")
    #print(count_ars('VaccinationCorpus'))


    # Count total amount of words in each dataset
    print("Total tokens, words and punct in PARC3.0:")
    print(count_total_words_tokens(parc, 'parc'))
    print("Total tokens, words and punct in POLNEAR:")
    print(count_total_words_tokens(polnear, 'polnear'))
    print("Total tokens, words and punct in VaccinationCorpus:")
    print(count_total_words_tokens(vaccorp, 'vaccorp'))



if __name__ == "__main__":
    main()
