import React, { useState } from "react";
import axios from "axios";
import { FaRoute, FaChevronUp, FaChevronDown } from "react-icons/fa";

//`https://nominatim.openstreetmap.org/search?q=${value}&format=json&addressdetails=1&limit=5`

const SelectAddress = ({setCurrentItinerary}) => {
  const [startAddress, setStartAddress] = useState("");
  const [endAddress, setEndAddress] = useState("");
  const [startAddressSuggestions, setStartAddressSuggestions] = useState([]);
  const [endAddressSuggestions, setEndAddressSuggestions] = useState([])
  const [selectedStartAddress, setSelectedStartAddress] = useState(null)
  const [selectedEndAddress, setSelectedEndAddress] = useState(null)

  const [showStartSuggestions, setShowStartSuggestions] = useState(false);
  const [showEndSuggestions, setShowEndSuggestions] = useState(false);

  const [isLoading, setIsLoading] = useState(false)

  const [showItineraryCalculation, setShowItineraryCalculation] = useState(true)

  let startTimeout;
  let endTimeout;

  const handleToggleItineraryCalculation = () => {
    setShowItineraryCalculation(!showItineraryCalculation)
  }

  const handleStartAddressChange = (event) => {
    const value = event.target.value;
    //replace double white space and then replace by +
    let query = value.replace(/\s{2,}/g, ' ')
    query = query.replace(/ /g, "+")
    setStartAddress(value);
    setSelectedStartAddress(null)
    clearTimeout(startTimeout)
    startTimeout = setTimeout(() => {
        axios
        .get(
          `https://api-adresse.data.gouv.fr/search/?q=${query}&limit=5&lat=45.763&lon=4.836`
        )
        .then((response) => {
          setStartAddressSuggestions(response.data.features);
        })
        .catch((error) => {
          console.log(error);
        });
    }, 2000)

  };

  const handleEndAddressChange = (event) => {
    const value = event.target.value;
    //replace double white space and then replace by +
    let query = value.replace(/\s{2,}/g, ' ')
    query = query.replace(/ /g, "+")
    setEndAddress(value);
    setSelectedEndAddress(null)
    clearTimeout(endTimeout)
    endTimeout = setTimeout(() => {
        axios
        .get(
          `https://api-adresse.data.gouv.fr/search/?q=${query}&limit=5&lat=45.763&lon=4.836`
        )
        .then((response) => {
          setEndAddressSuggestions(response.data.features);
        })
        .catch((error) => {
          console.log(error);
        });
    }, 2000)

  };

  const handleSelectStartAddress = (id) => {
    for(let address of startAddressSuggestions){
        if(address.properties.id == id){
            setStartAddress(`${address.properties.label.slice(0,30)}...`)
            setSelectedStartAddress(address)
            setStartAddressSuggestions([])
        }
    }
  }

  const handleSelectEndAddress = (id) => {
    for(let address of endAddressSuggestions){
        if(address.properties.id == id){
            setEndAddress(`${address.properties.label.slice(0,30)}...`)
            setSelectedEndAddress(address)
            setEndAddressSuggestions([])
        }
    }
  }

  const calculateItinerary = () => {
    setIsLoading(true)
    const start = performance.now()
    axios.get("http://localhost:3002/itinerary", {
        params: {
            start: {
                lat: selectedStartAddress.geometry.coordinates[1], 
                lon: selectedStartAddress.geometry.coordinates[0]
            },
            end: {
                lat : selectedEndAddress.geometry.coordinates[1],
                lon : selectedEndAddress.geometry.coordinates[0]
            }
        }
    }).then((response) => {
        const end = performance.now()
        console.log("duration : ", (end-start)/1000)
        setCurrentItinerary(response.data)
        setIsLoading(false)
    }).catch((error) => {
        console.error(error)
    })
  }

  const handleEndFocus = () => {
    setShowEndSuggestions(true);
  };

  return (
      <div className="bg-white bg-opacity-80 p-4 rounded-md shadow-lg">
          <button
          className="flex items-center cursor-pointer"
          onClick={handleToggleItineraryCalculation}
          >
            <span className="text-lg font-bold mr-2">Calcul d'itinéraires frais</span>
            {showItineraryCalculation ? (
              <FaChevronUp className="text-gray-500 mt-1" />
            ) : (
              <FaChevronDown className="text-gray-500 mt-1" />
            )}
        </button>
        {showItineraryCalculation && <div>
          <label htmlFor="startAddress" className="block font-medium mb-1">
            Adresse de départ :
          </label>
          <div className="relative">
            <input
              type="text"
              id="startAddress"
              name="startAddress"
              value={startAddress}
              onChange={handleStartAddressChange}
              onFocus={() => setShowStartSuggestions(true)}
              onBlur={() => setTimeout(() => setShowStartSuggestions(false), 200)}
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="Adresse de départ"
            />
            { showStartSuggestions && <ul
              id="startAddressSuggestions"
              className="absolute z-10 w-full bg-white border-gray-300 rounded-md shadow-lg mt-1"
              value={startAddress}
            >
              {startAddressSuggestions.map((suggestion) => {
                return(                
                  <li key={suggestion.properties.id} value={suggestion.properties.id} onClick={() => handleSelectStartAddress(suggestion.properties.id)}>
                    {suggestion.properties.label.length > 40 ? `${suggestion.properties.label.slice(0, 40)}...` : suggestion.properties.label}
                  </li>
                )
              })}
            </ul>}
          </div>
          
          <label htmlFor="endAddress" className="block font-medium my-2">
            Adresse d'arrivée :
          </label>
          <div className="relative">
            <input
              type="text"
              id="endAddress"
              name="endAddress"
              value={endAddress}
              onChange={handleEndAddressChange}
              onFocus={() => handleEndFocus(true)}
              onBlur={() => setTimeout(() => handleEndFocus(false), 200)}
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
              placeholder="Adresse d'arrivée"
            />
            {showEndSuggestions && <ul
              id="endAddressSuggestions"
              className="absolute z-10 w-full bg-white border-gray-300 rounded-md shadow-lg mt-1"
              value={endAddress}
              onChange={handleSelectEndAddress}
            >
              {endAddressSuggestions.map((suggestion) => (
                <li key={suggestion.properties.id} value={suggestion.properties.id} onClick={() => handleSelectEndAddress(suggestion.properties.id)}>
                  {suggestion.properties.label.length > 40 ? `${suggestion.properties.label.slice(0, 40)}...` : suggestion.properties.label}
                </li>
              ))}
            </ul>}
          </div>
          <div className="flex justify-center items-center">
            <button onClick={calculateItinerary} 
            className={`block mt-8 px-4 py-2 ${!selectedStartAddress || !selectedEndAddress ? "bg-gray-300 hover:bg-gray-400" : "bg-blue-500 hover:bg-blue-600"} text-white rounded-md transition duration-300`}
            disabled={!selectedStartAddress || !selectedEndAddress}
            >
              {isLoading ? (
                <div className="flex items-center">
                  <div className="w-6 h-6 rounded-full border-4 border-gray-300 border-t-blue-500 animate-spin mr-3"></div>
                  <span>Loading...</span>
                </div>
              ) : (
                <div className="flex items-center">
                  <span className="mr-2">Itinéraire | </span>
                  <FaRoute/>
                </div>
              )}
            </button>
          </div>
        </div>}

      </div>

  );
};

export default SelectAddress;
