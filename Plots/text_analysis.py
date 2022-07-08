from Data import read_data
from collections import Counter
import string
from pprint import pprint
from nltk.corpus import stopwords
import numpy as np
import matplotlib.pyplot as plt
import shifterator as sh


def main():
    stop_words = set(stopwords.words('english'))
    stop_words.add('’s')
    stop_words.add("n’t")
    stop_words.add("n't")
    stop_words.add("'s")
    stop_words.add("’m")
    stop_words.add("’ve")
    stop_words.add('\\"')
    stop_words.add('-lrb-')
    stop_words.add('-rrb-')
    stop_words.add('&amp;')
    #stop_words.add('co.')

    punctuation = string.punctuation + '“”’‘…—...--``' + "''"

    vaccorp_words = []
    vaccorp = read_data.read_data('../Data/VaccinationCorpus')
    parc_words = []
    parc = read_data.read_data('../Data/PARC3.0/PARC_tab_format/dev') + read_data.read_data('../Data/PARC3.0/PARC_tab_format/test') + read_data.read_data('../Data/PARC3.0/PARC_tab_format/train')
    polnear_words = []
    polnear = read_data.read_data('../Data/POLNEAR_enriched/test') + read_data.read_data('../Data/POLNEAR_enriched/dev') + read_data.read_data('../Data/POLNEAR_enriched/train')


    for file in vaccorp:
        for sentence in file:
            if sentence[4].lower() not in stop_words and sentence[4] not in punctuation and len(sentence[4]) != 1:
                vaccorp_words.append(sentence[4].lower())

    for file in parc:
        for sentence in file:
            if sentence[9].lower() not in stop_words and sentence[9] not in punctuation and len(sentence[9]) != 1:
                parc_words.append(sentence[9].lower())

    for file in polnear:
        for sentence in file:
            if sentence[9].lower() not in stop_words and sentence[9] not in punctuation and len(sentence[9]) != 1:
                polnear_words.append(sentence[9].lower())


    counter = Counter(vaccorp_words)
    counter2 = Counter(parc_words)
    counter3 = Counter(polnear_words)
    removed_counter = Counter()
    removed_counter2 = Counter()
    removed_counter3 = Counter()

    for key, value in counter.most_common():
        if value >= 1:
            removed_counter[key] = value
    for key, value in counter2.most_common():
        if value >= 1:
            removed_counter2[key] = value
    for key, value in counter3.most_common():
        if value >= 1:
            removed_counter3[key] = value
    pprint(removed_counter2)

    jsd_shift = sh.JSDivergenceShift(type2freq_1=removed_counter3,
                                     type2freq_2=removed_counter,
                                     weight_1=0.5,
                                     weight_2=0.5,
                                     base=2,
                                     alpha=1,
                                     )
    print(jsd_shift.diff)
    jsd_shift.get_shift_graph(top_n=50, system_names=['PolNeAR', 'Vaccination Corpus'])


def heatmap():
    y_axis = ['PARC3', ' PolNeAR', 'Vaccination Corpus']
    x_axis = ['PARC3', ' PolNeAR', 'Vaccination Corpus']
    values = np.array([[0, 0.28, 0.44],
                       [0.28, 0, 0.45],
                       [0.44, 0.45, 0]])

    fig, ax = plt.subplots()
    im = ax.imshow(values)

    ax.set_xticks(np.arange(len(x_axis)), labels=x_axis)
    ax.set_yticks(np.arange(len(y_axis)), labels=y_axis)
    ax.xaxis.tick_top()

    plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
             rotation_mode="anchor")

    for i in range(len(y_axis)):
        for j in range(len(x_axis)):
            text = ax.text(j, i, values[i, j],
                           ha="center", va="center", color="w")

    plt.colorbar(im)
    fig.tight_layout()
    plt.show()


main()
#heatmap()