# -*- coding: utf-8 -*-
"""
Created on Fri Nov 24 11:11:53 2023

@author: harendra.verma
"""

import pathlib
import json
from utils import FilesUtility, extract_pdf_data, process_image
from .doc_parser import ResumeTextParser,JDTextParser
import docx
import os

import STRINGS

# In[]
class DocumentProcessor:
    def __init__(self, filename, identifier=None):
        self.filename = filename
        self.identifier = identifier
        if self.identifier==STRINGS.RESUME:
            self.filepath = os.path.join(os.getcwd(), FilesUtility().resumes_path, self.filename)
        else:
            self.filepath = os.path.join(os.getcwd(), FilesUtility().jd_path, self.filename)
    
    def process_text(self):
        try:
            if self.identifier==STRINGS.RESUME:
                out_dict = self.read_resume_file()
            else:
                out_dict = self.read_jd_file()

            self.write_json_file(out_dict)
            return True
        except Exception as error:
            print(f"Error: {str(error)}")
            return  False
        
    def read_resume_file(self):
        data = self.read_text_from_file()
        self.raw_text = data
        out_dict = ResumeTextParser(data).get_json_file()
        return out_dict

    def read_jd_file(self):
        data = self.read_text_from_file()
        self.raw_text = data
        out_dict = JDTextParser(data).get_json_file()
        return out_dict

    def write_json_file(self, dictionary):
        file_name = str(self.identifier + pathlib.Path(self.filepath).stem +
                        dictionary["uid"] + ".json")
        
        if self.identifier==STRINGS.RESUME:
            save_directory_name = os.path.join(os.getcwd(), FilesUtility.resumes_save_path, file_name)
        else:
            save_directory_name = os.path.join(os.getcwd(), FilesUtility.jd_save_path, file_name)

        json_object = json.dumps(dictionary, sort_keys=True)
        with open(save_directory_name, "w+") as outfile:
            outfile.write(json_object)
                    
    def convertDocxToText(self):
        document = docx.Document(self.filepath)
        return "\n".join([para.text for para in document.paragraphs])
    
    def read_text_from_file(self):
        if self.filepath.endswith('.docx') or self.filepath.endswith('.doc'):
            text = self.convertDocxToText()
        elif self.filepath.endswith('.pdf') or self.filepath.endswith('.PDF'):
            text = extract_pdf_data(self.filepath)
        elif self.filepath.endswith('.txt'):
            with open(self.filepath) as f:
                text = f.read()     
        elif self.filepath.endswith('.png'):
            text = text + " " + process_image(self.filepath)
        else:
            print("File extention exception")
        text = str(text)
        
        return text            
    
    