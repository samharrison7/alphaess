import asyncio
from flask import Flask
from run import log_current_power

app = Flask(__name__)


@app.route('/run')
def run_script():
    current_power = asyncio.run(log_current_power())
    return current_power


if __name__ == '__main__':
    app.run()
