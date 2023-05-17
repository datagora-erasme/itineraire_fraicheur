import React from 'react'
// import { FaChevronDown, FaChevronUp } from "react-icons/fa";

function ListLayers({listLayers, selectedLayers, setSelectedLayers, isLayerLoading}){

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
        <div className="bg-white bg-opacity-80 p-4 rounded-md shadow-lg mt-2">
        {/* <button
          className="flex items-center cursor-pointer"
          onClick={handleToggleLayers}
        >
        {isLayerLoading && <div class="w-6 h-6 rounded-full border-4 border-gray-300 border-t-blue-500 animate-spin mr-3"></div>}
          <span className="text-lg font-bold mr-2">Liste des layers</span>
          {showLayers ? (
            <FaChevronUp className="text-gray-500 mt-1" />
          ) : (
            <FaChevronDown className="text-gray-500 mt-1" />
          )}
        </button> */}
        {/* {showLayers && ( */}
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
        {/* )} */}
      </div>
      );
    
      
}

export default ListLayers