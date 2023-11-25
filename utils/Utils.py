# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 23:04:35 2023

@author: harendra.verma
"""

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import LancasterStemmer, WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
import re, unicodedata
import inflect
import spacy
from uuid import uuid4
import textdistance as td
import STRINGS

nlp = spacy.load(STRINGS.NLP_MODEL)


def generate_uuid():
    """
    This function generate a unique id
    """
    return str(uuid4())


def word_count_frequency(text):
    """
    This function counts the frequecy of words in given text
    """
    doc = nlp(text)

    pos_freq = {}
    for token in doc:
        if token.pos_ in pos_freq:
            pos_freq[token.pos_] += 1
        else:
            pos_freq[token.pos_] = 1
    return pos_freq

def perform_tfidf(token):
    tfidf = TfidfVectorizer(max_df=0.05, min_df=0.002)
    words = tfidf.fit_transform(token)
    sentence = " ".join(tfidf.get_feature_names())
    return sentence


def get_similarity_score(resume, job_des):
    j = td.jaccard.similarity(resume, job_des)
    s = td.sorensen_dice.similarity(resume, job_des)
    c = td.cosine.similarity(resume, job_des)
    o = td.overlap.normalized_similarity(resume, job_des)
    total = (j+s+c+o)/4
    return total*100

def check_regex_match(match):
    if match is not None:
        return True
    return False

def sanitize_string(content: str):
    return content.lower().strip()

class DocumentCleaner:

    def __init__(self, raw_text):
        self.raw_input_text = raw_text
    
    def clean_text(self):
        """
        clean raw text
        """
        text = self.remove_specific_patterns(self.raw_input_text.lower())
        words = word_tokenize(text)
        words = self.remove_non_ascii(words)
        words =  self.to_lowercase(words)
        words =  self.remove_punctuation(words)
        # words = replace_numbers(words)
        words =  self.remove_stopwords(words)
        # words =  self.stem_words(words)
        # words =  self.lemmatize_verbs(words)
        cleaned_text = ' '.join(words)

        return cleaned_text    
    
    @staticmethod
    def remove_specific_patterns(text):
        """
        remove links and specific patterns
        """
        for pattern in STRINGS.RE_PATTERNS:
            text = re.sub(STRINGS.RE_PATTERNS[pattern], '', text)
        return text
    
    @staticmethod
    def remove_non_ascii(words):
        """Remove non-ASCII characters from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
            new_words.append(new_word)
        return new_words
    
    @staticmethod
    def to_lowercase(words):
        """Convert all characters to lowercase from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = word.lower()
            new_words.append(new_word)
        return new_words
    
    @staticmethod
    def remove_punctuation(words):
        """Remove punctuation from list of tokenized words"""
        new_words = []
        for word in words:
            new_word = re.sub(r'[^\w\s]', '', word)
            if new_word != '':
                new_words.append(new_word)
        return new_words
    
    @staticmethod
    def replace_numbers(words):
        """Replace all interger occurrences in list of tokenized words with textual representation"""
        p = inflect.engine()
        new_words = []
        for word in words:
            if word.isdigit():
                new_word = p.number_to_words(word)
                new_words.append(new_word)
            else:
                new_words.append(word)
        return new_words
    
    @staticmethod
    def remove_stopwords(words):
        """Remove stop words from list of tokenized words"""
        new_words = []
        for word in words:
            if word not in stopwords.words('english'):
                new_words.append(word)
        return new_words
    
    @staticmethod
    def stem_words(words):
        """Stem words in list of tokenized words"""
        stemmer = LancasterStemmer()
        stems = []
        for word in words:
            stem = stemmer.stem(word)
            stems.append(stem)
        return stems
    
    @staticmethod
    def lemmatize_verbs(words):
        """Lemmatize verbs in list of tokenized words"""
        lemmatizer = WordNetLemmatizer()
        lemmas = []
        for word in words:
            lemma = lemmatizer.lemmatize(word, pos='v')
            lemmas.append(lemma)
        return lemmas
    