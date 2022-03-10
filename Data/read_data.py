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

    clean_parc_dev_3 = []
    nested_regex = re.compile(r'[A-Za-z\-]+-NE-[0-9]+')
    label_regex = re.compile(r'(?:B-|I-)(?:CUE|CONTENT|SOURCE)')

    # Improved version
    for sentence in clean_parc_dev:
        temp = []
        for label_tokens in sentence:
            tokens = label_tokens[1]
            filtered_token = [i for i in tokens if not nested_regex.match(i)]
            if filtered_token != []:
                match = re.match(label_regex, filtered_token[0])
                temp.append((label_tokens[0], match[0]))
            else:
                temp.append((label_tokens[0], 'O'))
        clean_parc_dev_3.append(temp)


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
                #print(j[1][0])
                match = re.match(regex, j[1][0])
                if match is not None:
                    temp.append((j[0], match[0]))
                else:
                    temp.append((j[0], 'O'))
            else:
                temp.append((j[0], 'O'))
        clean_parc_dev_2.append(temp)

    return clean_parc_dev_3


def main(arg):
    parc_dev = read_data(arg)
    #print(parc_dev[0])
    clean_parc_dev = remove_placeholders(parc_dev)
    for i in clean_parc_dev:
        for j in i:
            print(j)
    #print(clean_parc_dev[0])
    return clean_parc_dev


if __name__ == "__main__":
    main()