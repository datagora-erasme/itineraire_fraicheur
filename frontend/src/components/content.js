import React from 'react'
import ListLayers from './listLayers'
import SelectAddress from './selectAdress'
import FreshnessAroundUser from './freshnessAroundUser'

function Content({setCurrentItinerary, listLayers, selectedLayers, setSelectedLayers, isLayerLoading, position, zoomToUserPosition, setZoomToUserPosition}){
    return(
        <div style={{ position: 'absolute', top: 20, left: 20, zIndex:1000}} className="bg-white bg-opacity-70 rounded-lg shadow-md p-4">
            <SelectAddress setCurrentItinerary={setCurrentItinerary}/>
            <FreshnessAroundUser position={position} zoomToUserPosition={zoomToUserPosition} setZoomToUserPosition={setZoomToUserPosition}/>
            {listLayers.length !== 0 ? <ListLayers listLayers={listLayers} selectedLayers={selectedLayers} setSelectedLayers={setSelectedLayers} isLayerLoading={isLayerLoading}/> : "loading ..."}
            <div className='mt-2 cursor-pointer'><a target="_blank" rel="noopener noreferrer" href='https://datagora.erasme.org/projets/sortons-au-frais/'>En savoir plus</a></div>
        </div>
    )
}

export default Content