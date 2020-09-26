from flask import render_template, request, Response
from app import app

from builder import build
from util import DEFAULTS

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/getimage')
def get_img():
    return "barney.jpg"

@app.route('/solve', methods=['POST'])
def solve():
    try:
        jsdata = request.form['hi']
        lines = str(jsdata).split('\n')

        args = DEFAULTS
        args['lines'] = lines

        print(lines)
        return jsdata + "xyz"
    except:
        return Response(
            "Invalid input",
            status=400
        )
