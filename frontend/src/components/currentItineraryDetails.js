import React, { useContext, useEffect, useState } from "react";
import MainContext from "../contexts/mainContext";
import { FaHourglassStart } from "react-icons/fa";

const CurrentItineraryDetails = () => {
    const { currentItinerary } = useContext(MainContext)
    const [details, setDetails] = useState([])

    useEffect(() => {
        if(currentItinerary){
            setDetails([])
            for(let it of currentItinerary){
                let tot = 0
                let dist = 0
                let duration = 0
                it.geojson.features.map((feat) => {
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
                setDetails((det) => [...det, {name: it.name, color: it.color, distance: dist, duration: duration}])
            }

        }
    }, [currentItinerary])

    return(
        <div className="card md:card-details-desktop">
            <div className="flex flex-col gap-4">
                {details.map((det, i) => {
                    return(
                        <div key={i} className="flex flex-col items-start w-full">
                            <h6 className="font-bold text-mainText">{det.name} <span style={{color: det.color}} className="-mt-2">   ____</span></h6>
                            <div className="flex gap-4">
                                <div className="px-2">Distance : {det.distance}</div>
                                <div className="px-2 flex"><FaHourglassStart className="mt-1"/> {det.duration}</div>
                            </div>
                        </div>
                    )
                })}
            </div>
        </div>
    )
}

export default CurrentItineraryDetails;