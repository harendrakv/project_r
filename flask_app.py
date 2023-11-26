import os
from text_extraction import process_resumes, process_job_descriptions
import STRINGS
from utils import FilesUtility, check_if_file
from similarity_scores import TextSimilarityScore
import pandas as pd
from pathlib import Path
from flask import Flask, jsonify, request, make_response

# creating a Flask app
app = Flask(__name__)

@app.route('/resume_filter', methods=['POST'])
def handle_rf_post():
    if request.method == 'POST':
        data = request.json
        if ('resume_file_path' in data and 
            'jd_file_path' in data):
            process_resumes(data['resume_file_path'])
            process_job_descriptions(data['jd_file_path'])
            processed_jdsfiles = os.listdir(FilesUtility.jd_save_path)
            base_path = Path(data['jd_file_path']).parent
            for i in range(len(processed_jdsfiles)):
                print("Creating match for job description {} of {}".format(i+1, len(processed_jdsfiles)))
                sim_df = TextSimilarityScore(base_path).get_resumes_similarity_given_jd(processed_jdsfiles[i])
                fields_df = TextSimilarityScore(base_path).get_keywords_similarity_given_jd(processed_jdsfiles[i])
                final_df = pd.merge(sim_df, fields_df, how="inner", on=["resumes"])
                outpath = os.path.join(base_path, 'output')
                if not os.path.isdir(outpath):
                    os.mkdir(outpath)
                    
                final_df.to_csv(os.path.join(outpath,"processed_resumes_for_jd_{}".format(processed_jdsfiles[i])+".csv"))
            
            response = make_response(STRINGS.SUCCESS_RESPONSE)
            response.status_code = 200
            return response
            
        else:
            response = make_response("<h1><li>Missing one or more required parameter/s</li><br /> <li>Path does not have specified file</li></h1>")
            response.status_code = 400
            return response

    else:
        response = make_response("<h1>Wrong Request</h1>")
        response.status_code = 400
        return response



# driver function
if __name__ == '__main__':
    app.run(debug=True)
