import os
import re
from Data import read_data

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
    token_re = re.compile(r'(?:B|I)-[A-Z]+-[0-9]+')
    tokens_labels = []
    for sentence in all_data:
        temp = []
        for token in sentence:
            if 'VaccinationCorpus' in argv:
                label = re.findall(token_re, token[-1])
                temp.append((token[0], token[3], label))
        tokens_labels.append(temp)
    return tokens_labels


def structure_data(tokens_labels: list, argv: str) -> list:
    clean_data = []
    nested_regex = re.compile(r'[A-Za-z\-]+-NE-[0-9]+')
    label_regex = re.compile(r'(?:B-|I-)(?:CUE|CONTENT|SOURCE)')
    id_regex = re.compile(r'[0-9]+')

    if 'VaccinationCorpus' in argv:
        for sentence in tokens_labels:
            first_token = ''
            temp = []
            for i in sentence:
                if first_token == '':
                    if i[2] != []:
                        if len(first_token) > 1:
                            first_token = i[2][0]
                        else:
                            first_token = i[2]
                if i[2] != [] and i[2][0][-2:] == first_token[0][-2:]:
                    match = i[2][0]
                    if match is not None:
                        temp.append((i[0], i[1], match))
                    else:
                        temp.append((i[0], i[1], 'O'))
                else:
                    temp.append((i[0], i[1], 'O'))
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
            if token_label[2] != 'O':
                label_id = ar_id.search(token_label[2])[0]
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
            if token_label[2] != 'O':
                clean_label = label_regex.search(token_label[2])[0]
                label_id = ar_id.search(token_label[2])[0]
                if ar_sent_count[label_id] > 3:
                    temp.append((token_label[0], token_label[1], 'O'))
                else:
                    temp.append((token_label[0], token_label[1], clean_label))
            else:
                temp.append((token_label[0], token_label[1], 'O'))
        removed_data.append(temp)

    return removed_data


def main():
    wikipedia = ["en-wikipedia-org", ]

    news = ["21st-century-wire", "abc-news", "activist-post", "banning-beaumont", "bbc-news", "carrington", 'chicagotribune',
            'cnn_2017', 'daily-intelligencer', 'fox-news', 'global-news', 'health-impact-news', 'heavy-com', 'huffingtonpost',
            'infowars', 'kxan-com', 'latimes-com', 'lifesitenews', 'mirror', 'naturalnews', 'nbc-news', 'news-nationalgeographic',
            'newscomau', 'newstarget-com', 'ny-daily-news', 'nytimes-com', 'oredigger-net', 'pbs-newshour', 'politico',
            'reuters', 'science-news-for-students', 'science-news_', 'scientific-american', 'the-guardian', 'the-independent',
            'the-west-australian', 'thinkprogress', 'usnews-com', 'vaccine-impact', 'vaccines-news', 'variety', 'washington-post',
            'wired_', 'wonkette-com', 'yahoo-com',
            ]

    blogs = ["ars-technica", "backyard-secret-exposed", "blogs-cdc-gov", 'collective-evolution', 'couples-resorts',
             "dogsnaturallymagazine", 'drsuzanne', 'gizmodo', 'justthevax-blogspot', 'kelly-brogan-md', 'kid-nurse',
             'ldi-201', 'leesburg-vet-blog', 'modern-alternative-health', 'mom-me_201', 'nation19-com', 'natural-health-365',
             'netmums', 'pregnancy-forum-co-uk', 'reasonable-hank', 'respectful-insolence', 'self_201', 'sharylattkisson',
             'skeptical-raptor', 'the-cat-site', 'the-conversation', 'the-forum-at-harvard', "the-people's-chemist",
             'thehealthyhomeeconomist', 'tripadvisor-com', 'truth4dogs', 'upmc-&-pitt', 'vaccine-injury-info', 'vactruth-com',
             'vaccinestoday-eu', 'vernoncoleman-com', 'virology-ws', 'wordreference-forums',
             ]

    science = ["biology-stackexchange", 'cid-oxfordjournals', 'content-healthaffairs', 'globalresearch', 'greenmedinfo',
               'nap-edu', 'nature-com', 'nature-news-&-comment', 'science-2-0', 'science-_-', 'science-based-medicine',
               'vk-ovg-ox-ac-uk',
               ]

    health = ["berkeleywellness", "acsh-org", "aids-gov", "betterhealth-vic-gov", "california-healthline", 'cdc-gov',
              'emergency-cdc', 'fda-gov', 'euro-who-int', 'fitfortravel', 'ggd-amsterdam', 'health-gov-on', 'health-ny-gov',
              'healthycanadians', 'immunisation-advisory', 'immunise-health-gov', 'international-medical-council', 'mayo-clinic',
              'mbah-state-ms-us', 'medlineplus-gov', 'national-vaccine-information-center', 'ncbi-nlm-nih-gov', 'nhs-uk',
              'phac-aspc-gc-ca', 'rivm-nl', 'tmb-ie', 'travel-gc-ca', 'travel-ready-md', 'vaccines-gov', 'who-int_',
              'world-health-organization',
              ]

    org = ["age-of-autism", "atlas-monitor", "avn-org", "butterflybirth-com", 'child-health-safety', 'church-law', 'cidrap',
           'epilepsy', 'fiercepharma', 'fodors', 'global-freedom', 'healthtalk-org', 'healthychildren', 'hepatitis-b',
           'hepb-org', 'historyofvaccines', 'immunize-org', 'immunizeforgood', 'influenzareport', 'info-cmsri-org', 'jabs-org',
           'npr-org', 'parents', 'patient-info', 'petful', 'petmd-com', 'politifact', 'popsugar-moms', 'publichealth-org',
           'state-of-health', 'stop-mandatory-vaccination', 'the-evergreen-center', 'thinktwice', 'travel-ready-md', 'travelfish',
           'unicef-org', 'uptodate-com', 'vaccinateyourbaby', 'vaccineinformation-org', 'vaccinepapers-org', 'vaxtruth-org',
           'veazie-vet', 'voices-for-vaccines', 'webmd_', 'whattoexpect', 'world-economic-forum',
           ]

    os.chdir('..')
    with open("../Results/BERT/output/output_bert_vaccorp_vaccorp.txt", 'r', encoding='utf8') as file:
        output_data = []
        for line in file:
            line = line.rstrip().split('\t')
            output_data.append(line)
        output_data.append([''])


    vaccorp = read_data.read_data("../Data/VaccinationCorpus")[21121:]
    tokens_labels = extract_tokens_labels(vaccorp, 'VaccinationCorpus')
    clean_data = structure_data(tokens_labels, 'VaccinationCorpus')
    vaccorp_data = remove_multi_ars(clean_data)

    input_data = []
    for line in vaccorp_data:
        for tokens in line:
            input_data.append(tokens)
        input_data.append([input_data[-1][0], ''])


    gold_news = []
    pred_news = []
    for i, pred in enumerate(output_data):
        source = input_data[i][0]
        for item in science:
            if item in source.lower():
                pred_news.append(pred)
                if len(input_data[i]) != 2:
                    gold_news.append([input_data[i][1], input_data[i][2]])
                else:
                    gold_news.append([''])


    print(os.getcwd())
    with open('Error Analysis/gold.txt', 'w', encoding='utf8') as file:
        for token_label in gold_news:
            if len(token_label) != 1:
                file.write(f"{token_label[0]}\t{token_label[1]}\n")
            else:
                file.write('\n')

    with open('Error Analysis/pred.txt', 'w', encoding='utf8') as file:
        for token_label in pred_news:
            if len(token_label) != 1:
                file.write(f"{token_label[0]}\t{token_label[1]}\n")
            else:
                file.write('\n')


if __name__ == "__main__":
    main()