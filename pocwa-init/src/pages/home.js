
import React, {useState, useEffect} from 'react';
import Map from '../components/map'
import ListLayers from '../components/listLayers';
import SelectAdress from '../components/selectAdress';

import axios from 'axios'
import Content from '../components/content';

function Home(){
    const [listLayers, setListLayers] = useState([])
    const [selectedLayers, setSelectedLayers] = useState([])
    const [currentItinerary, setCurrentItinerary] = useState(null)

    useEffect(() => {
        async function fetchListLayers(){
            try{
                const response = await axios.get("http://localhost:3002/data")
                setListLayers(response.data)
            } catch (error){
                console.error(error)
            } 
        }
        fetchListLayers()
    }, [])

    return (
        <div style={{position: 'relative'}}>
            <Content selectedLayers={selectedLayers} listLayers={listLayers} setCurrentItinerary={setCurrentItinerary} setSelectedLayers={setSelectedLayers}/>
            <Map selectedLayers={selectedLayers} currentItinerary={currentItinerary}/>
        
        </div>
    );
}

export default Home; 