import string

from Data import read_data

import time
import warnings
import sklearn_crfsuite
from sklearn.metrics import make_scorer
from sklearn_crfsuite import metrics
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
import spacy

nlp = spacy.load("en_core_web_sm")
warnings.simplefilter(action='ignore')


def word2features(sent, doc, i):
    """Retrieves features for each word and stores them in a dictionary for that word.

    :param sent:
    :param doc:
    :param i:
    :return:
    """
    word = sent[i][0]
    lemma = doc[i].lemma_
    pos_tag = doc[i].pos_
    tag = doc[i].tag_
    dep = doc[i].dep_
    shape = doc[i].shape_
    stop = doc[i].is_stop
    ne = doc[i].ent_type_
    verb_list = ["according", "accuse", "acknowledge", "add", "admit", "agree", "allege", "announce",
                 "argue", "assert", "believe", "blame", "charge", "cite", "claim", "complain",
                 "concede", "conclude", "confirm", "contend", "criticize", "declare", "decline", "deny",
                 "describe", "disagree", "disclose", "estimate", "explain", "fear", "hope", "insist",
                 "maintain", "mention", "note", "order", "predict", "promise", "recall", "recommend",
                 "reply", "report", "say", "state", "stress", "suggest", "tell", "testify", "think",
                 "urge", "warn", "worry", "write", "observe"]
    punctuation = string.punctuation

    features = {
        'bias': 1.0,
        'word.lower()': word.lower(),
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'word.isupper()': word.isupper(),
        'word.istitle()': word.istitle(),
        'word.isdigit()': word.isdigit(),
        'word.lemma': lemma,
        'word.postag': pos_tag,
        'word.tag': tag,
        'word.dep': dep,
        'word.shape': shape,
        'word.stop': stop,
        'word.inverblist': True if word.lower() in verb_list else False,
        'word.punct': True if word in punctuation else False,
        'word.ne': True if ne else False,
    }

    if i > 0:
        word1 = sent[i-1][0]
        lemma1 = doc[i-1].lemma_
        pos_tag1 = doc[i-1].pos_
        tag1 = doc[i-1].tag_
        dep1 = doc[i-1].dep_
        shape1 = doc[i-1].shape_
        stop1 = doc[i-1].is_stop
        ne1 = doc[i-1].ent_type_
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
            '-1:word.lemma': lemma1,
            '-1word.postag': pos_tag1,
            '-1word.tag': tag1,
            '-1word.dep': dep1,
            '-1word.shape': shape1,
            '-1word.stop': stop1,
            '-1word.inverblist': True if word1.lower() in verb_list else False,
            '-1word.punct': True if word1 in punctuation else False,
            '-1word.ne': True if ne1 else False,
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        lemma1 = doc[i+1].lemma_
        pos_tag1 = doc[i+1].pos_
        tag1 = doc[i+1].tag_
        dep1 = doc[i+1].dep_
        shape1 = doc[i+1].shape_
        stop1 = doc[i+1].is_stop
        ne1 = doc[i+1].ent_type_
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
            '+1:word.lemma': lemma1,
            '+1word.postag': pos_tag1,
            '+1word.tag': tag1,
            '+1word.dep': dep1,
            '+1word.shape': shape1,
            '+1word.stop': stop1,
            '+1word.inverblist': True if word1.lower() in verb_list else False,
            '+1word.punct': True if word1 in punctuation else False,
            '+1word.ne': True if ne1 else False,
        })
    else:
        features['EOS'] = True

    return features


def sent2features(sent):
    """Creates a Spacy NLP object for each sentence and stores the features
    of each word for each sentence in a list.

    :param sent:
    :return:
    """
    list_sentence = [word[0] for word in sent]
    sentence = ' '.join(list_sentence)
    doc = nlp(sentence)
    return [word2features(sent, doc, i) for i in range(len(sent))]


def sent2labels(sent):
    """Helper function to retrieve a list of labels from the sentences.

    :param sent:
    :return:
    """
    return [label for token, label in sent]


def sent2tokens(sent):
    """Helper function to retrieve a list of tokens from the sentences.

    :param sent:
    :return:
    """
    return [token for token, label in sent]


def train_crf(X_train, y_train):
    start_time = time.time()
    """Trains a Conditional Random Fields model on the train sentences with corresponding
    features.

    :param X_train:
    :param y_train:
    :return:
    """
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.01,
        max_iterations=100,
        all_possible_transitions=True
    )
    crf = crf.fit(X_train, y_train)
    print(f"Done fitting model. Time spent training:", round(time.time() - start_time, 2), "seconds.")
    return crf


def hyperparameter_optimization(X_train, y_train):
    """
    Perform hyperparameter optimization using a grid search and disabled cross validation.

    :param X_train:
    :param y_train:
    :return:
    """
    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        max_iterations=100,
        all_possible_transitions=True
    )

    params_space = {
        'c1': [0.1, 0.2, 0.5, 1],
        'c2': [0.01, 0.05, 0.1, 0.5],
    }

    labels = ['B-CONTENT', 'I-CONTENT', 'B-CUE', 'B-SOURCE', 'I-SOURCE', 'I-CUE']
    f1_scorer = make_scorer(metrics.flat_f1_score, average='weighted', labels=labels)

    gs = GridSearchCV(estimator = crf,
                      param_grid = params_space,
                      verbose = 0,
                      n_jobs = -1,
                      cv = [(slice(None), slice(None))],
                      scoring = f1_scorer)

    gs.fit(X_train, y_train)

    print('Best params: ', gs.best_params_)
    print('Best score:', gs.best_score_)
    print('Model size: ', gs.best_estimator_.size_)

    return gs.best_estimator_


def define_data(train, test):
    train_data = []

    for dataset in train:
        if dataset == 'PARC':
            train_data += read_data.main("../Data/PARC3.0/PARC_tab_format/train")
            train_data += read_data.main("../Data/PARC3.0/PARC_tab_format/dev")
        elif dataset == 'POLNEAR':
            train_data += read_data.main("../Data/POLNEAR_enriched/train")
            train_data += read_data.main("../Data/POLNEAR_enriched/dev")
        elif dataset == 'VACCORP':
            train_data += read_data.main("../Data/VaccinationCorpus")[:18773]

    if test == 'PARC':
        test_data = read_data.main("../Data/PARC3.0/PARC_tab_format/test")
    elif test == 'POLNEAR':
        test_data = read_data.main("../Data/POLNEAR_enriched/test")
    elif test == 'VACCORP':
        test_data = read_data.main("../Data/VaccinationCorpus")[18773:]

    return train_data, test_data



def main():
    start_time = time.time()
    development = False
    if development:
        parc_dev = read_data.main('../Data/PARC3.0/PARC_tab_format/dev')
        X_train = [sent2features(s) for s in parc_dev[:1076]]
        y_train = [sent2labels(s) for s in parc_dev[:1076]]
        X_test = [sent2features(s) for s in parc_dev[1076:]]
        y_test = [sent2labels(s) for s in parc_dev[1076:]]
    else:
        train, test = define_data(['VACCORP'], 'VACCORP')
        X_train = [sent2features(s) for s in train]
        y_train = [sent2labels(s) for s in train]
        X_test = [sent2features(s) for s in test]
        y_test = [sent2labels(s) for s in test]

        with open('../CRF/train_input_crf.txt', 'w', encoding='utf8') as file:
            for sentence in train:
                for token, label in sentence:
                    file.write(token + '\t' + label + '\n')
                file.write('\n')

    crf = train_crf(X_train, y_train)
    y_pred = crf.predict(X_test)

    #opt_crf = hyperparameter_optimization(X_train, y_train)
    #y_pred = opt_crf.predict(X_test)

    with open('../CRF/output_crf.txt', 'w', encoding='utf8') as file:
        for sentence in y_pred:
            file.write('\t'.join(sentence) + '\n')
    with open('../CRF/input_crf.txt', 'w', encoding='utf8') as file:
        for sentence in y_test:
            file.write('\t'.join(sentence) + '\n')

    print(f"Done entirely. Total time spent:", round(time.time() - start_time, 2), "seconds.")


if __name__ == "__main__":
    main()
