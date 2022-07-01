from flask import Flask

app_back = Flask(__name__)


def launch_backend():
    app_back.run(port=3000)


@app_back.route('/automatic/weekly')
def automatic_weekly():
    return 'yes'


@app_back.route('/automatic/xur')
def automatic_xur():
    return 'yes'


@app_back.route('/command/weekly')
def command_weekly():
    return 'yes'


@app_back.route('/command/xur')
def command_xur():
    return 'yes'


@app_back.route('/command/banshee')
def command_banshee():
    return 'yes'


@app_back.route('/command/player')
def command_player():
    return 'yes'