from flask import Flask, make_response

app = Flask(__name__)

@app.route("/hello")
def hello():
    headers = {
        'content-type': 'text/plain',
        # 'content-type': 'application/json',
    }

    response = make_response('<html></html>')
    response.headers = headers
    # return '<html></html>', 404, headers
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8899, debug=True)
