import React, { useContext } from "react";
import { FaArrowLeft } from "react-icons/fa";
import MainContext from "../contexts/mainContext";

const BackButton = () => {
    const { history, setHistory } = useContext(MainContext)
    return(
        <button 
            style={{zIndex:1000}} 
            className={`absolute main-btn main-btn-mobile flex gap-2 top-8 left-8 md:hidden ${history.length == 0 && "hidden"}`}
            onClick={() => {
                history[history.length -1].fn()
                setHistory(history.slice(0,-1))
            }}
            >
            <FaArrowLeft className="mt-1"/>
            <span>Retour</span>
        </button>
    )
}

export default BackButton;