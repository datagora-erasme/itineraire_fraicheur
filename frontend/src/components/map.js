
import React, { useContext, useEffect, useState } from 'react';
import { MapContainer, TileLayer, Marker, Popup, GeoJSON, ZoomControl, useMap, Polygon } from 'react-leaflet'
import axios from "axios"
import L from 'leaflet'
import { lineString, buffer, featureCollection, dissolve, booleanPointInPolygon, difference, polygon, circle} from "@turf/turf"
import MarkerClusterGroup from '@changey/react-leaflet-markercluster';
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

const colorIfScale = chroma.scale(["#f42a2d", "#3d83f5"]).domain([0,10])

function MapFreshness({setZoomToUserPosition, zoomToUserPosition, radius, selectedStartAddress, showCircle}){
    const map = useMap()

    if(selectedStartAddress && showCircle){
        const coordinates = [selectedStartAddress.geometry.coordinates[1], selectedStartAddress.geometry.coordinates[0]]
        map.eachLayer((layer) => {
            if (layer.options && (layer.options.id === "freshnessAroundUser" || layer.options.id === "userPosition" || layer.options.id === "doughnuts")) {
              map.removeLayer(layer);
            }
          });

        const littleCircle = circle([coordinates[1], coordinates[0]], radius=radius)
        const bigCircle = circle([coordinates[1], coordinates[0]], radius=1000)

        const doughnuts = difference(bigCircle, littleCircle)

        const mapLittleCircle = L.geoJSON(littleCircle, {
            id: "freshnessAroundUser",
            color: "white"
        })

        const mapDoughnuts = L.geoJSON(doughnuts, {
            id: "doughnuts",
            color: "gray",
            fillOpacity: 0.5
        })

        mapLittleCircle.addTo(map)
        mapDoughnuts.addTo(map)

        /*eslint-disable*/
        let marker = L.marker(coordinates, {
            id:"userPosition"
        }).addTo(map)

        // const userPosition = L.Marker(position)
        // userPosition.addTo(map)
      
        // zoom to circle
        if(zoomToUserPosition){
            map.fitBounds(mapLittleCircle.getBounds());
            setZoomToUserPosition(false)
        }


    } else if (!showCircle){
        map.eachLayer((layer) => {
            if (layer.options && (layer.options.id === "freshnessAroundUser" || layer.options.id === "userPosition" || layer.options.id === "doughnuts")) {
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
        // const centroid = bounds.getCenter()
        map.fitBounds(bounds)

        // map.setView(centroid, 15)
        map.removeLayer(layer)

        setZoomToItinerary(false)

    }
}


function Map(){

    const [geojsonFiles, setGeojsonFiles] = useState([])
    const [loadingLayer, setLoadingLayer] = useState(false)
    const [isLoading, setIsLoading] = useState(false)
    const [bufferedItineraries, setBufferedItineraries] = useState([])

    const { userPosition, zoomToUserPosition, setZoomToUserPosition, selectedLayers, 
        currentItinerary, setCurrentItinerary, selectedStartAddress, selectedEndAddress, radius, showCircle,
        zoomToItinerary, setZoomToItinerary,freshnessLayers, setShowPoiDetails, setHistory, history, setShowFindFreshness,
        setPoiDetails, layers, filteredFreshnessFeatures, setFilteredFreshnessFeatures, filteredItinerariesFeatures,
        setFilteredItinerariesFeatures
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

        //<span style=${markerOption.clusterCountStyle}>${cluster.getChildCount()}</span>

        return L.divIcon({
            html: `<span class="flex flex-col items-center justify-center">
                        <img src=${markerOption.iconUrl} style="display: block, width: 40px; height:40px;" />
                        <span class="text-bgWhite bg-mainText w-2/3 h-4 rounded-sm font-bold">${cluster.getChildCount()}</span>
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
        // console.log(informations)
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
                    } 
                    else {
                        lat = feature.geometry.coordinates[1]
                        lng = feature.geometry.coordinates[0]
                    }

                    if(lat && lng){
                        const distance = L.latLng(lat, lng).distanceTo(L.latLng(coordinates))
        
                        return distance < radius * 1000
                    }
                    return false
                })
                // console.log("filteredlayer: ", filteredlayer)

                // console.log("filteredLayer : ", filteredlayer)

                return filteredlayer
            })
            setFilteredFreshnessFeatures(newfilteredLayers)
        } else {
            setFilteredFreshnessFeatures([])
        }

    }, [selectedStartAddress, showCircle, radius])

    useEffect(() => {
        setBufferedItineraries([])
        if(currentItinerary && currentItinerary.length !== 0){
            for(let it of currentItinerary){
                const geojsonLayer = L.geoJSON(it.geojson)
                const bufferedFeatures = geojsonLayer.toGeoJSON().features.map((feature) => {
                    if (feature.geometry.type === 'LineString') {
                      const line = lineString(feature.geometry.coordinates);
                      const bufferedLine = buffer(line, 100, { units: 'meters' });
                      return bufferedLine;
                    }
                    return feature;
                  });
                
                const dissolvedFeature = {...dissolve(featureCollection(bufferedFeatures)), id: it.id}
                // console.log(geojsonLayer)
                // console.log("bufferedFeatures: ", bufferedFeatures)
                
                setBufferedItineraries((prevBufferedItineraries) => [...prevBufferedItineraries, dissolvedFeature])
            }
        }
    }, [currentItinerary])

    // console.log("current : ", currentItinerary)

    useEffect(() => {
        setFilteredItinerariesFeatures([])
        if(bufferedItineraries.length !== 0 && layers.length !== 0){
            const newFiltereditinerariesFeatures = layers.map((layer,i) => {
                // console.log("layer : ", layer)
                const filteredLayer = layer.geojson.features.filter((feat) => {
                    let point;
                    if(feat.geometry.type === "Point"){
                        point = feat.geometry.coordinates
                    } else if (feat.geometry.type === "Polygon" || feat.geometry.type === "MultiPolygon"){
                        const layer = L.geoJSON(feat)
                        const bounds = layer.getBounds()
                        const centroid = bounds.getCenter()
                        point = [centroid.lat, centroid.lng]
                    }
                    // console.log("bufferd : ", bufferedItineraries)
                    for(let bufferedIt of bufferedItineraries){
                        if(bufferedIt.id === "IF" && booleanPointInPolygon(point, bufferedIt.features[0])){
                            return true
                        }
                    }
                    return false
                })
                return {
                    id: layer.id,
                    geojson: filteredLayer,
                    markerOption: layer.markerOption
                }
            })
            setFilteredItinerariesFeatures(newFiltereditinerariesFeatures)
        }
    }, [bufferedItineraries])

    return (
        <div>
            {loadingLayer && "Loading ...."}
            <MapContainer id="map" center={[45.76309302427536, 4.836502750843036]} zoom={13} scrollWheelZoom={true} className="mapContainer" zoomControl={false}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    // url="http://{s}.tile.openstreetmap.fr/openriverboatmap/{z}/{x}/{y}.png"
                    // url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"
                    url="https://openmaptiles.data.grandlyon.com/styles/klokantech-basic/{z}/{x}/{y}.png"

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
                    setFilteredFreshnessFeatures={setFilteredFreshnessFeatures}
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
                                color: colorIfScale(feature.properties.freshness_score).hex(), 
                                weight: it.id === "LENGTH" ? 5 : 10, 
                                lineCap: "round", 
                                lineJoin: "round",
                                dashArray: it.id === "LENGTH" ? '1, 10' : '', 
                                dashOffset: '0'
                                })} 
                            key={Math.random()}/>
                        )
                    })
                }

                {bufferedItineraries.length !== 0 &&
                    bufferedItineraries.map((it, index) => {
                        // console.log(it)
                        if(it.id ==="IF"){
                            return(
                                <GeoJSON data={it} key={Math.random()} style={{
                                    color: "rgba(128, 128, 128, 0.2)",
                                    fillColor: "rgba(128, 128, 128, 1)",
                                    // fillOpacity: 0.2
                                }}/>
                            )
                        }
                    })
                }

                { selectedStartAddress &&
                    <Marker position={[selectedStartAddress.geometry.coordinates[1], selectedStartAddress.geometry.coordinates[0]]}></Marker>
                }
                {
                    selectedEndAddress &&
                    <Marker position={[selectedEndAddress.geometry.coordinates[1], selectedEndAddress.geometry.coordinates[0]]}></Marker>
                }


                {filteredFreshnessFeatures.length !== 0 && filteredFreshnessFeatures.map((data) => {
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
                {filteredItinerariesFeatures.length !== 0 && filteredItinerariesFeatures.map((data) => {
                    if(data.geojson.length !== 0){
                        // console.log("ddddddata: ", data)
                        const dataType = data.geojson[0].geometry.type
                        if(dataType === "MultiPolygon" || dataType === "Polygon"){
                            return(
                                <GeoJSON key={Math.random()} data={data.geojson} style={getColor} onEachFeature={showDetailsPopupPolygon}/>
                            )
                        } else if (dataType === "Point"){
                            const markerOption = data.markerOption
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
                                {data.geojson.map((dta,i) => {
                                    // console.log(dta)
                                    const coordinates = [dta.geometry.coordinates[1], dta.geometry.coordinates[0]]
                                    return (
                                        <Marker key={Math.random()} position={coordinates} icon={new L.icon(markerOption)}>

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