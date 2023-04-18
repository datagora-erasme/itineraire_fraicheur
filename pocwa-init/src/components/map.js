
import React from 'react';
import { MapContainer, TileLayer, useMap, Marker, Popup, GeoJSON } from 'react-leaflet'

// All of the following const should be send by the backend 

const sp = require("../data/sp_IF_3946.json");
const if_joined = require("../data/joined_if_3946.json");
const colors = {
    "1":" #d6e4d7 ",
    "0.8": "#b6e4ba",
    "0.6": "#83bd88",
    "0.4": "#588e5d",
    "0.2": "#4d8652",
    "0.01": "#28572c"
}


function Map(){

    function getColor(data){
        const value = data.properties.IF
        return {
            color: colors[value.toString()],
            fillColor: colors[value.toString()],
            opacity:1,
            fillOpacity: 1
        }
    }

    return (
        <div>
            <MapContainer center={[45.76309302427536, 4.836502750843036]} zoom={13} scrollWheelZoom={false} className="mapContainer">
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                <Marker position={[45.76309302427536, 4.836502750843036]}>
                    <Popup>
                    A pretty CSS3 popup. <br /> Easily customizable.
                    </Popup>
                </Marker>
                <GeoJSON data={sp} style={{color: "red"}}/>
                <GeoJSON data={if_joined} style={getColor}/>
            </MapContainer>

        </div>
    
    );
}

export default Map; 