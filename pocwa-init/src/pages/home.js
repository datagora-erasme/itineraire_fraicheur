
import React, {useState, useEffect} from 'react';
import Map from '../components/map'
import ListLayers from '../components/listLayers';
import SelectAdress from '../components/selectAdress';

import axios from 'axios'

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
        <div>
            <SelectAdress setCurrentItinerary={setCurrentItinerary}/>
            <Map selectedLayers={selectedLayers} currentItinerary={currentItinerary}/>
            {listLayers.length !== 0 ? <ListLayers listLayers={listLayers} selectedLayers={selectedLayers} setSelectedLayers={setSelectedLayers} /> : "loading ..."}        
        </div>
    );
}

export default Home; 