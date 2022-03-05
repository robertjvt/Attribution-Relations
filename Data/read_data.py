import os
import re


def read_data(location):
    data = []
    temp = []
    with os.scandir(location) as directory:
        for entry in directory:
            if entry.name.endswith('.conll') and entry.is_file():
                #print(entry.path, entry.file)
                with open(entry.path) as file:
                    in_file = file.readlines()
                    in_file.append('\n')
                    for line in in_file:
                        if line == '\n':
                            data.append(temp)
                            temp = []
                        else:
                            temp.append(line.rstrip().split('\t'))
    return data


def remove_placeholders(parc_dev):
    # Find the tokens: (?:[A-Za-z-[0-9])+
    # Find blanco tokens: (?:B-|I-)(?:CUE|CONTENT|SOURCE)
    clean_parc_dev = []
    for sentence in parc_dev:
        temp = []
        for token in sentence:
            label = token[-1].replace('_', '').split()
            temp.append((token[8], label))
        clean_parc_dev.append(temp)

    clean_parc_dev_2 = []
    regex = re.compile(r'(?:B-|I-)(?:CUE|CONTENT|SOURCE)')
    for i in clean_parc_dev:
        first_token = ''
        temp = []
        for j in i:
            # set first found token
            if first_token == '':
                if j[1] != []:
                    if len(first_token) > 1:
                        first_token = j[1][0]
                    else:
                        first_token = j[1]
                        #print(first_token)
            # append only equals
            if j[1] != [] and j[1][0][-2:] == first_token[0][-2:]:
                match = re.match(regex, j[1][0])
                if match is not None:
                    temp.append((j[0], match[0]))
                else:
                    temp.append((j[0], ''))
            else:
                temp.append((j[0], ''))
        clean_parc_dev_2.append(temp)
    return clean_parc_dev_2


def main(arg):
    parc_dev = read_data(arg)
    clean_parc_dev = remove_placeholders(parc_dev)
    return clean_parc_dev


if __name__ == "__main__":
    main()