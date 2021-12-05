from flask import Flask, request
import argparse
import requests

app = Flask(__name__)

@app.route("/addNode", methods=['POST'])
def addNode():
    if port := request.form.get('host', None):
        if port not in nodes:
            nodes.append(port)
            app.logger.debug(f'Added host %s to chain. Chain: %s', str(port), " -> ".join(nodes))
        return ({
            'previous_node': nodes[-2] if len(nodes) > 1 else '', 
            'next_node': ''}, 201)
    return ({'message': 'Must POST with a form {"host": host} to be added to the chain'}, 400)

@app.route("/write", methods=['POST'])
def write():
    with app.app_context():
        if len(nodes) == 0:
            return ({'message': 'no nodes have been connected to the coordinator'}, 400)
    requests.post(f'http://127.0.0.1:{nodes[0]}/write', data=request.form)
    return (requests.post(f'http://127.0.0.1:{nodes[0]}/write', data=request.form).json(), 201)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="port to run the coordinator process on", default=5200)
    args = parser.parse_args()
    with app.app_context():
        nodes = []
    app.run(port=args.port, debug=True)