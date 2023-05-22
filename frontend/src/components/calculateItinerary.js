import React, { useCallback, useContext, useEffect, useState } from "react";
import axios from "axios";
import _debounce from 'lodash/debounce'
import { FaChevronDown, FaCheck } from "react-icons/fa";
import MainContext from "../contexts/mainContext";


const CalculateItinerary = ({ showItineraryCalculation,  setShowItineraryCalculation}) => {
  const [startAddress, setStartAddress] = useState("");
  const [endAddress, setEndAddress] = useState("");
  const [startAddressSuggestions, setStartAddressSuggestions] = useState([]);
  const [endAddressSuggestions, setEndAddressSuggestions] = useState([])
  const [selectedStartAddress, setSelectedStartAddress] = useState(null)
  const [selectedEndAddress, setSelectedEndAddress] = useState(null)

  const [showStartSuggestions, setShowStartSuggestions] = useState(false);
  const [showEndSuggestions, setShowEndSuggestions] = useState(false);

  const [isLoading, setIsLoading] = useState(false)

  const { setCurrentItinerary, userAddress, history, setHistory } = useContext(MainContext)

  // const handleToggleItineraryCalculation = () => {
  //   setShowItineraryCalculation(!showItineraryCalculation)
  // }

  const handleStartAddressAPI = (query) => {
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
  }

  const handleEndAddressAPI = (query) => {
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
  }

  /*eslint-disable*/
  const debounceStartAddress = useCallback(_debounce(handleStartAddressAPI, 300), [])
  const debounceEndAddress = useCallback(_debounce(handleEndAddressAPI, 300), [])

  const handleStartAddressChange = (event) => {
    const value = event.target.value;
    //replace double white space and then replace by +
    let query = value.replace(/\s{2,}/g, ' ')
    query = query.replace(/ /g, "+")
    setStartAddress(value);
    setSelectedStartAddress(null)
    // clearTimeout(startTimeout)
    if(query.length > 3){
      debounceStartAddress(query)
    } else {
      setStartAddressSuggestions([])
    }
  };

  const handleEndAddressChange = (event) => {
    const value = event.target.value;
    //replace double white space and then replace by +
    let query = value.replace(/\s{2,}/g, ' ')
    query = query.replace(/ /g, "+")
    setEndAddress(value);
    setSelectedEndAddress(null)
    if(query.length > 3){
      debounceEndAddress(query)
    } else {
      setStartAddressSuggestions([])
    }
  };

  const handleSelectStartAddress = (id) => {
    for(let address of startAddressSuggestions){
        if(address.properties.id === id){
            setStartAddress(`${address.properties.label.slice(0,30)}...`)
            setSelectedStartAddress(address)
            setStartAddressSuggestions([])
        }
    }
  }

  const handleSelectEndAddress = (id) => {
    for(let address of endAddressSuggestions){
        if(address.properties.id === id){
            setEndAddress(`${address.properties.label.slice(0,30)}...`)
            setSelectedEndAddress(address)
            setEndAddressSuggestions([])
        }
    }
  }

  const calculateItinerary = () => {
    setIsLoading(true)
    const start = performance.now()
    axios.get(`${process.env.REACT_APP_URL_SERVER}/itinerary/`, {
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

  useEffect(() => {
    if(userAddress){
      setStartAddress(userAddress.properties.label)
      setSelectedStartAddress(userAddress)
    }
  }, [userAddress])

  return (
      <div className="card md:card-desktop">
          <button 
            onClick={() => {
              setShowItineraryCalculation(!showItineraryCalculation)
              setHistory(history.slice(0,-1))
            }} 
            className="md:hidden card-title"
            >
              <FaChevronDown className="text-gray-500 mt-1" />
              <span>Calculer un itinéraire</span>
          </button>
          <label htmlFor="startAddress" className="block mb-1 mt-4 flex">
            Départ
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
              className="main-input"
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
          
          <label htmlFor="endAddress" className="block my-2 flex ">
            Arrivée
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
              className="main-input mb-4"
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
            className={` main-btn ${!selectedStartAddress || !selectedEndAddress ? "bg-gray-300 hover:bg-gray-400" : "bg-primary"} text-white rounded-full transition duration-300`}
            disabled={!selectedStartAddress || !selectedEndAddress}
            >
              {isLoading ? (
                <div className="flex items-center gap-2">
                  <span>En cours de chargement</span>
                  <div className="w-6 h-6 rounded-full border-4 border-gray-300 border-t-primary animate-spin mr-3"></div>
                </div>
              ) : (
                <div className="flex items-center gap-2">
                  <span className="">Valider ma recherche </span>
                  <FaCheck/>
                </div>
              )}
            </button>
          </div>
        {/* </div>} */}

      </div>

  );
};

export default CalculateItinerary;
