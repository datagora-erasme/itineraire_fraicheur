import React, { useContext } from "react";
import { FaChevronDown } from "react-icons/fa";
import MainContext from "../contexts/mainContext";

const FreshnessAroundUser = ({ showFindFreshness, setShowFindFreshness}) => {
    
    const { userPosition, setZoomToUserPosition  } = useContext(MainContext)
    // const handleToggleShowFindFreshness = () => {
    //     setShowFindFreshness(!showFindFreshness)
    // }

    const findFreshnessAroundMe = () => {
        console.log(userPosition)
        if (userPosition) {
            setZoomToUserPosition(true)
        } else {
            alert("Veuillez activez votre géolocalisation pour utiliser cette fonctionnalité")
        }
    }


    return (
        <div className="card md:card-desktop" onBlur={() => setShowFindFreshness(!showFindFreshness)}>
            <button
                className="md:hidden card-title"
                onClick={() => setShowFindFreshness(!showFindFreshness)}
            >
                <FaChevronDown className="text-gray-500 mt-1" />
                <span className="text-lg font-bold mr-2">Lieu le plus frais autour de moi</span>
                

            </button>
                <div className="flex justify-center mt-8">
                    <button
                        onClick={findFreshnessAroundMe}
                        className="main-btn main-btn-mobile"
                    >
                        Trouver les lieux frais
                    </button>
                </div>
        </div>
    );
} 

export default FreshnessAroundUser;