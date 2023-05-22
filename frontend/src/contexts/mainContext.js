import React, {createContext, useState, useEffect} from "react"
import axios from 'axios'

const MainContext = createContext();

export const MainContextProvider = ({ children }) => {
    const [userPosition, setUserPosition] = useState(null)
    const [zoomToUserPosition, setZoomToUserPosition] = useState(false)

    const [listLayers, setListLayers] = useState([])
    const [selectedLayers, setSelectedLayers] = useState([])
    const [currentItinerary, setCurrentItinerary] = useState(null)
    const [showCurrentItineraryDetails, setShowCurrentItineraryDetails] = useState(false)

    const [startAddress, setStartAddress] = useState("");
    const [endAddress, setEndAddress] = useState("");
    const [selectedStartAddress, setSelectedStartAddress] = useState(null)
    const [selectedEndAddress, setSelectedEndAddress] = useState(null)

    const [isLayerLoading, setIsLayerLoading] = useState(false)

    const [userAddress, setUserAddress] = useState(null)

    const [history, setHistory] = useState([])

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

    useEffect(() => {
        if(userPosition){
            axios
            .get(
              `https://api-adresse.data.gouv.fr/reverse/?lon=${userPosition[1]}&lat=${userPosition[0]}`
            )
            .then((response) => {
              setUserAddress(response.data.features[0]);
            })
            .catch((error) => {
              console.log(error);
            });
        }
    }, [userPosition])

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
                showCurrentItineraryDetails,
                setShowCurrentItineraryDetails,
                isLayerLoading,
                setIsLayerLoading,
                userAddress, 
                history, 
                setHistory,
                startAddress, 
                setStartAddress,
                endAddress,
                setEndAddress,
                selectedStartAddress,
                setSelectedStartAddress,
                selectedEndAddress,
                setSelectedEndAddress
            }}
        >
            {children}
        </MainContext.Provider>
    );
};

export default MainContext;