import asyncio
from flask import Flask
from run import log_current_power

table_headers = ['Timestamp (UTC)',
                 'Solar (W)',
                 'Load (W)',
                 'Grid consumption (W)',
                 'Battery discharge (W)',
                 'Battery status',
                 'Grid status',
                 'Battery charge (%)']
app = Flask(__name__)


@app.route('/alphaess')
def run_script():
    current_power = asyncio.run(log_current_power())
    txt = '<br>'.join([f'{table_headers[i]}: {p}' for i, p in enumerate(current_power)])
    return txt


if __name__ == '__main__':
    app.run()
