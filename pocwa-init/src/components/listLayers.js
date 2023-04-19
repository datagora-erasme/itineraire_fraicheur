import React from 'react'

function ListLayers({listLayers, selectedLayers, setSelectedLayers}){

    function handleCheckBoxList(event){
        const {value, checked} = event.target;
        if(checked){
            setSelectedLayers((prevSelectedLayers) => [...prevSelectedLayers, value]);
        } else {
            const updatedSelectedLayers = selectedLayers.filter((layerId) => layerId !== value)
            setSelectedLayers(updatedSelectedLayers)
        }
    }

    return(
        <div>
            <h2>Liste des layers</h2>
            <ul>
                {
                    listLayers.map((layer) => {
                        return(
                            <li key={layer.id} >
                                <input 
                                    type="checkbox" 
                                    id={layer.id}
                                    value={layer.id}
                                    checked={selectedLayers.includes(layer.id)}
                                    onChange={handleCheckBoxList}
                                    >
                                </input>
                                <label htmlFor={layer.id}>{layer.name}</label>
                            </li>
                        )
                    })
                }
            </ul>
        </div>
    )
}

export default ListLayers