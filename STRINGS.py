JD = "job_description"
RESUME = "resume"

skill_pattern_path = "data/jz_skill_patterns.jsonl"
extra_skill_pattern_path = "data/other_skills.jsonl"

job_titles_pattern_path = "data/job_titles.jsonl"
domain_keywords_file_path = 'data/job_domains.jsonl'
TRAINED_NLP_MODEL = "models/output_v2/model-best"
NLP_MODEL = "en_core_web_trf"
RE_PATTERNS = {
    'email_pattern': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b',
    'phone_pattern': r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}",
    'link_pattern': r'\b(?:https?://|www\.)\S+\b',
    'position_year_pattern': r"(\b\w+\b\s+\b\w+\b),\s+(\d{4})\s*-\s*(\d{4}|\bpresent\b)",
    'education_pattern': r"(?i)(?:Bsc|\bB\.\w+|\bM\.\w+|\bPh\.D\.\w+|\bBachelor(?:'s)?|\bMaster(?:'s)?|\bPh\.D)\s(?:\w+\s)*\w+"
}

jd_fields = [
            "job_title",
            "technical_skills",
            "education",
            "industry_domain",
            "language_known",
            "location",
            ]

education_keywords = [
            'Bachelor', 'BE','B.E.', 'B.E', 'BS', 'B.S','C.A.','c.a.','B.Com','B. Com','Bsc', 'B. Pharmacy', 'B Pharmacy', 
            'M. Com', 'M.Com','M. Com .','Msc', 'M. Pharmacy','M. Pharma','M Pharma',
            'ME', 'M.E', 'M.E.', 'MS', 'M.S',
            'BTECH', 'B.TECH', 'M.TECH', 'MTECH','Master',
            'PHD', 'phd', 'ph.d', 'Ph.D.','MBA','mba','graduate', 'post-graduate','5 year integrated masters','masters',
            'SSC', 'HSC', 'CBSE', 'ICSE', 'X', 'XII'
        ]