from flask import Flask, render_template,Response,jsonify

app = Flask(__name__)


# GET request handler
@app.route('/', methods=['GET'])
def test():
    return jsonify("Hello Friend")

if __name__ == '__main__':
    app.run()

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=5000)