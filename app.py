from summarizer_build import *
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route("/home/")
def home():
    # 
    return render_template(...)


# 
if __name__ == '__main__':
    app.run()