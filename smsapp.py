from flask import Flask, request
import logging
from flask import Flask

app = Flask(__name__)
app.debug = True

app = Flask(__name__)
logging.basicConfig(filename='logs/sms.log', level=logging.INFO)

@app.route('/sms', methods=['POST'])
def sms():
    to = request.json['to']
    body = request.json['body']
    logging.info(f"Sending SMS to {to}: {body}")
    return "SMS Sent!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8081)