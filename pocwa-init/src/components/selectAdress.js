import React, { useState } from "react";
import axios from "axios";

const SelectAddress = () => {
  const [startAddress, setStartAddress] = useState("");
  const [endAddress, setEndAddress] = useState("");
  const [startAddressSuggestions, setStartAddressSuggestions] = useState([]);
  const [endAddressSuggestions, setEndAddressSuggestions] = useState([])
  const [selectedStartAddress, setSelectedStartAddress] = useState(null)
  const [selectedEndAddress, setSelectedEndAddress] = useState(null)
  let timeout;

  const handleStartAddressChange = (event) => {
    const value = event.target.value;
    setStartAddress(value);
    clearTimeout(timeout)
    timeout = setTimeout(() => {
        axios
        .get(
          `https://nominatim.openstreetmap.org/search?q=${value}&format=json&addressdetails=1&limit=5`
        )
        .then((response) => {
          setStartAddressSuggestions(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    }, 500)

  };

  const handleEndAddressChange = (event) => {
    const value = event.target.value;
    setEndAddress(value);
    axios
      .get(
        `https://nominatim.openstreetmap.org/search?q=${value}&format=json&addressdetails=1&limit=5`
      )
      .then((response) => {
        setEndAddressSuggestions(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const handleSelectStartAddress = (event) => {
    for(let address of startAddressSuggestions){
        if(address.osm_id == event.target.value){
            setStartAddress(`${address.display_name.slice(0,30)}...`)
            setSelectedStartAddress(address)
            setStartAddressSuggestions([])
        }
    }
  }

  const handleSelectEndAddress = (event) => {
    for(let address of endAddressSuggestions){
        if(address.osm_id == event.target.value){
            setEndAddress(`${address.display_name.slice(0,30)}...`)
            setSelectedEndAddress(address)
            setEndAddressSuggestions([])
        }
    }
  }

  console.log(startAddressSuggestions)

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
            key={suggestion.place_id} 
            value={suggestion.osm_id}
            onClick={handleSelectStartAddress}
            >
                {suggestion.display_name.length > 30 ? `${suggestion.display_name.slice(0,30)}...`: suggestion.display_name}
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
            key={suggestion.place_id} 
            value={suggestion.osm_id}
            onClick={handleSelectEndAddress}
            >
                {suggestion.display_name.length > 30 ? `${suggestion.display_name.slice(0,30)}...`: suggestion.display_name}
            </option>
        ))}
      </datalist>
    </div>
  );
};

export default SelectAddress;
