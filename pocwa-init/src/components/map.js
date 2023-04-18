
import React from 'react';
import { MapContainer, TileLayer, useMap, Marker, Popup } from 'react-leaflet'

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
            </MapContainer>

        </div>
    
    );
}

export default Map; 