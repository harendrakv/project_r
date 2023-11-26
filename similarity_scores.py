# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 17:03:45 2023

@author: harendra.verma
"""
import os
import textdistance as td
import json
from utils import FilesUtility
import pandas as pd
import STRINGS

class TextSimilarityScore:
    def __init__(self, base_path=None):
        if base_path:
            resumes_path = os.path.join(base_path, FilesUtility.resumes_save_path)
            jds_path = os.path.join(base_path, FilesUtility.jd_save_path)
        else:
            resumes_path = os.path.join(FilesUtility.user_file_path, FilesUtility.resumes_save_path)
            jds_path = os.path.join(FilesUtility.user_file_path, FilesUtility.jd_save_path)

        resumes = []
        for file in os.listdir(resumes_path):
            r1 = json.load(open(os.path.join(resumes_path, file)))
            resumes.append(r1)
        self.resumes =resumes     

        jds = []
        for file in os.listdir(jds_path):
            jd1 = json.load(open(os.path.join(jds_path, file)))
            jds.append(jd1)
        self.jds =jds 
    
    @staticmethod
    def calc_jaccard_similarity(res_text, jd_text):
        return td.jaccard.similarity(res_text, jd_text)
   
    @staticmethod
    def calc_cosine_similarity(res_text, jd_text):
        return td.cosine.similarity(res_text, jd_text)
    
    @staticmethod
    def calc_overlap_similarity(res_text, jd_text):
        return td.overlap.normalized_similarity(res_text, jd_text)
    
    @staticmethod
    def calc_sorensen_dice_similarity(res_text, jd_text):
        return td.sorensen_dice.similarity(res_text, jd_text)    
    
    def get_average_similarity(self, res_text, jd_text):
        jaccard_s = self.calc_jaccard_similarity(res_text, jd_text)
        cosine_s = self.calc_cosine_similarity(res_text, jd_text)
        overlap_s = self.calc_overlap_similarity(res_text, jd_text)
        sorensen_s = self.calc_sorensen_dice_similarity(res_text, jd_text)
        total_similarity = (jaccard_s+cosine_s+overlap_s+sorensen_s)/4
        return total_similarity
    
    def get_resumes_similarity_given_jd(self, jd_path):       
        jd = json.load(open(os.path.join(FilesUtility.user_file_path,FilesUtility.jd_save_path, jd_path)))
        resume_scores = []
        resume_files = []
        for i in range(len(self.resumes)):
            score = self.get_average_similarity(self.resumes[i]['cleantext'], jd['cleantext'])  
            resume_scores.append(score)
            resume_files.append(self.resumes[i]['resume_file'])
        return pd.DataFrame({"resumes": resume_files, "score": resume_scores})
    
    def get_jd_similarity_given_resume(self, resume_path):       
        resume = json.load(open(os.path.join(FilesUtility.user_file_path, FilesUtility.resume_save_path, resume_path)))
        jd_scores = []
        jd_files = []
        for i in range(len(self.jds)):
            score = self.get_similarity(self.jds[i]['cleantext'], resume['cleantext'])  
            jd_scores.append(score)
            jd_files.append(self.jds[i]['jd_file'])
        return pd.DataFrame({"jd": jd_files, "score": jd_scores})
    
    @staticmethod
    def get_keywords_matches(jd_kws, resume_kws):
        matches = []  
        for i in range(len(jd_kws)):
            for j in range(len(resume_kws)):
                if jd_kws[i]==resume_kws[j]:
                    matches.append(jd_kws[i])
                    break    
        return matches
    
    def get_keywords_similarity_given_jd(self, jd_path, tags=None):
        # other tags are job_title, location, education and industry_domain
        if tags==None:
            tags=STRINGS.jd_fields
        jd = json.load(open(os.path.join(FilesUtility.user_file_path, FilesUtility.jd_save_path, jd_path)))
        
        dflist = []
        for j, tag in enumerate(tags):
            jd_keywords = jd[tag]
            if len(jd_keywords)>0:
                matching_keywords = []
                resume_files = []
                keywords_match_score = []
                for i in range(len(self.resumes)):
                    resume_keywords = self.resumes[i][tag]
                    matches = self.get_keywords_matches(jd_keywords, resume_keywords)
                    score = len(matches)/len(jd_keywords)*100
                    matching_keywords.append(matches)
                    keywords_match_score.append(score)
                    resume_files.append(self.resumes[i]['resume_file'])
                
                matched_df = pd.DataFrame({"resumes": resume_files, tag+"_matched": matching_keywords, tag+"_score": keywords_match_score})
                dflist.append(matched_df)
            else:
                pass
        fields_df = pd.concat(dflist, axis=1, join="inner")
        fields_df = fields_df.loc[:,~fields_df.columns.duplicated(keep='last')]
        return fields_df       
    
    
    
    # def match_skills(jd_skills, resume_skills):
    #     skill_score = []  
    #     matched_skills = []  
    #     for i in range(len(jd_skills)):
    #         for j in range(len(resume_skills)):
    #             score = nlp(jd_skills[i]).similarity(nlp(resume_skills[j]))    
    #             if score>=.8:
    #                 matched_skills.append(jd_skills[i])
    #                 break
    #         skill_score.append(score)
        
    #     return matched_skills
        
    
    