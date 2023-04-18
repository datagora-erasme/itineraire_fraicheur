
import React from 'react';
import { MapContainer, TileLayer, useMap, Marker, Popup, GeoJSON } from 'react-leaflet'

const sp = require("../data/sp_IF_3946.json")


function Map(){
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
                <GeoJSON data={sp} style={{color:"red"}}/>
            </MapContainer>

        </div>
    
    );
}

export default Map; 