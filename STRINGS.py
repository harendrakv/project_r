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

FAILURE_RESPONSE = '''
<html>
  <head>
<link href="https://fonts.googleapis.com/css?family=Nunito+Sans:400,400i,700,900&display=swap" rel="stylesheet">
  </head>
    <style>
      body {
        text-align: center;
        padding: 40px 0;
        background: #EBF0F5;
      }
        h1 {
          color: #FF0000;
          font-family: "Nunito Sans", "Helvetica Neue", sans-serif;
          font-weight: 900;
          font-size: 40px;
          margin-bottom: 10px;
        }
        p {
          color: #404F5E;
          font-family: "Nunito Sans", "Helvetica Neue", sans-serif;
          font-size:20px;
          margin: 0;
        }
      i {
        color: #FF0000;
        font-size: 100px;
        font-family: sans-serif;
        line-height: 200px;
        margin-left:-15px;
      }
      .card {
        background: white;
        padding: 60px;
        border-radius: 4px;
        box-shadow: 0 2px 3px #C8D0D8;
        display: inline-block;
        margin: 0 auto;
      }
    </style>
    <body>
      <div class="card">
      <div style="border-radius:200px; height:200px; width:200px; background: #F8FAF5; margin:0 auto;">
        <i class="checkmark">X</i>
      </div>
        <h1>Failed</h1> 
        <p> Something went wrong!<br/>Please Try Again Later</p>
      </div>
    </body>
</html>
'''


SUCCESS_RESPONSE = '''
<html>
  <head>
    <link href="https://fonts.googleapis.com/css?family=Nunito+Sans:400,400i,700,900&display=swap" rel="stylesheet">
  </head>
    <style>
      body {
        text-align: center;
        padding: 40px 0;
        background: #EBF0F5;
      }
        h1 {
          color: #88B04B;
          font-family: "Nunito Sans", "Helvetica Neue", sans-serif;
          font-weight: 900;
          font-size: 40px;
          margin-bottom: 10px;
        }
        p {
          color: #404F5E;
          font-family: "Nunito Sans", "Helvetica Neue", sans-serif;
          font-size:20px;
          margin: 0;
        }
      i {
        color: #9ABC66;
        font-size: 100px;
        line-height: 200px;
        margin-left:-15px;
      }
      .card {
        background: white;
        padding: 60px;
        border-radius: 4px;
        box-shadow: 0 2px 3px #C8D0D8;
        display: inline-block;
        margin: 0 auto;
      }
    </style>
    <body>
      <div class="card">
      <div style="border-radius:200px; height:200px; width:200px; background: #F8FAF5; margin:0 auto;">
        <i class="checkmark">✓</i>
      </div>
        <h1>Success</h1> 
        <p>Your File converted;<br/> Check your file path provided in request!</p>
      </div>
    </body>
</html>
'''