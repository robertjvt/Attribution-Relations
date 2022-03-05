from Data import read_data

import os

import sklearn
from sklearn.metrics import make_scorer

import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics


def word2features(sent, i):
    word = sent[i][0]

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
    }

    if i > 0:
        word1 = sent[i-1][0]
        postag1 = sent[i-1][1]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        postag1 = sent[i+1][1]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]


def sent2labels(sent):
    return [label for token, label in sent]


def sent2tokens(sent):
    return [token for token, postag, label in sent]


def train_crf(X_train, y_train):
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )
    return crf.fit(X_train, y_train)


def main():
    os.chdir('..')
    #parc_train = read_data.main('Data/PARC3.0/PARC_tab_format/train')
    #parc_test = read_data.main('Data/PARC3.0/PARC_tab_format/test')
    parc_dev = read_data.main('Data/PARC3.0/PARC_tab_format/dev')

    X_train = [sent2features(s) for s in parc_dev[:1076]]
    y_train = [sent2labels(s) for s in parc_dev[:1076]]

    X_test = [sent2features(s) for s in parc_dev[1076:]]
    y_test = [sent2labels(s) for s in parc_dev[1076:]]

    crf = train_crf(X_train, y_train)


if __name__ == "__main__":
    main()