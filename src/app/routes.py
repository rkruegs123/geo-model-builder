from flask import render_template, request, Response, send_file
from app import app
from io import StringIO, BytesIO
import pdb
import base64

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

        figs = build(args, show_plot=False, encode_fig=True)
        fig = figs[0]

        img = BytesIO()
        fig.savefig(img, format='png')
        fig.close()
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return f"data:image/png;base64,{plot_url}"

    except Exception as e:
        return Response(
            "Invalid input",
            status=400
        )
