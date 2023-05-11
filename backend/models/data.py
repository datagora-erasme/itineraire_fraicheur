import json
import os

with open('./data/data_informations.json') as f:
    data_informations = json.load(f)

def get_layer_list():
    layers_list = []
    raw_data = data_informations['data_raw']
    wfs_data = data_informations['data_wfs']

    for data_id, data in raw_data.items():
        layers_list.append({
            'id': data_id,
            **data
        })

    for data_id, data in wfs_data.items():
        layers_list.append({
            'id': data_id,
            **data
        })

    return layers_list

def findMany():
    return get_layer_list()

def findOne(id):
    layer_list = get_layer_list()
    print(f'fetching geojson: {id}')

    for data in layer_list:
        if data['id'] == id:
            path = data['geojson_path']
            print(path)
            with open(path) as f:
                geojson = json.load(f)

            markerOption = data['marker_option']
            return {
                'geojson': geojson,
                'markerOption': markerOption,
                'id': id
            }

    return None
