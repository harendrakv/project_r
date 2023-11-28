# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 22:43:58 2023

@author: harendra.verma
"""

from utils import DocumentCleaner
from .feature_extractors import KeyphraseExtractor, FieldsExtractor


class ResumeTextParser:

    def __init__(self, text):
        self.raw_text = text
        self.cleantext = DocumentCleaner(self.raw_text).clean_text()
        self.job_title = FieldsExtractor(self.cleantext).extract_job_title()
        self.name = FieldsExtractor(self.cleantext).extract_name()
        self.experience = FieldsExtractor(self.cleantext).extract_experience()
        self.technical_skills = FieldsExtractor(
            self.cleantext).extract_technical_skills()
        self.education = FieldsExtractor(self.cleantext).extract_education()
        self.industry_and_domain = FieldsExtractor(
            self.cleantext).extract_industry_and_domain()
        self.links = FieldsExtractor(self.raw_text).extract_links()
        self.emails = FieldsExtractor(self.raw_text).extract_emails()
        self.phones = FieldsExtractor(self.raw_text).extract_phone_numbers()
        self.location = FieldsExtractor(self.cleantext).extract_location()
        self.language_known = FieldsExtractor(
            self.cleantext).extract_language_known()
        self.keyphrases = KeyphraseExtractor(
            self.cleantext).get_keyphrase_using_spacy()

    def get_json_file(self):
        """
        Returns a dictionary of resume data.
        """
        outfile = {
            "raw_text": self.raw_text,
            "cleantext": self.cleantext,
            # "links": self.links,
            "keyphrases": self.keyphrases,
            "name": self.name,
            "experience": self.experience,
            "emails": self.emails,
            "phones": self.phones,
            "job_title": self.job_title,
            "technical_skills": self.technical_skills,
            "education": self.education,
            "industry_domain": self.industry_and_domain,
            "language_known": self.language_known,
            "location": self.location,
        }

        return outfile


class JDTextParser:

    def __init__(self, text):
        self.raw_text = text
        self.cleantext = DocumentCleaner(self.raw_text).clean_text()
        self.job_title = FieldsExtractor(self.cleantext).extract_job_title()
        self.technical_skills = FieldsExtractor(
            self.cleantext).extract_technical_skills()
        self.education = FieldsExtractor(self.cleantext).extract_education()
        self.industry_and_domain = FieldsExtractor(
            self.cleantext).extract_industry_and_domain()
        self.location = FieldsExtractor(self.cleantext).extract_location()
        self.language_known = FieldsExtractor(
            self.cleantext).extract_language_known()
        self.keyphrases = KeyphraseExtractor(
            self.cleantext).get_keyphrase_using_spacy()

    def get_json_file(self):
        outtile = {
            "raw_text": self.raw_text,
            "cleantext": self.cleantext,
            "job_title": self.job_title,
            "technical_skills": self.technical_skills,
            "education": self.education,
            "industry_domain": self.industry_and_domain,
            "language_known": self.language_known,
            "location": self.location,
            "keyphrases": self.keyphrases,
        }

        return outtile
