import React, {useState} from "react";
import { FaChevronUp, FaChevronDown } from "react-icons/fa";

const FreshnessAroundUser = ({position, zoomToUserPosition, setZoomToUserPosition}) => {
    const [showFindFreshness, setShowFindFreshness] = useState(false)

    const handleToggleShowFindFreshness = () => {
        setShowFindFreshness(!showFindFreshness)
    }

    const findFreshnessAroundMe = () => {
        if (position) {
            setZoomToUserPosition(true)
        } else {
            alert("Veuillez activez votre géolocalisation pour utiliser cette fonctionnalité")
        }
    }


    return (
        <div className="bg-white bg-opacity-80 p-4 rounded-md shadow-lg mt-2">
            <button
                className="flex items-center justify-center cursor-pointer"
                onClick={handleToggleShowFindFreshness}
            >
                <span className="text-lg font-bold mr-2">Lieu le plus frais autour de moi</span>
                {showFindFreshness ? (
                    <FaChevronUp className="text-gray-500 mt-1" />
                ) : (
                    <FaChevronDown className="text-gray-500 mt-1" />
                )}
            </button>
            {showFindFreshness && (
                <div className="flex justify-center mt-8">
                    <button
                        onClick={findFreshnessAroundMe}
                        className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-md transition duration-300"
                    >
                        Trouver les lieux frais
                    </button>
                </div>
            )}
        </div>
    );
} 

export default FreshnessAroundUser;