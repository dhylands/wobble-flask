"""Views for the Home blueprint."""

from flask import Blueprint, Flask, render_template
from flask_sock import Sock

app = Flask(__name__)
home = Blueprint('home', __name__, template_folder="templates")
sock = Sock(app)


@home.route("/", methods=["GET"])
def index() -> str:
    """
    Serve `Home` page template.

    :returns: str
    """
    return render_template(
        "home/index.jinja2",
        title="Wobble Home Page",
        subtitle="Wobble Subtitle",
        template="home-template",
    )
    #return render_template("home/home.html")


@sock.route('/reverse', bp=home)
def reverse(ws):
    """WebSocket example which reverses text strings received."""
    while True:
        s = ws.receive()
        ws.send(s[::-1])


@sock.route('/echo', bp=home)
def echo(ws):
    """WebSocket example which echos text strings received."""
    while True:
        s = ws.receive()
        ws.send(s)
