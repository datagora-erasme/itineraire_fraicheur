import React, { useContext, useState } from "react";
import MainContext from "../contexts/mainContext";
import { FaChevronDown, FaCheck } from "react-icons/fa";
import L from "leaflet"
import axios from "axios";

const PoiDetails = () => {

    const [isLoading, setIsLoading] = useState(false)
    const {poiDetails, setPoiDetails, setCurrentItinerary, userPosition, setShowCircle, setShowPoiDetails, setShowCurrentItineraryDetails, selectedStartAddress} = useContext(MainContext)

    const calculateItinerary = () => {
        let coordinates;
        if(poiDetails.geometry.type === "Polygon"){
            const layer = L.geoJSON(poiDetails)
            const bounds = layer.getBounds()
            const centroid = bounds.getCenter()

            coordinates = [centroid.lat, centroid.lng]
        } else if(poiDetails.geometry.type === "Point"){
            coordinates = [poiDetails.geometry.coordinates[1], poiDetails.geometry.coordinates[0]]
        }
        setIsLoading(true)
        axios({
            method:'get',
            baseURL: `${process.env.REACT_APP_URL_SERVER}`,
            url: "/itinerary/",
            params: {
                start: {
                    lat: selectedStartAddress.geometry.coordinates[1], 
                    lon: selectedStartAddress.geometry.coordinates[0]
                },
                end: {
                    lat : coordinates[0],
                    lon : coordinates[1]
                }
            }
        }).then((response) => {
            setCurrentItinerary(response.data)
            setShowPoiDetails(false)
            setShowCurrentItineraryDetails(true)
            setIsLoading(false)
            setShowCircle(false)
        }).catch((error) => {
            console.error(error)
        })
    }

    return(
        <div className="card md:card-details-desktop">
            {poiDetails && (
                <div className="mb-4 font-bold text-mainText"> 
                    {poiDetails.properties.nom}
                </div>
            )}
            <div className="flex justify-center items-center">
            <button onClick={calculateItinerary} 
            className={` main-btn bg-primary text-white rounded-full transition duration-300`}
            >
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <span>En cours de chargement</span>
                  <div className="w-6 h-6 rounded-full border-4 border-gray-300 border-t-primary animate-spin mr-3"></div>
                </div>
              ) : (
                <div className="flex items-center gap-2" onClick={() => window.trackButtonClick("ValidateCalculateItinerary")}>
                  <span className="">Valider ma recherche </span>
                  <FaCheck/>
                </div>
              )}
            </button>
          </div>
        </div>
    )
}

export default PoiDetails;