import os
import re
from collections import Counter


def restructure_all_data():
    """Restructures the dataset files to be of the same structure as PARC and PolNeAr"""
    data = []
    temp = []
    eventclaimreg = re.compile(r'(?:[A-Z]-event-[0-9]+|[A-Z]-claim-[0-9]+)')
    with os.scandir('VaccinationCorpus') as directory:
        for entry in directory:
            if entry.name.endswith('.annot') and entry.is_file():
                with open(entry.path, encoding='utf8') as file:
                    in_file = file.readlines()
                    fileloc = entry.path[:-6]
                    f = open(fileloc, 'w', encoding='utf8')

                    for line in in_file:
                        line = line.split('\t')
                        if line != ['\n']:
                            newline = '\t'.join(line[0:9])
                            tokens = line[9:]
                            #print(tokens)
                            new_tokens = []
                            for i in tokens:
                                if not eventclaimreg.match(i):
                                    new_tokens.append(i)
                                else:
                                    if i[-1] == '\n':
                                        new_tokens.append('\n')

                            tokenz = ' '.join(new_tokens)
                            f.write(fileloc[18:] + '\t' + newline + '\t' + tokenz.upper())
                        else:
                            f.write('\n')
                    f.close()

                    in_file.append('\n')
                    for line in in_file:
                        if line == '\n':
                            data.append(temp)
                            temp = []
                        else:
                            temp.append(line.rstrip().split('\t'))


def convert_unique_ids():
    """Converts all the unique id's to be the same for all unique AR's."""
    first_id = re.compile(r'[0-9]+')
    with os.scandir('VaccinationCorpus') as directory:
        for entry in directory:
            if entry.name.endswith('.conll') and entry.is_file():
                with open(entry.path, encoding='utf8') as file:
                    in_file = file.readlines()
                    temp = []
                    ids = []
                    # Find all id's
                    for line in in_file:
                        line = line.split('\t')
                        temp.append(line)
                        if ':' in line[-1]:
                            ids.append(re.findall(first_id, line[-1].split('#')[0]))
                            if len(line[-1].split('#')) > 1 and len(line[-1].split('#')[1]) > 1:

                                ids.append(re.findall(first_id, line[-1].split('#')[1]))

                    # Replace all found id's with unique AR id
                    for id_set in ids:
                        future_id = id_set[0]
                        rest = id_set[1:]
                        for id in rest:
                            for i, line in enumerate(temp):
                                temp[i][-1] = re.sub(id, future_id, temp[i][-1])

                    # Write new files
                    fileloc = entry.path[:-6] + '.conll-2'
                    f = open(fileloc, 'w', encoding='utf8')
                    for line in temp:
                        if line != ['\n']:
                            newline = '\t'.join(line)
                            f.write(newline)
                        else:
                            f.write('\n')
                    f.close()


def remove_nested_ars():
    """Removes nested ARs from the dataset and also ARs which span across the entire document."""
    id = re.compile(r'[0-9]+')
    with os.scandir('VaccinationCorpus') as directory:
        for entry in directory:
            if entry.name.endswith('.conll-2') and entry.is_file():
                with open(entry.path, encoding='utf8') as file:
                    all_ids = []
                    temp = []
                    in_file = file.readlines()
                    # Collect all unique AR id's
                    for line in in_file:
                        line = line.split('\t')
                        temp.append(line)
                        ids = re.findall(id, line[-1])
                        for found_id in ids:
                            all_ids.append(found_id)

                    # Count all unique id's and remove AR that spans across >80% of document
                    counter = Counter(all_ids).most_common(1)
                    if counter != [] and counter[0][1] / len(in_file) >= 0.8:
                        remove_id = counter[0][0]
                        remove_1st = re.compile('(?:B|I)-[A-Z]+-' + remove_id + ':?')
                        remove_2nd = re.compile(remove_id + '-[A-Z]+_?')
                        remove_3rd = re.compile('# ')
                        for i, line in enumerate(temp):
                            temp[i][-1] = re.sub(remove_1st, '', temp[i][-1])
                            temp[i][-1] = re.sub(remove_2nd, '', temp[i][-1])
                            temp[i][-1] = re.sub(remove_3rd, '', temp[i][-1])

                    # Write new data to file
                    fileloc = entry.path[:-8] + '.conll-3'
                    f = open(fileloc, 'w', encoding='utf8')
                    for line in temp:
                        if line != ['\n']:
                            newline = '\t'.join(line)
                            f.write(newline)
                        else:
                            f.write('\n')
                    f.close()


def main():
    #restructure_all_data()
    #convert_unique_ids()
    remove_nested_ars()


if __name__ == "__main__":
    main()