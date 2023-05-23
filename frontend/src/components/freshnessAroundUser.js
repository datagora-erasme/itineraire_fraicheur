import React, { useState, useContext, useCallback, useEffect } from "react";
import { FaChevronDown } from "react-icons/fa";
import { BiCurrentLocation } from "react-icons/bi"
import MainContext from "../contexts/mainContext";
import axios from "axios";
import _debounce from 'lodash/debounce'

const FreshnessAroundUser = ({ showFindFreshness, setShowFindFreshness}) => {
    const [startAddressSuggestions, setStartAddressSuggestions] = useState([]);
    const [showStartSuggestions, setShowStartSuggestions] = useState(false);
    // const [startAddress, setStartAddress] = useState("")
    
    const { userPosition, setZoomToUserPosition, history, setHistory, 
        startAddress, setStartAddress, selectedStartAddress, setSelectedStartAddress, userAddress,
        radius, setRadius, showCircle, setShowCircle
    } = useContext(MainContext)
    // const handleToggleShowFindFreshness = () => {
    //     setShowFindFreshness(!showFindFreshness)
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
    /*eslint-disable*/
    const debounceStartAddress = useCallback(_debounce(handleStartAddressAPI, 300), [])

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

    const findFreshnessAroundMe = () => {
        if (selectedStartAddress) {
            setZoomToUserPosition(true)
        } else {
            alert("Veuillez activez votre géolocalisation pour utiliser cette fonctionnalité")
        }
    }

    const handleSelectStartAddress = (id) => {
        for(let address of startAddressSuggestions){
            if(address.properties.id === id){
                setStartAddress(`${address.properties.label.slice(0,30)}...`)
                setSelectedStartAddress(address)
                setStartAddressSuggestions([])
            }
        }
      }

    const handleChangeRadius = (e) => {
        setRadius(e.target.value)
    }

    const handleSelectUserAddress = () => {
        console.log("test")
        setStartAddress(userAddress.properties.label)
        setSelectedStartAddress(userAddress)
    }

    useEffect(() => {
        if(userAddress && startAddress === ""){
          setStartAddress(userAddress.properties.label)
          setSelectedStartAddress(userAddress)
        }
      }, [userAddress])


    return (
        <div className="card md:card-desktop">
            <button
                className="md:hidden card-title"
                onClick={() => {
                    setShowFindFreshness(!showFindFreshness)
                    setHistory(history.slice(0,-1))
                }}
            >
                <FaChevronDown className="text-gray-500 mt-1" />
                <span className="text-lg font-bold mr-2">Lieu le plus frais autour de moi</span>
            </button>

                <div className="flex flex-col p-2">
                    <label htmlFor="startAddress" className="block mb-1 mt-4 flex justify-between">
                        <p>Départ</p>
                        <input type="checkbox" onChange={() => setShowCircle(!showCircle)} checked={showCircle}></input>
                    </label>
                    <div className="relative flex gap-2">
                        <input
                        type="text"
                        id="startAddress"
                        name="startAddress"
                        value={startAddress}
                        onChange={handleStartAddressChange}
                        onFocus={() => setShowStartSuggestions(true)}
                        onBlur={() => setTimeout(() => setShowStartSuggestions(false), 200)}
                        className="main-input mb-2"
                        placeholder="Adresse de départ"
                        />
                        { showStartSuggestions && <ul
                        id="startAddressSuggestions"
                        className="absolute z-10 w-full bg-white border-gray-300 rounded-md shadow-lg mt-12 md:mt-10"
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
                        <BiCurrentLocation size={30} className="mt-2 cursor-pointer" onClick={handleSelectUserAddress}/>
                    </div>
                    <div className="w-full mx-auto mb-2 flex flex-col gap-2 mt-2">
                        <div className="w-full flex justify-between">
                            <p>Distance (km)</p>
                            <p className="font-bold">{radius} km</p>
                        </div>
                        <input
                            type="range"
                            min="0.2"
                            max="10"
                            step="0.2"
                            value={radius}
                            onChange={handleChangeRadius}
                            className="w-full h-4 bg-gray-400 rounded-full appearance-none"
                        />
                        <div className="flex justify-between">
                            <span>0.2 km</span>
                            <span>10 km</span>
                        </div>
                    </div>
                    <div className="w-full flex justify-center">
                        <button
                            onClick={findFreshnessAroundMe}
                            className={` main-btn ${!selectedStartAddress ? "bg-gray-300 hover:bg-gray-400" : "bg-primary"} text-white rounded-full transition duration-300`}
                            disabled={!selectedStartAddress}
                        >
                            Trouver les lieux frais
                        </button>
                    </div>
                </div>
        </div>
    );
} 

export default FreshnessAroundUser;