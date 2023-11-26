# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 13:59:19 2023

@author: harendra.verma
"""
import textacy
from textacy import extract
import spacy
from spacy.matcher import Matcher
import nltk
import re
from utils import DocumentCleaner
import STRINGS

trained_ner = spacy.load(STRINGS.TRAINED_NLP_MODEL)
all_ents = list(trained_ner.get_pipe("ner").labels)
nlp = spacy.load(STRINGS.NLP_MODEL)

class FieldsExtractor:

    def __init__(self, raw_text):
    
        self.text = raw_text
        self.clean_text = DocumentCleaner(self.text).clean_text()
        self.doc = nlp(self.clean_text)
        self.ner_doc = trained_ner(self.clean_text)

    def extract_name(self):
        matcher = Matcher(nlp.vocab)
        pattern1 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
        pattern2 = [{'POS': 'PROPN'}, {'POS': 'PROPN'}, {'POS': 'PROPN'}]

        matcher.add('NAME', [pattern1, pattern2])
        matches = matcher(self.doc)
        spans = [self.doc[start:end] for _, start, end in matches]
        names = []
        for span in spacy.util.filter_spans(spans):
            names.append(span.text)

        return names[0]

    def extract_technical_skills(self):
        skills = [ent.text for ent in self.ner_doc.ents if ent.label_ == 'SKILL']
        return list(set(skills))
    
    def extract_language_known(self):
        langs = [ent.text for ent in self.doc.ents if ent.label_ == 'LANGUAGE']
        return langs
    
    def extract_links(self):
        weblinks = re.findall(STRINGS.RE_PATTERNS['link_pattern'], self.text)
        return weblinks

    def extract_emails(self):
        email_pattern = STRINGS.RE_PATTERNS['email_pattern']
        emails = re.findall(email_pattern, self.text)
        return emails

    def extract_phone_numbers(self):
        phone_number_pattern = STRINGS.RE_PATTERNS['phone_pattern']
        phone_numbers = re.findall(phone_number_pattern, self.text)
        return phone_numbers

    def extract_location(self):
        location = [ent.text for ent in self.doc.ents if ent.label_ == 'GPE']
        return list(set(location))
    
    def extract_job_title(self):
        jobtitles = [ent.text for ent in self.ner_doc.ents if ent.label_ == 'JOBTITLE']
        if len(jobtitles)==0:
            domain_ents = [ent for ent in all_ents if ent not in ['SKILL']]
            jobtitles = [ent.label_ for ent in self.ner_doc.ents if ent.label_ in domain_ents]

        return list(set(jobtitles))

    def extract_education(self):
        education = []
        for keyword in STRINGS.education_keywords:
            pattern = r"(?i)\b{}\b".format(re.escape(keyword))
            match = re.search(pattern, self.text)
            if match:
                education.append(match.group())
        return education
    
    def extract_industry_and_domain(self):
        domain_ents = [ent for ent in all_ents if ent not in ['JOBTITLE', 'SKILL']]
        domains = [ent.label_ for ent in self.ner_doc.ents if ent.label_ in domain_ents]
        return list(set(domains))

    def extract_experience(self):
        experience=[]
        for sentence in self.doc.sents:
            word_list = []
            for word in sentence:
                try:
                    word_list.append(word.text.lower())
                except:
                    word_list.append(word.text)
            sent = " ".join(word_list)
            if re.search('experience',sent):
                sent_tokenised= nltk.word_tokenize(sent)
                tagged = nltk.pos_tag(sent_tokenised)
                entities = nltk.chunk.ne_chunk(tagged)
                for subtree in entities.subtrees():
                    for leaf in subtree.leaves():
                        if leaf[1]=='CD':
                            experience=leaf[0]
        
        return experience

class KeyphraseExtractor:
    
    def __init__(self, text, top_counts=30):
        
        self.text = text
        self.doc = nlp(text)
        self.top_counts = top_counts

    def get_keyphrase_using_spacy(self):
        keywords = []
        for chunk in self.doc.noun_chunks: 
            if chunk.text.lower() not in nlp.Defaults.stop_words: 
                keywords.append(chunk.text)
        return keywords

    def get_keyphrase_using_scake(self):
        keywords = [kps for kps, weights in list(extract.keyterms.scake(self.doc, normalize="lemma",
                                           topn=self.top_counts))]
        return keywords
    