"""Views for the Chart blueprint."""

import json
import random
import time

from flask import Blueprint, Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
chart = Blueprint('chart', __name__, template_folder="templates")
sock = Sock(app)

START_TIME = 0


@chart.route("/chart", methods=["GET"])
def index() -> str:
    """
    Serve `chart` page template.

    :returns: str
    """
    return render_template(
        "chart/index.jinja2",
        title="Charts",
        template="chart-template",
    )


@chart.route("/chart-random", methods=["GET"])
def chart_random() -> str:
    """
    Serve `chart` page template.

    :returns: str
    """
    global START_TIME  # pylint: disable=global-statement
    START_TIME = 0
    return render_template(
        "chart/index.jinja2",
        title="Charts",
        template="chart-template",
    )


@sock.route("/chart-data", bp=chart)
def chart_data(ws):
    """
    WebSocket endpoint which serves up chart data.
    """
    global START_TIME  # pylint: disable=global-statement
    if START_TIME == 0:
        START_TIME = time.time()
    while True:
        json_data = json.dumps({
            "time": f'{time.time() - START_TIME:.3f}',
            "value": random.random() * 100,
        })
        ws.send(f'{json_data}\n\n')
        time.sleep(0.5)
