# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 14:03:14 2023

@author: harendra.verma
"""

import os
from text_extraction import process_resumes, process_job_descriptions
import STRINGS
from utils import FilesUtility
from similarity_scores import TextSimilarityScore
import pandas as pd

# In[]
if __name__=='__main__':
    
    # process_resumes()
    # process_job_descriptions()
    
    # processed_resume_files = os.listdir(FilesUtility.resumes_save_path)
    processed_jdsfiles = os.listdir(FilesUtility.jd_save_path)
    sim_df = TextSimilarityScore().get_resumes_similarity_given_jd(processed_jdsfiles[0])
    fields_df = TextSimilarityScore().get_keywords_similarity_given_jd(processed_jdsfiles[0])
    final_df = pd.merge(sim_df, fields_df, how="inner", on=["resumes"])

    final_df.to_csv("output/processed_resumes_for_jd_{}".format(processed_jdsfiles[0])+".csv")