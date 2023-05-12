
import React, {useState, useEffect} from 'react';
import Map from '../components/map'

import axios from 'axios'
import Content from '../components/content';

function Home(){
    const [listLayers, setListLayers] = useState([])
    const [selectedLayers, setSelectedLayers] = useState([])
    const [currentItinerary, setCurrentItinerary] = useState(null)

    const [isLayerLoading, setIsLayerLoading] = useState(false)

    const [userPosition, setUserPosition] = useState(null)
    const [zoomToUserPosition, setZoomToUserPosition] = useState(false)

    useEffect(() => {
        async function fetchListLayers(){
            try{
                const response = await axios({
                    method:'get',
                    baseURL: `${process.env.REACT_APP_URL_SERVER}`,
                    url: "/data/",
                })
                setListLayers(response.data) 
            } catch (error){
                console.error(error)
            } 
        }
        setIsLayerLoading(true)
        fetchListLayers()
        setIsLayerLoading(false)
    }, [])

    useEffect(() => {
        // Get user's current position using geolocation API
        navigator.geolocation.getCurrentPosition(
          (pos) => {
            const { latitude, longitude } = pos.coords;
            setUserPosition([latitude, longitude]);
          },
          (err) => {
            console.log(err);
          }
        );
      }, []);

    return (
        <div style={{position: 'relative'}}>
            <Content 
                selectedLayers={selectedLayers} 
                listLayers={listLayers} 
                setCurrentItinerary={setCurrentItinerary} 
                setSelectedLayers={setSelectedLayers} 
                isLayerLoading={isLayerLoading} 
                position={userPosition} 
                zoomToUserPosition={zoomToUserPosition}
                setZoomToUserPosition={setZoomToUserPosition}
            />
            <Map 
                selectedLayers={selectedLayers} 
                currentItinerary={currentItinerary} 
                zoomToUserPosition={zoomToUserPosition} 
                position={userPosition} 
                setZoomToUserPosition={setZoomToUserPosition}
                setCurrentItinerary={setCurrentItinerary}
            />
        
        </div>
    );
}

export default Home; 