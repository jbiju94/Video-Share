from flask import Flask, render_template
from awsClient import awsClient

app = Flask(__name__)


@app.route("/")
def homepage():
    aws = awsClient('s3')
    videos = aws.list_files()
    return render_template('index.html', videos=videos)


@app.route("/listAllVideos")
def list_all_videos():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
