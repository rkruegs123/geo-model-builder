from flask import render_template, request
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/getimage')
def get_img():
    return "barney.jpg"

@app.route('/solve', methods=['POST'])
def solve():
    jsdata = request.form['hi']
    return jsdata + "xyz"
