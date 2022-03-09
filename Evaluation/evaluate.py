import os
import re


def determine_spans(data):
    spans = []
    # sentence index
    i = 0
    for sentence in data:
        span = []
        # begin and end index of the span
        first, second = 0, 0
        # token index
        j = 0
        for item in sentence:
            if item[0] == 'B' and span == []:
                span = [item]
                first = j
            elif item[0] == 'I':
                span.append(item)
            elif item == 'O' and span != []:
                second = j-1
                spans.append([i, [first, second], span])
                span = []
            elif item[0] == 'B' and span != []:
                second = j-1
                spans.append([i, [first, second], span])
                first = j
                span = [item]
            j += 1
        i += 1
    return spans


def determine_spans2(data):
    spans = []
    j = 0
    for sentence in data:
        i = 0
        span = []
        for item in sentence:
            if i != 0:
                prev_item = sentence[i-1]

            if span == []:
                span = [item]
                first = i
            elif i != 0 and item[-1] == prev_item[-1]:
                span.append(item)
            elif i != 0 and item[-1] != prev_item[-1]:
                second = i
                spans.append([j, [first, second], [re.sub('SOURCEX', 'SOURCE', token) for token in span]])
                first = i
                span = [item]
            i += 1
        j += 1
    return spans

def evaluate_spans(gold_spans, predictions):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for span in gold_spans:
        sentence_index = span[0]
        span_index = span[1]
        gold_span = span[2]
        pred_span = predictions[sentence_index][span_index[0]:span_index[1]]
        if gold_span == pred_span and gold_span.count('O') != len(gold_span):
            tp += 1
        elif gold_span.count('O') == len(gold_span) and pred_span.count('O') == len(pred_span):
            tn += 1
        elif pred_span.count('O') == len(pred_span) and gold_span.count('O') != len(gold_span):
            fn += 1
        elif gold_span != pred_span:
            fp += 1

    print(f'Total spans in gold: {len(gold_spans)}')
    print(f'TP: {tp}, TN: {tn}, FP: {fp}, FN: {fn}')
    print(f'Precision: {tp / (tp + fp)}')
    print(f'Recall: {tp / (tp + fn)}')
    print(f'F1: {(2*tp) / ((2*tp) + fp + fn)}')


def main():
    os.chdir('..')
    #with open('CRF/output_crf.txt', 'r') as file:
        #predictions = file.readlines()

    with open('CRF/input_crf.txt', 'r') as file:
        gold = []
        predictions = []
        for line in file:
            predictions.append(line.rstrip().split('\t'))
            line = re.sub('SOURCE', 'SOURCEX', line)
            line = line.rstrip() + '\t<eos>'
            gold.append(line.rstrip().split('\t'))

    gold_spans = determine_spans2(gold)
    evaluate_spans(gold_spans, predictions)

if __name__ == "__main__":
    main()