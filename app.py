from flask import Flask, send_from_directory
import os

app = Flask(__name__)

@app.route('/')
def homepage():
    return send_from_directory('.', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
