import React, {createContext, useState, useEffect} from "react"
import axios from 'axios'

const MainContext = createContext();

export const MainContextProvider = ({ children }) => {
    const [userPosition, setUserPosition] = useState(null)
    const [zoomToUserPosition, setZoomToUserPosition] = useState(false)
    const [zoomToItinerary, setZoomToItinerary] = useState(false)

    const [listLayers, setListLayers] = useState([])
    const [layers, setLayers] = useState([])
    const [selectedLayers, setSelectedLayers] = useState([])
    const [freshnessLayers, setFreshnessLayers] = useState([])

    const [filteredFreshnessFeatures ,setFilteredFreshnessFeatures] = useState([])
    const [filteredItinerariesFeatures, setFilteredItinerariesFeatures] = useState([])

    const [currentItinerary, setCurrentItinerary] = useState(null)
    const [showCurrentItineraryDetails, setShowCurrentItineraryDetails] = useState(false)
    const [showFindFreshness, setShowFindFreshness] = useState(false)

    const [startAddress, setStartAddress] = useState("");
    const [endAddress, setEndAddress] = useState("");
    const [selectedStartAddress, setSelectedStartAddress] = useState(null)
    const [selectedEndAddress, setSelectedEndAddress] = useState(null)

    const [isLayerLoading, setIsLayerLoading] = useState(false)

    const [userAddress, setUserAddress] = useState(null)

    const [history, setHistory] = useState([])

    const [radius, setRadius] = useState(1)

    const [showCircle, setShowCircle] = useState(false)

    const [showPoiDetails, setShowPoiDetails] = useState(false)

    const [poiDetails, setPoiDetails] = useState(null)

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
      async function fetchLayers(){
        const res = await axios.get(`${process.env.REACT_APP_URL_SERVER}/data/`, {
          params:{
              id: "all"
          }
        })
        setLayers(res.data)
      }
        fetchLayers()
    }, [])

    // console.log("layers: ", layers)

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
      async function fetchFreshnessLayers(){
        const fetchParcs = await axios.get(`${process.env.REACT_APP_URL_SERVER}/data/`, {
          params:{
              id: "parcs_jardins_metropole"
          }
      })
        const fetchFreshPlaces = await axios.get("https://download.data.grandlyon.com/ws/grandlyon/com_donnees_communales.equipementspublicsclimatises/all.json")
        // console.log(fetchFreshPlaces.data.values)
        const freshplaces = {
          id: "batiments_frais",
          geojson: {
            crs: {
              properties: {name: 'urn:ogc:def:crs:OGC:1.3:CRS84'},
              type: "name"
            },
            features: fetchFreshPlaces.data.values.map((val) => {
            return {
                geometry: {coordinates: [val.lon, val.lat], type:"Point"},
                properties: {
                  ...val,
                  markerOption: {
                    iconUrl: "building.svg",
                    iconRetinaUrl: "building.svg",
                    popupAnchor: [
                              0,
                              0
                          ],
                    iconSize: [
                              40,
                              40
                          ],
                    clusterCountStyle: "position:absolute;top:48px;left:0px;color:black;font-weight:bold;"
                  }
                },
                type: "Feature"
              }
              }),
            type: "FeatureCollection"
        },
        }
        // console.log("parcs : ", fetchParcs.data)
        // console.log("fetchFreshPlaces.data : ", freshplaces)
        setFreshnessLayers([fetchParcs.data, freshplaces])
      }
      fetchFreshnessLayers()
    }, [])

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

    useEffect(() => {
      setZoomToItinerary(true)
    }, [currentItinerary])

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
                setSelectedEndAddress,
                radius,
                setRadius, 
                showCircle, 
                setShowCircle,
                zoomToItinerary,
                setZoomToItinerary,
                freshnessLayers,
                showPoiDetails,
                setShowPoiDetails,
                showFindFreshness,
                setShowFindFreshness,
                poiDetails, 
                setPoiDetails,
                layers,
                filteredFreshnessFeatures,
                setFilteredFreshnessFeatures,
                filteredItinerariesFeatures,
                setFilteredItinerariesFeatures
            }}
        >
            {children}
        </MainContext.Provider>
    );
};

export default MainContext;