from Data import read_data

import time
import sklearn_crfsuite
import spacy

nlp = spacy.load("en_core_web_sm")


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
    }

    if i > 0:
        word1 = sent[i-1][0]
        features.update({
            '-1:word.lower()': word1.lower(),
            '-1:word.istitle()': word1.istitle(),
            '-1:word.isupper()': word1.isupper(),
        })
    else:
        features['BOS'] = True

    if i < len(sent)-1:
        word1 = sent[i+1][0]
        features.update({
            '+1:word.lower()': word1.lower(),
            '+1:word.istitle()': word1.istitle(),
            '+1:word.isupper()': word1.isupper(),
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
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )
    crf = crf.fit(X_train, y_train)
    print(f"Done fitting model. Time spent training:", round(time.time() - start_time, 2), "seconds.")
    return crf


def main():
    start_time = time.time()
    parc_train = read_data.main("../Data/PARC3.0/PARC_tab_format/train")
    parc_test = read_data.main("../Data/PARC3.0/PARC_tab_format/test")
    parc_dev = read_data.main('../Data/PARC3.0/PARC_tab_format/dev')

    all = False
    if all:
        X_train = [sent2features(s) for s in parc_train+parc_dev]
        y_train = [sent2labels(s) for s in parc_train+parc_dev]
        X_test = [sent2features(s) for s in parc_test]
        y_test = [sent2labels(s) for s in parc_test]
    else:
        X_train = [sent2features(s) for s in parc_dev[:100]]
        y_train = [sent2labels(s) for s in parc_dev[:100]]
        X_test = [sent2features(s) for s in parc_test[100:200]]
        y_test = [sent2labels(s) for s in parc_test[100:200]]

    crf = train_crf(X_train, y_train)
    y_pred = crf.predict(X_test)

    with open('../CRF/output_crf.txt', 'w') as file:
        for sentence in y_pred:
            file.write('\t'.join(sentence) + '\n')
    with open('../CRF/input_crf.txt', 'w') as file:
        for sentence in y_test:
            file.write('\t'.join(sentence) + '\n')
    with open('../CRF/train_input_crf.txt', 'w') as file:
        for sentence in parc_train:
            for token, label in sentence:
                file.write(token + '\t' + label + '\n')
            file.write('\n')

    print(f"Done entirely. Total time spent:", round(time.time() - start_time, 2), "seconds.")

if __name__ == "__main__":
    main()
