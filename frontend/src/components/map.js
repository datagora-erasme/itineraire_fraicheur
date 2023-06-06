
import React, { useContext, useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, GeoJSON, ZoomControl, useMap } from 'react-leaflet'
import axios from "axios"
import L, { marker } from 'leaflet'
import MarkerClusterGroup from '@changey/react-leaflet-markercluster';
import { FaGofore, FaRoute } from 'react-icons/fa';
import MainContext from '../contexts/mainContext';
import chroma from "chroma-js"


// All of the following const should be send by the backend 

// const sp = require("../data/sp_IF_3946.json");
// const if_joined = require("../data/joined_if_3946.json");

// const network= require("../data/final_network.json")

const colors = {
    "1":" #d6e4d7 ",
    "0.8": "#b6e4ba",
    "0.6": "#83bd88",
    "0.4": "#588e5d",
    "0.2": "#4d8652",
    "0.01": "#28572c"
}

const colorIfScale = chroma.scale(["#1f8b2c", "#900C3F"]).domain([0.9,1])

function MapFreshness({setZoomToUserPosition, zoomToUserPosition, radius, selectedStartAddress, showCircle, freshnessLayers, setFilteredFeatures}){
    const map = useMap()

    if(selectedStartAddress && showCircle){
        const coordinates = [selectedStartAddress.geometry.coordinates[1], selectedStartAddress.geometry.coordinates[0]]
        map.eachLayer((layer) => {
            if (layer.options && (layer.options.id === "freshnessAroundUser" || layer.options.id === "userPosition")) {
              map.removeLayer(layer);
            }
          });

        const circle = L.circle(coordinates, {
            id:"freshnessAroundUser",
            radius: radius*1000,
            color: 'green',
        }).addTo(map);

        /*eslint-disable*/
        let marker = L.marker(coordinates, {
            id:"userPosition"
        }).addTo(map)

        // const userPosition = L.Marker(position)
        // userPosition.addTo(map)
      
        // zoom to circle
        if(zoomToUserPosition){
            map.fitBounds(circle.getBounds());
            setZoomToUserPosition(false)
        }


    } else if (!showCircle){
        map.eachLayer((layer) => {
            if (layer.options && (layer.options.id === "freshnessAroundUser" || layer.options.id === "userPosition")) {
              map.removeLayer(layer);
            }
          });
    }
    return null
}

function ZoomItinerary({zoomToItinerary, setZoomToItinerary, currentItinerary}){
    const map = useMap()
    if(currentItinerary && currentItinerary.length !== 0 && zoomToItinerary){
        const geojsonData = currentItinerary[0].geojson
        const layer = L.geoJSON(geojsonData)
        const bounds = layer.getBounds()
        const centroid = bounds.getCenter()

        map.setView(centroid, 15)
        map.removeLayer(layer)

        setZoomToItinerary(false)

    }
}


function Map(){

    const [geojsonFiles, setGeojsonFiles] = useState([])
    const [loadingLayer, setLoadingLayer] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const [filteredFeatures ,setFilteredFeatures] = useState([])

    const { userPosition, zoomToUserPosition, setZoomToUserPosition, selectedLayers, 
        currentItinerary, setCurrentItinerary, selectedStartAddress, selectedEndAddress, radius, showCircle,
        zoomToItinerary, setZoomToItinerary,freshnessLayers, setShowPoiDetails, setHistory, history, setShowFindFreshness,
        setPoiDetails
     } = useContext(MainContext)

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
            color: "green",
            fillColor: "green", 
            fillOpacity: 0.5, 
            opacity: 0.5
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
            url: "/itinerary/",
            params: {
                start: {
                    lat: userPosition[0], 
                    lon: userPosition[1]
                },
                end: {
                    lat : coordinates[0],
                    lon : coordinates[1]
                }
            }
        }).then((response) => {
            setCurrentItinerary(response.data)
            setIsLoading(false)
        }).catch((error) => {
            console.error(error)
        })
    }

    const handleShowDetailsPopupPolygon = (e) => {
        setPoiDetails(e.target.feature)
        setShowFindFreshness(false)
        setShowPoiDetails(true)
        setHistory([...history, {fn: () => {
            setShowPoiDetails(false)
            setShowFindFreshness(true)
          }}])
    }

    const showDetailsPopupPolygon = (feature, layer) => {
        layer.on({
            click: handleShowDetailsPopupPolygon
        })
    }

    const handleShowDetailsPopupMarker = (informations) => {
        console.log(informations)
        setPoiDetails(informations)
        setShowFindFreshness(false)
        setShowPoiDetails(true)
        setHistory([...history, {fn: () => {
            setShowPoiDetails(false)
            setShowFindFreshness(true)
          }}])
    }

    useEffect(() => {
        if(selectedStartAddress && showCircle){
            const coordinates = [selectedStartAddress.geometry.coordinates[1], selectedStartAddress.geometry.coordinates[0]]
            const newfilteredLayers = freshnessLayers.map((layer) => {
                // console.log("layer : ", layer)
                const filteredlayer = layer.geojson.features.filter((feature) => {
                    // console.log("feature into filter : ", feature)
                    let lat;
                    let lng;
                    if(feature.geometry.type === "Polygon" || feature.geometry.type === "MultiPolygon"){
                        // console.log("ok")
                        const layer = L.geoJSON(feature)
                        const bounds = layer.getBounds()
                        const centroid = bounds.getCenter()
                        lat = centroid.lat
                        lng = centroid.lng
                    } else {
                        lat = feature.geometry.coordinates[1]
                        lng = feature.geometry.coordinates[0]
                    }
                    
                    const distance = L.latLng(lat, lng).distanceTo(L.latLng(coordinates))
        
                    return distance < radius * 1000
                })
                // console.log("filteredlayer: ", filteredlayer)

                // console.log("filteredLayer : ", filteredlayer)

                return filteredlayer
            })
            setFilteredFeatures(newfilteredLayers)
        } else {
            setFilteredFeatures([])
        }

    }, [selectedStartAddress, showCircle, radius])

    return (
        <div>
            {loadingLayer && "Loading ...."}
            <MapContainer id="map" center={[45.76309302427536, 4.836502750843036]} zoom={13} scrollWheelZoom={true} className="mapContainer" zoomControl={false}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    // url="http://{s}.tile.openstreetmap.fr/openriverboatmap/{z}/{x}/{y}.png"
                    url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                    // url="https://openmaptiles.data.grandlyon.com/data/v3/{z}/{x}/{y}.pbf"
                />
                <ZoomControl position='topright' />
                <MapFreshness 
                    zoomToUserPosition={zoomToUserPosition} 
                    radius={radius} 
                    setZoomToUserPosition={setZoomToUserPosition} 
                    selectedStartAddress={selectedStartAddress} 
                    showCircle={showCircle} 
                    freshnessLayers={freshnessLayers}
                    setFilteredFeatures={setFilteredFeatures}
                    />
                <ZoomItinerary zoomToItinerary={zoomToItinerary} setZoomToItinerary={setZoomToItinerary} currentItinerary={currentItinerary}/>

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
                                                                Informations
                                                            </div>
                                                        </Popup>
                                                    </Marker>
                                                )
                                            })}
                                        </MarkerClusterGroup>
                                )
                            } else if (dataType === "MultiPolygon" || dataType === "Polygon"){
                                return(
                                    <GeoJSON data={data.geojson} style={getColor} key={Math.random()} />
                                )
                            } 
                            // else if (dataType === "Polygon"){
                            //     return(
                            //         <>
                            //             {data.geojson.features.map((polygon, index) => {
                            //                 return(
                            //                     <Polygon key={index} positions={polygon.geometry.coordinates} color='green'>

                            //                     </Polygon>
                            //                 )
                            //             })}
                            //         </>
                            //     )
                            // }
                        }
                        return null
                    })
                }

                {/* <GeoJSON data={network} key={Math.random()}/> */}

                {currentItinerary && 
                    currentItinerary.map((it, index) => {
                        return(
                            <GeoJSON 
                            data={it.geojson} 
                            style={(feature) => ({
                                color: colorIfScale(feature.properties.IF).hex(), 
                                weight: 5, 
                                lineCap: "round", 
                                lineJoin: "round",
                                dashArray: it.id === "LENGTH" ? '5, 15' : '', 
                                dashOffset: '0'
                                })} 
                            key={Math.random()}/>
                        )
                    })
                }
                { selectedStartAddress &&
                    <Marker position={[selectedStartAddress.geometry.coordinates[1], selectedStartAddress.geometry.coordinates[0]]}></Marker>
                }
                {
                    selectedEndAddress &&
                    <Marker position={[selectedEndAddress.geometry.coordinates[1], selectedEndAddress.geometry.coordinates[0]]}></Marker>
                }


                {filteredFeatures.length !== 0 && filteredFeatures.map((data) => {
                    if(data.length !== 0){
                        // console.log("ddddddata: ", data)
                        const dataType = data[0].geometry.type
                        if(dataType === "MultiPolygon" || dataType === "Polygon"){
                            return(
                                <GeoJSON key={Math.random()} data={data} style={getColor} onEachFeature={showDetailsPopupPolygon}/>
                            )
                        } else if (dataType === "Point"){
                            const markerOption = data[0].properties.markerOption
                            return(
                                <MarkerClusterGroup 
                                key={Math.random()} 
                                maxClusterRadius={100}
                                polygonOptions={{
                                    opacity: 0
                                }}
                                iconCreateFunction={(cluster) => createClusterCustomIcon(cluster, markerOption)}
                                // eventHandlers={{
                                //     click: (cluster) => handleShowDetailsPopupMarker(cluster.sourceTarget)
                                // }}
                                >
                                {data.map((dta,i) => {
                                    // console.log(dta)
                                    const coordinates = [dta.geometry.coordinates[1], dta.geometry.coordinates[0]]
                                    return (
                                        <Marker key={Math.random()} position={coordinates} icon={new L.icon(markerOption)} eventHandlers={{
                                            click: () => handleShowDetailsPopupMarker(dta)
                                        }}>

                                        </Marker>
                                    )
                                })}
                                </MarkerClusterGroup>
                            )
                        }
                    }
                })}
            </MapContainer>

        </div>
    
    );
}

export default Map; 