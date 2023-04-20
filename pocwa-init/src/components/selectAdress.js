import React, { useState } from "react";
import axios from "axios";

//`https://nominatim.openstreetmap.org/search?q=${value}&format=json&addressdetails=1&limit=5`

const SelectAddress = ({setCurrentItinerary}) => {
  const [startAddress, setStartAddress] = useState("");
  const [endAddress, setEndAddress] = useState("");
  const [startAddressSuggestions, setStartAddressSuggestions] = useState([]);
  const [endAddressSuggestions, setEndAddressSuggestions] = useState([])
  const [selectedStartAddress, setSelectedStartAddress] = useState(null)
  const [selectedEndAddress, setSelectedEndAddress] = useState(null)
  let startTimeout;
  let endTimeout;

  const handleStartAddressChange = (event) => {
    const value = event.target.value;
    //replace double white space and then replace by +
    let query = value.replace(/\s{2,}/g, ' ')
    query = query.replace(/ /g, "+")
    setStartAddress(value);
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

  const handleSelectStartAddress = (event) => {
    for(let address of startAddressSuggestions){
        if(address.properties.id == event.target.value){
            setStartAddress(`${address.properties.label.slice(0,30)}...`)
            setSelectedStartAddress(address)
            setStartAddressSuggestions([])
        }
    }
  }

  const handleSelectEndAddress = (event) => {
    for(let address of endAddressSuggestions){
        if(address.properties.id == event.target.value){
            setEndAddress(`${address.properties.label.slice(0,30)}...`)
            setSelectedEndAddress(address)
            setEndAddressSuggestions([])
        }
    }
  }

  const calculateItinerary = () => {
    console.log(selectedEndAddress.lat)
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
        console.log(response)
        setCurrentItinerary(response.data)
    }).catch((error) => {
        console.error(error)
    })
  }

  return (
    <div>
      <label htmlFor="startAddress">Start Address:</label>
      <input
        type="text"
        id="startAddress"
        name="startAddress"
        value={startAddress}
        onChange={handleStartAddressChange}
        list="startAddressSuggestions"
      />
      <datalist id="startAddressSuggestions" style={{display: "block"}}>
        {startAddressSuggestions.map((suggestion) => (
          <option 
            key={suggestion.properties.id} 
            value={suggestion.properties.id}
            onClick={handleSelectStartAddress}
            >
                {suggestion.properties.label.length > 30 ? `${suggestion.properties.label.slice(0,30)}...`: suggestion.properties.label}
          </option>
        ))}
      </datalist>

      <label htmlFor="endAddress">End Address:</label>
      <input
        type="text"
        id="endAddress"
        name="endAddress"
        value={endAddress}
        onChange={handleEndAddressChange}
        list="endAddressSuggestions"
      />
      <datalist id="endAddressSuggestions" style={{display: "block"}}>
        {endAddressSuggestions.map((suggestion) => (
            <option 
            key={suggestion.properties.id} 
            value={suggestion.properties.id}
            onClick={handleSelectEndAddress}
            >
                {suggestion.properties.label.length  > 30 ? `${suggestion.properties.label.slice(0,30)}...`: suggestion.properties.label}
            </option>
        ))}
      </datalist>

      <button onClick={calculateItinerary}>Calculer</button>
    </div>
  );
};

export default SelectAddress;
