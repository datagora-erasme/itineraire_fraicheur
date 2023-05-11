from flask import Flask, request, jsonify
from flask_cors import CORS
from models.data import *
from load_network import *
from models.itinerary import *

app = Flask(__name__)
CORS(app)

network_path = "./data/osm/final_network.gpkg"
network_pickle_path = "./data/pickle_network.pickle"

G = None

print("loading network ...")
load_net = load_network(network_path, network_pickle_path)
if(load_net):
    print("Network loaded")
    G = load_graph_from_pickle(network_pickle_path)

@app.route('/')
def hello_worl():
    return "Hello, World"

@app.route('/data/', methods=['GET'])
def get_layers():
    layer_id = request.args.get('id')
    print("request", request)
    if layer_id:
        try:
            print("one layer")
            data = findOne(layer_id)
            if not data:
                return '', 404
            return jsonify(data)
        except Exception as e:
            print(e)
            return '', 500
    else:
        try:
            results = findMany()
            return jsonify(results)
        except Exception as e:
            print(e)
            return '', 500

@app.route('/itinerary/', methods=['GET'])
def get_itinerary():
    start_lat = request.args.get("start[lat]")
    start_lon = request.args.get("start[lon]")
    end_lat = request.args.get("end[lat]")
    end_lon = request.args.get("end[lon]")

    start = (float(start_lon), float(start_lat))
    end = (float(end_lon), float(end_lat))

    print(start_lat, start_lon, end_lat, end_lon)
    try:
        print(start, end)
        geojson_path = shortest_path(G, start, end)
        # print(geojson_path)
        results = [{
            "geojson": geojson_path, 
            "color": "blue"
        }]
        print(results)
        return jsonify(results)
    except Exception as e:
        print(e)
        return '', 500



if __name__ == "__main__":
    app.config["extra_files"] = [
        "./data/pickle_network.pickle"
    ]
    app.run(debug=True, host="localhost", port=3002)