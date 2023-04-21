import React from 'react'
import ListLayers from './listLayers'
import SelectAddress from './selectAdress'

function Content({setCurrentItinerary, listLayers, selectedLayers, setSelectedLayers, isLayerLoading}){
    return(
        <div style={{ position: 'absolute', top: 20, left: 20, zIndex:1000}} className="bg-white bg-opacity-70 rounded-lg shadow-md p-4">
            <SelectAddress setCurrentItinerary={setCurrentItinerary}/>
            {listLayers.length !== 0 ? <ListLayers listLayers={listLayers} selectedLayers={selectedLayers} setSelectedLayers={setSelectedLayers} isLayerLoading={isLayerLoading}/> : "loading ..."}
        </div>
    )
}

export default Content