from flask import Flask, render_template,Response,jsonify,request
from Database.database import createHistory,readHistory
app = Flask(__name__)


# GET request handler
@app.route('/', methods=['GET'])
def test():
    return jsonify({"message":"Hello Friends"})


# CREATE a new HIstory
@app.route('/createHistory', methods=['POST'])
def CREATE():
    result = createHistory(
                            images=request.json['images'], 
                            name=request.json['name'], 
                            time_in=request.json['time_in'], 
                            date=request.json['date']
                        )
    return jsonify({ "message":result})

# READ from a HIstory
@app.route('/readHistory', methods=['GET'])
def READ():
    result = readHistory()
    return jsonify(result)



if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        debug=True,
        port=4000)