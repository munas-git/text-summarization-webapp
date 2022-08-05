from summarizer_build import *
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)


@app.route('/summarize/', methods= ['GET', 'POST'])
def first():
    if request.method == 'GET':
        return render_template('test.html')
    elif request.method == 'POST':
        name = request.form.get('text', None)
        return render_template('test.html', final_summary=name)


# run the server. 
if __name__ == '__main__':
    app.run()