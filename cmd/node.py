from flask import Flask, request
import argparse
import requests
import dbm

app = Flask(__name__)

@app.route("/write", methods=['POST'])
def write():
    for k in request.form.keys():
        with dbm.open(f'.{args.port}-dbm', 'c') as store:
            store[k] = request.form[k]
    return ({'message': f'Added value for key {k}'}, 201)

@app.route("/read", methods=['GET'])
def read():
    if k := request.args.get('key', None):
        with dbm.open(f'.{args.port}-dbm', 'r') as store:
            if k in store:
                return {k: store[k].decode('utf8')}, 200
        return ({'message': 'Key does not exist in store.'}, 404)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="port to run the node process on", default=5201)
    parser.add_argument("-c", "--coordinator", help="port of the coordinator process", default=5200)

    with app.app_context():
        args = parser.parse_args()
        chain_info = requests.post(f'http://127.0.0.1:{args.coordinator}/addNode', data= {'host': args.port}).json()
        app.run(port=args.port, debug=True)