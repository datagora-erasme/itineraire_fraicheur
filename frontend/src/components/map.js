
import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, GeoJSON, ZoomControl, useMap } from 'react-leaflet'
import axios from "axios"
import L from 'leaflet'
import MarkerClusterGroup from '@changey/react-leaflet-markercluster';
import { FaRoute } from 'react-icons/fa';


// All of the following const should be send by the backend 

// const sp = require("../data/sp_IF_3946.json");
// const if_joined = require("../data/joined_if_3946.json");
const colors = {
    "1":" #d6e4d7 ",
    "0.8": "#b6e4ba",
    "0.6": "#83bd88",
    "0.4": "#588e5d",
    "0.2": "#4d8652",
    "0.01": "#28572c"
}

function MapFreshness({setZoomToUserPosition, zoomToUserPosition, position}){
    const map = useMap()

    if(position && zoomToUserPosition){
        map.eachLayer((layer) => {
            if (layer.options && layer.options.color === 'green') {
              map.removeLayer(layer);
            }
          });

        const circle = L.circle(position, {
            radius: 500,
            color: 'green',
        }).addTo(map);

        L.marker(position).addTo(map)

        // const userPosition = L.Marker(position)
        // userPosition.addTo(map)
      
        // zoom to circle
        map.fitBounds(circle.getBounds());
        setZoomToUserPosition(false)
    }
    return null
}


function Map({selectedLayers, currentItinerary, setCurrentItinerary, zoomToUserPosition, setZoomToUserPosition, position}){

    const [geojsonFiles, setGeojsonFiles] = useState([])
    const [loadingLayer, setLoadingLayer] = useState(false)
    const [isLoading, setIsLoading] = useState(false)

    function getColor(data){
        // TODO : for each layer : specific style properties
        if(data.properties.IF){
            const value = data.properties.IF
            return {
                color: colors[value.toString()],
                fillColor: colors[value.toString()],
                opacity:1,
                fillOpacity: 1
            }
        }
        return {
            color: "red"
        }

    }

    useEffect(() => {
        async function fetchGeoJSON(id){
            setLoadingLayer(true)
            try {
                const response = await axios.get(`${process.env.REACT_APP_URL_SERVER}/data/`, {
                    params:{
                        id: id
                    }
                })
                const updatedGeojsonFiles = [...geojsonFiles, {...response.data}]
                setGeojsonFiles(updatedGeojsonFiles)
            } catch (error){
                console.error(error)
            }
            setLoadingLayer(false)
        }
        let existingGeojsonFilesId = []
        for(let file of geojsonFiles){
            existingGeojsonFilesId.push(file.id)
        }
        for(let id of selectedLayers){
            if(!existingGeojsonFilesId.includes(id)){
                fetchGeoJSON(id)
            }
        }
    }, [selectedLayers, geojsonFiles])

    const createClusterCustomIcon = function (cluster, markerOption) {

        return L.divIcon({
            html: `<span style="position: relative; width:25px; height:25px;">
                        <img src=${markerOption.iconUrl} style="display: block, width: 40px; height:40px;" />
                        <span style=${markerOption.clusterCountStyle}>${cluster.getChildCount()}</span>
                    </span>`,
            className: 'custom-marker-cluster',
            iconSize: L.point(33, 33, true),
        })
    }

    const handleClickMarker = (coordinates) => {
        setIsLoading(true)
        axios({
            method:'get',
            baseURL: `${process.env.REACT_APP_URL_SERVER}`,
            url: "/data/",
            params: {
                start: {
                    lat: position[0], 
                    lon: position[1]
                },
                end: {
                    lat : coordinates[1],
                    lon : coordinates[0]
                }
            }
        }).then((response) => {
            setCurrentItinerary(response.data)
            setIsLoading(false)
        }).catch((error) => {
            console.error(error)
        })
    }

    return (
        <div>
            {loadingLayer && "Loading ...."}
            <MapContainer id="map" center={[45.76309302427536, 4.836502750843036]} zoom={13} scrollWheelZoom={false} className="mapContainer" zoomControl={false}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    // url="http://{s}.tile.openstreetmap.fr/openriverboatmap/{z}/{x}/{y}.png"
                    url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                />
                <ZoomControl position='topright' />
                <MapFreshness zoomToUserPosition={zoomToUserPosition} position={position} setZoomToUserPosition={setZoomToUserPosition}/>

                {geojsonFiles.length !== 0 && 
                    geojsonFiles.map((data) => { 
                        if(selectedLayers.includes(data.id)) {
                            const dataType = data.geojson.features[0].geometry.type
                            const markerOption = data.markerOption
                            if(dataType === "Point"){
                                return(
                                        <MarkerClusterGroup 
                                            key={data.id} 
                                            maxClusterRadius={100}
                                            polygonOptions={{
                                                opacity: 0
                                            }}
                                            iconCreateFunction={(cluster) => createClusterCustomIcon(cluster, markerOption)}
                                            >
                                            {data.geojson.features.map((point, index) => {
                                                const coordinates = point.geometry.coordinates
                                                return(
                                                    <Marker key={index} position={[coordinates[1], coordinates[0]]} icon={new L.icon(markerOption)} onEachFeature={handleClickMarker}>
                                                        <Popup>
                                                            <div className="flex justify-center items-center">
                                                                <button onClick={() => handleClickMarker(coordinates)} 
                                                                className={"block px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition duration-300"}
                                                                >
                                                                {isLoading ? (
                                                                    <div className="flex items-center">
                                                                    <div className="w-6 h-6 rounded-full border-4 border-gray-300 border-t-blue-500 animate-spin mr-3"></div>
                                                                    <span>Loading...</span>
                                                                    </div>
                                                                ) : (
                                                                    <div className="flex items-center">
                                                                    <span className="mr-2">Itinéraire | </span>
                                                                    <FaRoute/>
                                                                    </div>
                                                                )}
                                                                </button>
                                                            </div>
                                                        </Popup>
                                                    </Marker>
                                                )
                                            })}
                                        </MarkerClusterGroup>
                                )
                            } else if (dataType === "MultiPolygon"){
                                return(
                                    <GeoJSON data={data.geojson} style={getColor} key={Math.random()} />
                                )
                            }
                        }
                        return null
                    })
                }

                {currentItinerary && 
                    currentItinerary.map((it) => {
                        return(
                            <GeoJSON data={it.geojson} style={{color: it.color}} key={Math.random()}/>
                        )
                    })
                }

            </MapContainer>

        </div>
    
    );
}

export default Map; 