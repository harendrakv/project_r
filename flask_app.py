from flask import Flask, jsonify, request, make_response
from resumeParser import extract_resume_data
from jdParser import extract_jd_data

import STRINGS
from file_util import check_if_file
from pathlib import Path

# creating a Flask app
app = Flask(__name__)

@app.route('/resume_filter', methods=['POST'])
def handle_rf_post():
    if request.method == 'POST':
        data = request.json
        if ('resume_file_path' in data and check_if_file(Path(data['resume_file_path'])) and 
            'jd_file_path' in data and check_if_file(Path(data['jd_file_path']))):
            extract_resume_data(data['resume_file_path'])
            extract_jd_data(data['jd_file_path'])
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
