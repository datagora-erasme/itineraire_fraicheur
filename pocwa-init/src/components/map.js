
import React, { useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, GeoJSON, ZoomControl } from 'react-leaflet'
import axios from "axios"
import L from 'leaflet'
import MarkerClusterGroup from '@changey/react-leaflet-markercluster';

const drop = "droplet-solid.svg"


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


function Map({selectedLayers, currentItinerary}){

    const [geojsonFiles, setGeojsonFiles] = useState([])
    const [loadingLayer, setLoadingLayer] = useState(false)

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
                const response = await axios.get("http://localhost:3002/data/", {
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
    }, [selectedLayers])

    // if (!geojsonFile) {
    //     return <p>Loading GeoJSON...</p>;
    //   }

    // console.log(geojsonFiles)
    const createClusterCustomIcon = function (cluster, markerOption) {
        console.log(markerOption.clusterCountStyle)
        return L.divIcon({
            html: `<span style="position: relative; width:25px; height:25px;">
                        <img src=${markerOption.iconUrl} style="display: block, width: 40px; height:40px;" />
                        <span style=${markerOption.clusterCountStyle}>${cluster.getChildCount()}</span>
                    </span>`,
            className: 'custom-marker-cluster',
            iconSize: L.point(33, 33, true),
        })
    }
    return (
        <div>
            {loadingLayer && "Loading ...."}
            <MapContainer center={[45.76309302427536, 4.836502750843036]} zoom={13} scrollWheelZoom={false} className="mapContainer" zoomControl={false}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <ZoomControl position='topright' />
                {/* <Marker position={[45.76309302427536, 4.836502750843036]}>
                    <Popup>
                    A pretty CSS3 popup. <br /> Easily customizable.
                    </Popup>
                </Marker> */}
                {/* <GeoJSON data={sp} style={{color: "red"}}/> */}
                {geojsonFiles.length !== 0 && 
                    geojsonFiles.map((data) => { 
                        if(selectedLayers.includes(data.id)) {
                            const dataType = data.geojson.features[0].geometry.type
                            const markerOption = data.markerOption
                            if(dataType == "Point"){
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
                                                    <Marker key={index} position={[coordinates[1], coordinates[0]]} icon={new L.icon(markerOption)}></Marker>
                                                )
                                            })}
                                        </MarkerClusterGroup>
                                )
                            } else if (dataType == "MultiPolygon"){
                                return(
                                    <GeoJSON data={data.geojson} style={getColor} key={Math.random()} />
                                )
                            }

                        }
                    })
                }
                {/* <GeoJSON data={geojsonFile} style={getColor}/> */}
                {currentItinerary && <GeoJSON data={currentItinerary} style={{color: "blue"}} key={Math.random()}/>}
            </MapContainer>

        </div>
    
    );
}

export default Map; 