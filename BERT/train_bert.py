from Data import read_data
from transformers import AutoTokenizer
from transformers import BertTokenizerFast, BertModel, DistilBertTokenizerFast, DistilBertModel
import numpy as np
import torch

from transformers import BertForTokenClassification, DistilBertForTokenClassification, Trainer, TrainingArguments


#tokenizer = AutoTokenizer.from_pretrained("bert-base-cased")
#model = BertModel.from_pretrained("bert-base-cased")

#tokenizer = BertTokenizerFast.from_pretrained('bert-base-cased')
#model = BertForTokenClassification.from_pretrained("bert-base-cased", num_labels=7)

tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-cased')
model = DistilBertForTokenClassification.from_pretrained("bert-base-cased", num_labels=7)


class ARdataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


def train_bert(train_dataset, dev_dataset):
    training_args = TrainingArguments(
        output_dir='../Results/BERT',  # output directory
        num_train_epochs=2,  # total number of training epochs
        per_device_train_batch_size=16,  # batch size per device during training
        per_device_eval_batch_size=64,  # batch size for evaluation
        warmup_steps=500,  # number of warmup steps for learning rate scheduler
        weight_decay=0.01,  # strength of weight decay
        logging_dir='./logs',  # directory for storing logs
        logging_steps=10,
    )

    trainer = Trainer(
        model=model,  # the instantiated Transformers model to be trained
        args=training_args,  # training arguments, defined above
        train_dataset=train_dataset,  # training dataset
        eval_dataset=dev_dataset  # evaluation dataset
    )
    trainer.train()
    return trainer


def encode_tags(tags, encodings):
    unique_tags = set(tag for doc in tags for tag in doc)
    tag2id = {tag: id for id, tag in enumerate(unique_tags)}
    id2tag = {id: tag for tag, id in tag2id.items()}

    print(unique_tags)
    print(tag2id)
    print(id2tag, '\n')

    labels = [[tag2id[tag] for tag in doc] for doc in tags]
    encoded_labels = []


    for doc_labels, doc_offset in zip(labels, encodings.offset_mapping):
        # create an empty array of -100
        doc_enc_labels = np.ones(len(doc_offset),dtype=int) * -100
        arr_offset = np.array(doc_offset)

        # set labels whose first offset position is 0 and the second is not 0
        doc_enc_labels[(arr_offset[:,0] == 0) & (arr_offset[:,1] != 0)] = doc_labels
        encoded_labels.append(doc_enc_labels.tolist())

    return encoded_labels, id2tag


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


def main():
    development = True
    if development:
        # len development = 1346
        #train = read_data.main('../Data/PARC3.0/PARC_tab_format/dev')[0:5]
        #test = read_data.main('../Data/PARC3.0/PARC_tab_format/dev')[5:10]
        #dev = read_data.main('../Data/PARC3.0/PARC_tab_format/dev')[10:15]

        #vaccorp = read_data.main("../Data/VaccinationCorpus")
        #train = vaccorp[:18775]
        #test = vaccorp[21121:]
        #dev = vaccorp[18775:21121]

        train = read_data.main('../Data/PARC3.0/PARC_tab_format/train')[0:100]
        dev = read_data.main('../Data/PARC3.0/PARC_tab_format/dev')[0:30]
        test = read_data.main('../Data/POLNEAR_enriched/test')[0:30]

    else:
        train = read_data.main('../Data/PARC3.0/PARC_tab_format/train')
        test = read_data.main('../Data/PARC3.0/PARC_tab_format/test')
        dev = read_data.main('../Data/PARC3.0/PARC_tab_format/dev')

    X_train = [sent2tokens(s) for s in train]
    y_train = [sent2labels(s) for s in train]

    X_dev = [sent2tokens(s) for s in dev]
    y_dev = [sent2labels(s) for s in dev]

    X_test = [sent2tokens(s) for s in test]
    y_test = [sent2labels(s) for s in test]

    train_encodings = tokenizer(X_train, is_split_into_words=True, return_offsets_mapping=True, padding=True, truncation=True)
    dev_encodings = tokenizer(X_dev, is_split_into_words=True, return_offsets_mapping=True, padding=True, truncation=True)
    test_encodings = tokenizer(X_test, is_split_into_words=True, return_offsets_mapping=True, padding=True, truncation=True)

    train_labels, train_tags = encode_tags(y_train, train_encodings)
    dev_labels, dev_tags = encode_tags(y_dev, dev_encodings)
    test_labels, test_tags = encode_tags(y_test, test_encodings)

    train_encodings.pop("offset_mapping")
    dev_encodings.pop("offset_mapping")
    test_encodings.pop("offset_mapping")
    train_dataset = ARdataset(train_encodings, train_labels)
    dev_dataset = ARdataset(dev_encodings, dev_labels)
    test_dataset = ARdataset(test_encodings, test_labels)

    model = train_bert(train_dataset, dev_dataset)
    X_pred, y_pred, _ = model.predict(test_dataset)
    predictions = np.argmax(X_pred, axis=2)

    label_list = []
    for key, value in test_tags.items():
        label_list.append(value)

    true_predictions = [
        [label_list[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, y_pred)
    ]

    true_labels = [
        [label_list[l] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, y_pred)
    ]

    with open('../BERT/output_bert.txt', 'w', encoding='utf8') as file:
        for i, sentence in enumerate(test):
            for j, token_label in enumerate(sentence):
                file.write(f"{token_label[0]}\t{true_predictions[i][j]}\n")
            if i < len(test)-1:
                file.write('\n')

    with open('../BERT/input_bert.txt', 'w', encoding='utf8') as file:
        for i, sentence in enumerate(test):
            for j, token_label in enumerate(sentence):
                file.write(f"{token_label[0]}\t{true_labels[i][j]}\n")
            if i < len(test)-1:
                file.write('\n')

if __name__ == "__main__":
    main()
