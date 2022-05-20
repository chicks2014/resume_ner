from flask import Flask, request, render_template
import os
from flask_cors import CORS, cross_origin
from werkzeug.utils import secure_filename
from pipeline import prediction_pipeline

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)

@app.route("/", methods=['GET'])
@cross_origin()
def home():
    return render_template('index.html')

def store_file(file_content):
    home_dir = os.path.expanduser("~")
    UPLOAD_FOLDER = os.path.join(home_dir, "upload")
    with open(UPLOAD_FOLDER, 'w', encoding="utf-8") as f:
        f.write(file_content)

@app.route("/predict", methods=['POST'])
@cross_origin()
def predictRoute():

    file = request.files['file-0']
    filename = secure_filename(file.filename)
    dest_path = r'../resumes/prediction/01_resume_source/'
    file.save(dest_path + filename)

    pred_pipe = prediction_pipeline()
    pred_pipe.predict()

    return "{result: success}"


#port = int(os.getenv("PORT"))
if __name__ == "__main__":
    #app.run(host='0.0.0.0', port=port)
    app.run(host='127.0.0.1', port=5001, debug=True)
