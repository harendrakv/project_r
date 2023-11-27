# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 14:03:14 2023

@author: harendra.verma
"""

import os
from text_extraction import process_resumes, process_job_descriptions
from resumeKeywordsMatcher import process_resumes_for_keywords_matching, list_domains, sort_resumes
import STRINGS
from utils import FilesUtility
from similarity_scores import TextSimilarityScore
import pandas as pd

# In[]
if __name__=='__main__':
    
    # process_resumes(FilesUtility.resumes_path)
    process_job_descriptions(FilesUtility.jd_path)
    
    # processed_resume_files = os.listdir(FilesUtility.resumes_save_path)
    processed_jdsfiles = os.listdir(os.path.join(FilesUtility.user_file_path, FilesUtility.jd_save_path))
    sim_df = TextSimilarityScore().get_resumes_similarity_given_jd(processed_jdsfiles[0])
    fields_df = TextSimilarityScore().get_keywords_similarity_given_jd(processed_jdsfiles[0])
    final_df = pd.merge(sim_df, fields_df, how="inner", on=["resumes"])
    outpath = os.path.join(FilesUtility.user_file_path, 'output')
    if not os.path.isdir(outpath):
        os.mkdir(outpath)
        
    final_df.to_csv(os.path.join(outpath,"processed_resumes_for_jd_{}".format(processed_jdsfiles[0])+".csv"))

    
    keyword_file = "Keywords.txt"
    process_resumes_for_keywords_matching(keyword_file, outpath=outpath)
    entities = list_domains(keyword_file)
    for entity in entities:
        try:
            sort_resumes(entity, outpath=outpath)
        except:
            pass
        