const fs = require("fs")

const data_informations = JSON.parse(fs.readFileSync("./script_python/data_informations.json"));

function get_layer_list(){
    const layers_list = [];
    const raw_data = data_informations["raw_data"]
    const wfs_data = data_informations["data_wfs"]

    for(let data_id in raw_data){
        layers_list.push({
            id: data_id, 
            ...raw_data[data_id]
        })
    }
    for(let data_id in wfs_data){
        layers_list.push({
            id: data_id,
            ...wfs_data[data_id]
        })
    }

    return layers_list
}



module.exports.findMany = () => {
   return get_layer_list()
}

module.exports.findOne = (id) => {
    const layer_list = get_layer_list()

    console.log('fetching geojson : ' + id)

    for(let data of layer_list){
        if(data["id"] === id){
            const path = data["geojson_path"]
            const geojson = JSON.parse(fs.readFileSync(path))
            const markerOption = data["marker_option"]
        
            return {
                geojson,
                markerOption,
                id
            }
        }
    }

    return null
}