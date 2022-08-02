from summarizer_build import *
from flask import Flask, render_template, request, redirect, url_for


app = Flask(__name__)
# app.secret_key = "work"

@app.route('/home/', methods= ['POST', 'GET'])
def first():
    if request.method == 'POST':
        name = request.form['text']
        print(name)
        # render_template('test.html', result= name)
        return redirect(url_for('second', txt=name))
    else:
        return render_template('test.html')


@app.route('/<txt>/', methods=['POST', 'GET'])
def second(txt):
    
    return render_template('test.html', result= txt)


# run the server. 
if __name__ == '__main__':
    app.run()