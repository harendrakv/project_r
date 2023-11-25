# -*- coding: utf-8 -*-
"""
Created on Sat Nov 25 14:42:10 2023

@author: harendra.verma
"""

import spacy
from text_extraction import DocumentProcessor
import os
import STRINGS
from utils import load_jsonl
import warnings
from pathlib import Path
from spacy.tokens import DocBin
import pandas as pd

# In[]
def prepare_ner_train_data(patterns):
    nlp1 = spacy.load("en_core_web_sm")

    nlp = spacy.blank("en")
    ruler = nlp.add_pipe("entity_ruler")
    ruler.add_patterns(patterns)
    
    files =  os.listdir(STRINGS.RESUME_FILES_PATH)
    
    TRAIN_DATA = []

    for i in range(len(files)):
        text = DocumentProcessor(files[i], STRINGS.RESUME).read_text_from_file()
    
        corpus = []
        doc = nlp1(text)
        for sent in doc.sents:
            corpus.append(sent.text)
    
        for sentence in corpus:
            doc = nlp(sentence)
            entities = []
        
            for ent in doc.ents:
                entities.append([ent.start_char, ent.end_char, ent.label_])
            TRAIN_DATA.append([sentence, {"entities": entities}])
    return TRAIN_DATA

def convert(lang: str, TRAIN_DATA, output_path: Path):
    nlp = spacy.blank(lang)
    db = DocBin()
    for text, annot in TRAIN_DATA:
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    db.to_disk(output_path)

def read_domain_file(keyword_file):   
    file = open(keyword_file,newline='')
    result = file.read()
    result1 = result.split('\n')
    
    keys = []
    short_keys = []
    keywords = []
    import re
    for i in range(len(result1)):
        keywords.append(result1[i].split(': ')[1].split(','))
        key = result1[i].split(': ')[0]
        lis = re.split(r'[()]',key)
        keys.append(lis[0])
        try:
            short_keys.append(lis[1])
        except:
            short_keys.append(lis[0])
            
    dictionary = dict(zip(keys, keywords))
    keywords_df = pd.DataFrame({k:pd.Series(v) for k,v in dictionary.items()})
    # keywords_df = read_domain_file(domain_keywords_file_path)
    keywords_df.columns = keywords_df.columns.str.replace(' ', '') 
    dictionary = keywords_df.to_dict()
    patterns = []
    for key in dictionary:
        skills = list(dictionary[key].values())
        skills = [x for x in skills if str(x) != 'nan']
        for i in range(len(skills)):
            patterns.append({"label": key, "pattern": [{"lOWER": x.lower()} for x in skills[i].split(" ")]})

    with open('job_domains.jsonl', 'w') as f:
        for line in patterns:
            f.write(f"{line}\n")
            
    return keywords_df

# read_domain_file('data/DomainKeywords.txt')
    
# In[]
patterns = load_jsonl(STRINGS.skill_pattern_path)
patterns = patterns + load_jsonl(STRINGS.job_titles_pattern_path)
patterns = patterns + load_jsonl(STRINGS.domain_keywords_file_path)
patterns = patterns + load_jsonl(STRINGS.extra_skill_pattern_path)

train_data = prepare_ner_train_data(patterns)

convert("en", train_data, "data/train.spacy")
convert("en", train_data, "data/valid.spacy")

# create config
# python -m spacy init fill-config data/base_config.cfg data/config.cfg
# train
# python -m spacy train data/config.cfg --paths.train data/train.spacy --paths.dev data/valid.spacy --output ./models/output_trf

# In[]
# python -m spacy train data/config_trf.cfg --output ./models/output_trf
        