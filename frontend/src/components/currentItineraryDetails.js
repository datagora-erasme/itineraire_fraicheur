import React, { useContext, useEffect, useState } from "react";
import MainContext from "../contexts/mainContext";
import { FaHourglassStart } from "react-icons/fa";
import {BiX} from "react-icons/bi"

const CurrentItineraryDetails = ({showMenu}) => {
    const { currentItinerary, filteredItinerariesFeatures, setHistory, setShowCurrentItineraryDetails } = useContext(MainContext)
    const [details, setDetails] = useState([])

    useEffect(() => {
        if(currentItinerary){
            setDetails([])
            for(let it of currentItinerary){
                let tot = 0
                let dist = 0
                let duration = 0
                it.geojson.features.forEach((feat) => {
                    tot = tot + feat.properties.length
                })
                if(tot > 1000){
                    dist = (Math.round(tot)/1000).toString() + " km"
                } else {
                    dist = Math.round(tot).toString() + " m"
                }
                duration = Math.round(Math.round(tot) * 60 / 4000)
                if(duration > 60){
                    let hour = Math.trunc(duration/60)
                    let minutes = duration % 60
                    duration = hour.toString()+ "h " + minutes.toString() +"min"
                } else {
                    duration = duration.toString() + "min"
                }
                setDetails((det) => [...det, {id: it.id, name: it.name, color: it.color, distance: dist, duration: duration}])
            }

        }
    }, [currentItinerary])

    return(
        <div className={`${showMenu ? "" : "hidden"} md:block mt-4 md:mt-0 card md:card-details-desktop`}>
            <div 
                className="absolute -ml-6 -mt-2 w-full flex justify-end cursor-pointer" 
                onClick={() =>{ 
                    setShowCurrentItineraryDetails(false)
                    }}
                >
                <BiX className="w-6 h-6"/></div>
            <div className="flex flex-col gap-4">
                {details.map((det, i) => {
                    return(
                        <div key={i} className="flex flex-col items-start w-full">
                            <div className="flex w-full items-center gap-6">
                                <h6 className="font-bold text-mainText">{det.name}</h6>
                                <div className="bg-gradient-to-r from-startGradientLegend to-endGradientLegend w-[100px] h-[5px] flex flex-row gap-4 pl-4">
                                    {det.id === "LENGTH" && (
                                        <>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                            <div className="h-full w-[10px] bg-white"> </div>
                                        </>
                                    )}
                                </div>
                            </div>
                            <div className="flex gap-4">
                                <div className="px-2">Distance : {det.distance}</div>
                                <div className="px-2 flex"><FaHourglassStart className="mt-1"/> {det.duration}</div>
                            </div>
                        </div>
                    )
                })}
            </div>
            <div className="mt-2 flex flex-col items-start gap-2">
                <h6 className="font-bold text-mainText">Sur votre chemin : </h6>
                <ul className="flex flex-row gap-8 flex-wrap">
                    {
                        filteredItinerariesFeatures.map((layer) => {
                            if(layer.geojson.length !== 0){
                                return(
                                    <li className="flex flex-row gap-2 items-center">
                                        {layer.geojson.length}
                                        <img className="w-8 h-8" alt={`${layer.id}_icon`} src={layer.markerOption.iconUrl}/>
                                    </li>
                                )
                            }
                            return null
                        })
                    }
                </ul>
            </div>
        </div>
    )
}

export default CurrentItineraryDetails;