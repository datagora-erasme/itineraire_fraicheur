import React from 'react'
import { FaChevronDown } from "react-icons/fa";

function ListLayers({listLayers, selectedLayers, setSelectedLayers, isLayerLoading, showLayers, setShowLayers}){

    // const handleToggleLayers = () => {
    //   setShowLayers(!showLayers);
    // };

    function handleCheckBoxList(event){
        const {value, checked} = event.target;
        if(checked){
            setSelectedLayers((prevSelectedLayers) => [...prevSelectedLayers, value]);
        } else {
            const updatedSelectedLayers = selectedLayers.filter((layerId) => layerId !== value)
            setSelectedLayers(updatedSelectedLayers)
        }
    }

    return (
        <div className="card md:card-desktop">
        <button
          className="md:hidden card-title"
          onClick={() => setShowLayers(!showLayers)}
        >
        {isLayerLoading && <div class="w-6 h-6 rounded-full border-4 border-gray-300 border-t-blue-500 animate-spin mr-3"></div>}
          <FaChevronDown className="text-gray-500 mt-1" />
          <span className="text-lg font-bold mr-2">Liste des layers</span>
        </button>
          {listLayers.length !== 0 ? <ul className="mt-2">
            {listLayers.map((layer) => {
              return (
                <li key={layer.id} className="flex items-center justify-start space-x-2">
                  <input
                    type="checkbox"
                    id={layer.id}
                    value={layer.id}
                    checked={selectedLayers.includes(layer.id)}
                    onChange={handleCheckBoxList}
                    disabled={isLayerLoading}
                  />
                  <label htmlFor={layer.id} className="ml-2">
                    {layer.name}
                  </label>
                </li>
              );
            })}
          </ul> : "Loading .. "}
      </div>
      );
    
      
}

export default ListLayers