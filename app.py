from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'message': 'Annotate server v0.0.1', 
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)