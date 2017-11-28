from flask import Flask, render_template
from awsClient import awsClient as aws

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/listAllVideos")
def list_all_videos():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
