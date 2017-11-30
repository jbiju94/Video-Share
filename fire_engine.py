from flask import Flask, render_template, request
from awsClient import awsClient
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)


@app.route("/")
def homepage():
    aws = awsClient('s3')
    videos = aws.list_files()
    return render_template('index.html', videos=videos)


@app.route("/video/<action>/<key>")
def get_video_details(action, key):
    aws = awsClient('s3')
    if action == 'get':
        video = aws.get_file_details(key)
        return json.dumps(video)
    elif action == 'delete':
        resp = aws.delete_file(key)
        videos = aws.list_files()
        return render_template('index.html', videos=videos, responce=resp)


@app.route("/uploadVideo", methods=['POST'])
def upload_video():
    if request.method == 'POST':
        aws = awsClient('s3')
        file_object = request.files['file']
        if file_object.filename == "":
            return "Please select a file"
        file_object.filename = secure_filename(file_object.filename)
        aws.upload_file(file_object)
        videos = aws.list_files()
        return render_template('index.html', videos=videos)
    else:
        return render_template('index.html')


if __name__ == "__main__":
    app.run()
