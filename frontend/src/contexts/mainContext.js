import React, {createContext, useState, useEffect} from "react"
import axios from 'axios'

const MainContext = createContext();

export const MainContextProvider = ({ children }) => {
    const [userPosition, setUserPosition] = useState(null)
    const [zoomToUserPosition, setZoomToUserPosition] = useState(false)

    const [listLayers, setListLayers] = useState([])
    const [selectedLayers, setSelectedLayers] = useState([])
    const [currentItinerary, setCurrentItinerary] = useState(null)

    const [isLayerLoading, setIsLayerLoading] = useState(false)

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

    return(
        <MainContext.Provider
            value={{
                userPosition,
                setUserPosition,
                zoomToUserPosition, 
                setZoomToUserPosition,
                listLayers,
                setListLayers,
                selectedLayers,
                setSelectedLayers,
                currentItinerary,
                setCurrentItinerary,
                isLayerLoading,
                setIsLayerLoading
            }}
        >
            {children}
        </MainContext.Provider>
    );
};

export default MainContext;