"""Flask Hello World App"""

import yaml

from flask_sock import Sock
from flask import Flask

app = Flask(__name__)
sock = Sock(app)
#app.logger.setLevel(logging.DEBUG)


@app.route('/')
def hello_world():
    """Root page."""
    app.logger.debug("hello_world")
    return 'Hello, World! - modified version'


@sock.route('/reverse')
def reverse(ws):
    """WebSocket example which reverses text strings received."""
    while True:
        s = ws.receive()
        ws.send(s[::-1])


@sock.route('/echo')
def echo(ws):
    """WebSocket example which echos text strings received."""
    while True:
        s = ws.receive()
        ws.send(s)


if __name__ == "__main__":
    app.run()
