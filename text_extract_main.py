# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 14:03:14 2023

@author: harendra.verma
"""

import os
from text_extraction import DocumentProcessor
from text_extraction import ResumeTextParser,JDTextParser
import STRINGS

# In[]
if __name__=='__main__':
    
    resume_files = os.listdir(STRINGS.RESUME_FILES_PATH)
    for i, file in enumerate(resume_files):
        print("Processing resume {} of {}".format(i, len(resume_files)))
        doc_pr = DocumentProcessor(file, STRINGS.RESUME).process_text()


    jd_files = os.listdir(STRINGS.JD_FILES_PATH)
    for i, file in jd_files:
        print("Processing job descriptio {} of {}".format(i, len(jd_files)))
        doc_pr = DocumentProcessor(file, STRINGS.JD).process_text()