# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 00:46:20 2023

@author: harendra.verma
"""
import os
from io import StringIO
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
from spacy.matcher import PhraseMatcher
import spacy
import STRINGS
import json
from utils import FilesUtility
import re
import matplotlib
matplotlib.use('Agg')


nlp = spacy.load(STRINGS.NLP_MODEL)


def spacy_phrase_matcher(keyword_file):
    file = open(keyword_file, newline='')
    result = file.read()
    result1 = result.split('\n')

    keys = []
    short_keys = []
    keywords = []
    for i in range(len(result1)):
        keywords.append(result1[i].split(': ')[1].split(','))
        key = result1[i].split(': ')[0]
        lis = re.split(r'[()]', key)
        keys.append(lis[0])
        try:
            short_keys.append(lis[1])
        except:
            short_keys.append(lis[0])
    dictionary = dict(zip(keys, keywords))
    keyword_df = pd.DataFrame({k: pd.Series(v) for k, v in dictionary.items()})
    matcher = PhraseMatcher(nlp.vocab)
    for i in range(len(short_keys)):
        words = [nlp(text) for text in keyword_df[keys[i]].dropna(axis=0)]
        matcher.add(short_keys[i], None, *words)
    return matcher

# In[Function for creating database for resumes based on keywords]

def create_database(phraseMatcher):
    extracted_resumes_path = os.path.join(
        FilesUtility.user_file_path, FilesUtility.resumes_save_path)
    resumeFiles = os.listdir(extracted_resumes_path)
    final_database = []
    i = 0
    while i < len(resumeFiles):
        file = resumeFiles[i]
        print("Processing: ", os.path.basename(file),
              "        ..."+str(i+1)+"/"+str(len(resumeFiles)))
        try:
            text_dict = json.load(
                open(os.path.join(extracted_resumes_path, file)))
            doc = nlp(text_dict['cleantext'])
            resume = text_dict['resume_file']
            # Match the keywords present in text/doc using phrase_matcher
            d = []
            matches = phraseMatcher(doc)
            for match_id, start, end in matches:
                rule_id = nlp.vocab.strings[match_id]
                span = doc[start: end]  # get the matched slice of the doc
                d.append((rule_id, span.text))
            keywords = "\n".join(
                f'{i[0]}&{i[1]}&({j})' for i, j in Counter(d).items())

            # convertimg string of keywords to dataframe
            df = pd.read_csv(StringIO(keywords), names=['Keywords_List'])
            df1 = pd.DataFrame(df.Keywords_List.str.split(
                '&').tolist(), columns=['Subject', 'Keyword', 'Count'])
            df1['Count'] = df1.Count.str.extract('(\d+)')
            df1['resumes'] = [resume]*len(df1)

            final_database.append(df1)
            i += 1

        except:
            print("There was an error processing", file)
            i += 1

    return final_database

# In[Function for Plotting]


def list_domains(keyword_file):
    file = open(keyword_file, newline='')
    result = file.read()
    result1 = result.split('\n')

    keys = []
    short_keys = []
    keywords = []
    import re
    for i in range(len(result1)):
        keywords.append(result1[i].split(': ')[1].split(','))
        key = result1[i].split(': ')[0]
        lis = re.split(r'[()]', key)
        keys.append(lis[0])
        try:
            short_keys.append(lis[1])
        except:
            short_keys.append(lis[0])
    return short_keys


def sort_n_plot(data, subject, no_samples_to_plot, threshold, outpath=None):

    for c in data.columns.tolist():
        data.loc[data[c] < threshold, c] = 0

#    data[data.values < threshold] = 0
    plot_df1 = data.sort_values(by=[subject], ascending=False)[
        :no_samples_to_plot]
    cols = list(plot_df1.columns)
    cols.remove(subject)
    plot_df1 = plot_df1[[subject]+cols]

    plt.rcParams.update({'font.size': 8})
    plot_df = plot_df1.sort_values(by=[subject], ascending=True)
    ax = plot_df.plot.barh(title="Top "+str(no_samples_to_plot)+" Resumes sorted by " +
                           subject+" out of "+str(len(data)), figsize=(12, 6), legend=False, stacked=True)
    labels = []
    for j in plot_df.columns:
        for i in plot_df.index:
            #            label = str(plot_df.loc[i][j])
            label = str(j)+": " + str(plot_df.loc[i][j])
            labels.append(label)

    patches = ax.patches
    for label, rect in zip(labels, patches):
        width = rect.get_width()
        if width > 0:
            x = rect.get_x()
            y = rect.get_y()
            height = rect.get_height()
            ax.text(x + width/2., y + height/2.,
                    label, ha='center', va='center')
    plt.tight_layout()
    if outpath == None:
        plt.savefig(os.path.join(os.getcwd, 'output',
                    'resumes_sorted_by_{}.png'.format(subject)))
    else:
        plt.savefig(os.path.join(
            outpath, 'resumes_sorted_by_{}.png'.format(subject)))
    plt.close('all')


def process_resumes_for_keywords_matching(keyword_file, threshold_for_keyword_count_perSubject=0, outpath=None):
    # Read all the resume files and create a database based on skills and keywords matching
    phraseMatcher = spacy_phrase_matcher(keyword_file)
    dflist = create_database(phraseMatcher)
    data_df = pd.concat(dflist)
    data_df['Count'] = pd.to_numeric(data_df['Count'])

    # Grouping the Skills based on keywords for each candidate
    data_df1 = data_df[data_df.Count > threshold_for_keyword_count_perSubject]
    data_df1 = data_df1['Keyword'].groupby(
        [data_df1['resumes'], data_df1['Subject']]).count().unstack()
    data_df1.reset_index(inplace=True)
    data_df1.fillna(0, inplace=True)
    data_df2 = data_df1.iloc[:, 1:]
    data_df2.index = data_df1['resumes']
    if outpath == None:
        data_df2.to_csv(os.path.join(os.getcwd, 'output', 'sample.csv'))
    else:
        data_df2.to_csv(os.path.join(outpath, 'sample.csv'))


def sort_resumes(entity, n=5, outpath=None):
    if outpath == None:
        data = pd.read_csv(os.path.join(os.getcwd, 'output', 'sample.csv'))
    else:
        data = pd.read_csv(os.path.join(outpath, 'sample.csv'))

    data.index = data['resumes']
    data = data.drop('resumes', axis=1)
    threshold_perSubject = 2  # minimum number of keywords for subject to be identified
    sort_n_plot(data, entity, n, threshold_perSubject, outpath=outpath)

# In[]


if __name__ == '__main__':
    keyword_file = "keywords.txt"
    process_resumes_for_keywords_matching(keyword_file)
    entities = list_domains(keyword_file)
    for entity in entities:
        try:
            sort_resumes(entity)
        except:
            pass
