from flask import Flask
from flask import request
from flask_cors import CORS
from main import finviz_data_extractor
import json

app = Flask(__name__)
CORS(app)


@app.route('/ticker', methods=['POST'])
def data_extractor():
    if request.method == 'POST':
        ticker_json = request.get_json()
        if ticker_json:
            ticker_name = ticker_json['ticker']
            data_dict = finviz_data_extractor(ticker_name)
            return json.dumps(data_dict)
        else:
            return json.dumps({})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
