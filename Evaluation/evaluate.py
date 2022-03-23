import re
import sys

from sklearn import metrics

# File of where to save the results to (define model used, datasets that were used to train on
# and the dataset that was evaluated on.
file_name = "../Results/CRF/crf_parc_parc.txt"


def read_data(input: str, output: str):
    """Reads the .txt data in which the input that was used for the model and the
    output it produced.

    :param input: gold labels
    :param output: predicted labels
    :return: predicted labels, gold labels
    """
    with open(input, 'r') as file:
        predictions = []
        for line in file:
            predictions.append(line.rstrip().split('\t'))

    with open(output, 'r') as file:
        gold = []
        for line in file:
            line = re.sub('SOURCE', 'SOURCEX', line)
            line = line.rstrip() + '\t<eos>'
            gold.append(line.rstrip().split('\t'))

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
    labels = ['O', 'B-CONTENT', 'I-CONTENT', 'B-CUE', 'B-SOURCE', 'I-SOURCE', 'I-CUE']
    gold = [re.sub('SOURCEX', 'SOURCE', word) for sent in gold for word in sent if word != '<eos>']
    predictions = [re.sub('SOURCEX', 'SOURCE', word) for sent in predictions for word in sent if word != '<eos>']

    sorted_labels = sorted(labels, key=lambda name: (name[1:], name[0]))
    print(metrics.classification_report(gold, predictions, labels=sorted_labels),
          file=open(file_name, 'a'))


def main(loc_output, loc_input):
    # loc output and input: "../CRF/output_crf.txt" "../CRF/input_crf.txt"
    predictions, gold = read_data(loc_output, loc_input)
    gold_spans = determine_spans(gold)
    strict_match(gold_spans, predictions)
    overlap_match(gold_spans, predictions)
    token_match(gold, predictions)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
