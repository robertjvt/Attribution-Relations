# An investigation on the portability of systems across Attribution Relation corpora

Robert van Timmeren, supervised by Tommaso Caselli

This repository contains the source code for my master thesis on Attribution Relations (ARs) at the University of Groningen.

## Dependencies
Make sure you have the following dependencies installed:
* Python ^3.9
* All libraries from requirements.txt

## Experiments
All experiments for this project are conducted with two types of models:
* BERT [(Devlin et al., 2019)](https://aclanthology.org/N19-1423/)
* CRF [(Lafferty et al., 2001)](https://repository.upenn.edu/cgi/viewcontent.cgi?article=1162&context=cis_papers)

And three corpora:
* PARC 3.0 [(Pareti, 2016)](https://aclanthology.org/L16-1619/)
* PolNeAR [(Newell et al., 2018)](https://aclanthology.org/L18-1524/)
* Vaccination Corpus [(Morante et al., 2020)](https://aclanthology.org/2020.lrec-1.611/)

## Running
### BERT
For replicating and fine-tuning one of our models run:
```
python BERT/train_bert.py
```
Please note to set the correct train, dev and test split.

### CRF
For replicating and training one of our baseline CRFs run:
```
python CRF/train_crf.py
```
Again, please note to set the correct train, dev and test split. For our CRF script you can simply use our define_data function.

### Evaluation
For running an evaluation on the predictions of one of the models run:
```
python evaluation/evaluate.py "../Results/BERT/output/file_name.txt" "../Results/BERT/input/file_name.txt"
```
Change the file_name.txt and folder depending on what you want to evaluate.

## File-Structure
    ├── BERT                          # Folder containing the scripts for fine-tuning BERT.
    │   ├── execute.sh                # Unix shell executable for fine-tuning on Peregrine.
    │   ├── input_bert.txt            # Temporary data file with the input test data.
    │   ├── output_bert.txt           # Temporary data file with the predictions on the test data.
    │   └── train_bert.py             # The script for fine-tuning BERT.
    │
    ├── CRF                           # Folder containing the scripts for training CRFs.
    │   ├── input_crf.txt             # Temporary data file with the input test data.
    │   ├── output_crf .txt           # Temporary data file with the predictions on the test data.
    │   └── train_crf.py              # The script for training the CRFs.
    │
    ├── Data                          # Folder containing the corpora (data) for conducting all experiments.
    │   ├── PARC3.0                   # Folder containg the PARC 3.0 data.
    │   ├── POLNEAR_enriched          # Folder containg the PolNeAR data.
    │   └── VaccinationCorpus         # Folder containg the Vaccination Corpus data.
    └── ...
   
## Acknowledgements
Special thanks to the Center for Information Technology of the University of Groningen for providing access to the Peregrine high performance computing cluster.



