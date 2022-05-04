import re
import sys
from sklearn import metrics
import spacy
import time

# File of where to save the results to (define model used, datasets that were used to train on
# and the dataset that was evaluated on.
# crf
#file_name = "../Results/CRF/crf_parc_parc.txt"
# bert
file_name = "../Results/BERT/distilbert_parc+polnear_polnear2.txt"

nlp = spacy.load("en_core_web_sm")


# loc output and input:
# "../CRF/output_crf.txt" "../CRF/input_crf.txt"
# "../BERT/output_bert.txt" "../BERT/input_bert.txt"


def preprocess_cue(data):
    temp_total = []
    input_sentences = []
    verb_list = ['VBD', 'VBN', 'VBG', 'VBP', 'VBZ']
    with open(data, 'r', encoding='utf8') as file:
        for token_label in file:
            if token_label == '\n':
                temp_tokens = [token_label2[0] for token_label2 in temp_total]
                doc = nlp(' '.join(temp_tokens))
                for i, token in enumerate(temp_tokens):
                    temp_total[i].append(doc[i].tag_)
                input_sentences.append(temp_total)
                temp_total = []
            else:
                temp_total.append(token_label.rstrip().split('\t'))

    for i, sentence in enumerate(input_sentences):
        for j, token_label_pos in enumerate(sentence):
            if token_label_pos[1] == 'B-CUE' or token_label_pos[1] == 'I-CUE':
                if token_label_pos[2] in verb_list:
                    input_sentences[i][j][1] = 'CUE'
                else:
                    input_sentences[i][j][1] = 'O'

    return input_sentences


def read_data(input: str, output: str):
    predictions = []
    for sentence in input:
        temp = []
        for token_label_pos in sentence:
            temp.append(token_label_pos[1])
        predictions.append(temp)

    gold = []
    for sentence in output:
        temp = []
        for token_label_pos in sentence:
            temp.append(token_label_pos[1])
        gold.append(temp)

    return predictions, gold


def determine_spans(data: list) -> list:
    """Retrieves spans in the data, which are consecutive tokens.

    :param data: list of tokens of sentences
    :return: list of spans in the data with index features
    """
    spans = []
    sentence_index = 0
    for sentence in data:
        i = 0
        span = []
        for item in sentence:
            if i != 0:
                prev_item = sentence[i-1]

            if span == []:
                span = [item]
                start_index = i
            elif i != 0 and item[-1] == prev_item[-1]:
                span.append(item)
            elif i != 0 and item[-1] != prev_item[-1]:
                end_index = i
                spans.append([sentence_index, [start_index, end_index], [re.sub('SOURCEX', 'SOURCE', token) for token in span]])
                start_index = i
                span = [item]
            i += 1
        sentence_index += 1
    return spans


def strict_match(gold_spans: list, predictions: list):
    """Evaluates the predictions to the gold spans using a strict match on
    the spans.

    :param gold_spans: the spans retrieved from the gold data
    :param predictions: the predictions that are retrieved from a model
    """
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    test = []
    for span in gold_spans:
        sent_index = span[0]
        begin_span = span[1][0]
        end_span = span[1][1]

        gold_span = span[2]
        pred_span = predictions[sent_index][begin_span:end_span]
        if gold_span == pred_span and gold_span.count('O') != len(gold_span):
            tp += 1
        elif gold_span.count('O') == len(gold_span) and pred_span.count('O') == len(pred_span):
            tn += 1
        elif pred_span.count('O') == len(pred_span) and gold_span.count('O') != len(gold_span):
            fn += 1
        elif gold_span != pred_span:
            test.append((gold_span, pred_span))
            fp += 1

    print(f'Span-based exact match evaluation\n'
          f'Total spans: {len(gold_spans)}\n'
          f'TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}\n'
          f'Precision: {tp / (tp + fp)}\n'
          f'Recall: {tp / (tp + fn)}\n'
          f'F1: {(2*tp) / ((2*tp) + fp + fn)}\n',
          file=open(file_name, 'w'))


def overlap_match(gold_spans: list, predictions: list):
    """Evaluates the prediction spans on the gold spans using a softer
    match. Instead gives points based on the amount of overlap in a span.

    :param gold_spans: the spans retrieved from the gold data
    :param predictions: the predictions that are retrieved from a model
    """
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for span in gold_spans:
        sent_index = span[0]
        begin_span = span[1][0]
        end_span = span[1][1]

        gold_span = span[2]
        pred_span = predictions[sent_index][begin_span:end_span]

        correct = 0
        incorrect = 0
        correct_neg = 0
        incorrect_neg = 0

        for i in range(len(gold_span)):
            if pred_span[i] == gold_span[i]:
                if pred_span[i] == 'O' and gold_span[i] == 'O':
                    correct_neg += 1
                else:
                    correct += 1
            else:
                if pred_span[i] != 'O' and gold_span[i] == 'O':
                    incorrect_neg += 1
                elif pred_span[i] != 'O' and gold_span[i] != 'O':
                    incorrect_neg += 1
                elif pred_span[i] == 'O' and gold_span[i] != 'O':
                    incorrect += 1

        tp += correct / len(gold_span)
        fp += incorrect_neg / len(gold_span)
        tn += correct_neg / len(gold_span)
        fn += incorrect / len(gold_span)

    print(f'Span-based soft overlap evaluation\n'
          f'Total spans: {len(gold_spans)}\n'
          f'TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}\n'
          f'Precision: {tp / (tp + fp)}\n'
          f'Recall: {tp / (tp + fn)}\n'
          f'F1: {(2*tp) / ((2*tp) + fp + fn)}\n',
          file=open(file_name, 'a'))


def token_match(gold: list, predictions: list):
    """Shows a classification report for exact match on AR labels.

    :param gold: list of sentences with list of gold labels
    :param predictions: list of sentences with list of predicted labels
    """
    labels = ['B-CONTENT', 'I-CONTENT', 'B-SOURCE', 'I-SOURCE', 'CUE']
    gold = [re.sub('SOURCEX', 'SOURCE', word) for sent in gold for word in sent if word != '<eos>']
    predictions = [re.sub('SOURCEX', 'SOURCE', word) for sent in predictions for word in sent if word != '<eos>']

    sorted_labels = sorted(labels, key=lambda name: (name[1:], name[0]))
    print(metrics.classification_report(gold, predictions, labels=sorted_labels),
          file=open(file_name, 'a'))


def main(loc_output, loc_input):
    start_time = time.time()

    cue_pred, cue_gold = preprocess_cue(loc_output), preprocess_cue(loc_input)
    predictions, gold = read_data(cue_pred, cue_gold)
    gold_spans = determine_spans(gold)
    strict_match(gold_spans, predictions)
    overlap_match(gold_spans, predictions)
    token_match(gold, predictions)

    print(f"Done evaluating. Total time spent:", round(time.time() - start_time, 2), "seconds.")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
