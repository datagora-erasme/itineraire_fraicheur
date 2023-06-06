import React, { useContext, useState } from 'react'
import ListLayers from './listLayers'
import CalculateItinerary from './calculateItinerary'
import FreshnessAroundUser from './freshnessAroundUser'
import { FaChevronUp, FaChevronDown } from "react-icons/fa";
import MainContext from '../contexts/mainContext';
import CurrentItineraryDetails from './currentItineraryDetails';


function Content(){
    const [showItineraryCalculation, setShowItineraryCalculation] = useState(false)
    const [showFindFreshness, setShowFindFreshness] = useState(false)
    const [showLayers, setShowLayers] = useState(false);

    const { history, setHistory, showCurrentItineraryDetails, setShowCircle, setSelectedLayers, setCurrentItinerary, setSelectedEndAddress, setEndAddress, setShowCurrentItineraryDetails } = useContext(MainContext)

    return(
        <div style={{zIndex:1000}} className="absolute md:top-8 bottom-4 flex flex-col gap-4 w-full p-8 md:pd-0 md:w-[400px] md:gap-0 md:rounded-full">
            <div className="hidden md:block bg-bgWhite w-[300px] ml-[20px] p-4 absolute top-0 rounded-full font-bold text-xl drop-shadow-lg">Sortons au frais !</div>
            <div className="hidden md:block h-8 bg-bgWhite rounded-t-3xl"></div>
            {showCurrentItineraryDetails && <CurrentItineraryDetails/>}
            <button 
                onClick={() => {
                    setShowItineraryCalculation(!showItineraryCalculation)
                    setShowFindFreshness(false)
                    setShowLayers(false)
                    setHistory([...history, {fn: () => setShowItineraryCalculation(false)}])
                    setShowCircle(false)
                    setSelectedLayers([])
                    window.trackButtonClick("OpenCalculateItinerary")
                    }} 
                className="main-btn main-btn-mobile md:main-btn-desktop md:rounded-none md:rounded-b-none md:border-b-2 md:border-b-gray-100">
                {showItineraryCalculation ? (
                <FaChevronUp className="hidden md:block text-gray-500 mt-1" />
                ) : (
                <FaChevronDown className="hidden md:block text-gray-500 mt-1" />
                )}
                <span>Calculer un itinéraire</span>
                {/* <span className="hidden md:block">Je calcule mon itinéraire fraîcheur</span> */}
            </button>
            {showItineraryCalculation && <CalculateItinerary showItineraryCalculation={showItineraryCalculation} setShowItineraryCalculation={setShowItineraryCalculation}/>}

            <button 
                onClick={() => {
                    setShowFindFreshness(!showFindFreshness)
                    setShowItineraryCalculation(false)
                    setShowLayers(false)
                    setHistory([...history, {fn: () => setShowFindFreshness(false)}])
                    setCurrentItinerary(null)
                    setSelectedEndAddress(null)
                    setEndAddress("")
                    setShowCurrentItineraryDetails(false)
                    setSelectedLayers([])
                    window.trackButtonClick("OpenFindFreshness")
                }} 
                className="main-btn main-btn-mobile md:main-btn-desktop md:rounded-none md:border-b-2 md:border-b-gray-100"
                >
                {showFindFreshness ? (
                <FaChevronUp className="hidden md:block text-gray-500 mt-1" />
                ) : (
                <FaChevronDown className="hidden md:block text-gray-500 mt-1" />
                )}
                <span>Trouver un lieu frais</span>
            </button>
            {showFindFreshness && <FreshnessAroundUser showFindFreshness={showFindFreshness} setShowFindFreshness={setShowFindFreshness}/>}

            <button 
                onClick={() => {
                    setShowLayers(!showLayers)
                    setShowItineraryCalculation(false)
                    setShowFindFreshness(false)
                    setHistory([...history, {fn: () => setShowLayers(false)}])
                    setCurrentItinerary(null)
                    setSelectedEndAddress(null)
                    setEndAddress("")
                    setShowCurrentItineraryDetails(false)
                    setShowCircle(false)
                    window.trackButtonClick("OpenLayers")
                }} 
                className="main-btn main-btn-mobile md:main-btn-desktop md:rounded-none md:border-b-2 md:border-b-gray-100">
                {showLayers ? (
                <FaChevronUp className="hidden md:block text-gray-500 mt-1" />
                ) : (
                <FaChevronDown className="hidden md:block text-gray-500 mt-1" />
                )}
                <span>Consulter la carte fraîcheur</span>
            </button>
            {showLayers && <ListLayers showLayers={showLayers} setShowLayers={setShowLayers}/>}

            <div className='cursor-pointer secondary-btn secondary-btn-mobile md:main-btn-desktop md:rounded-t-none md:rounded-b-3xl'>
                <a 
                    target="_blank" 
                    rel="noopener noreferrer" 
                    href='https://datagora.erasme.org/projets/sortons-au-frais/'
                    >
                        En savoir plus
                    </a>
            </div>
        </div>
    )
}

export default Content