const express = require('express');
const cors = require('cors');

const { setupRoutes } = require('./routes/index');

const { loadGraph } = require('./load_network')

const app = express();

app.use(express.json());
app.use(cors());

setupRoutes(app);

const NETWORK_PATH = './data/osm/final_network.gpkg';
const NETWORK_PICKLE_PATH = './data/pickle_network.pickle'

async function startServer() {
    console.log("LOADING GRAPH");
    let status = await loadGraph(NETWORK_PATH, NETWORK_PICKLE_PATH);
    if(status.toString() === "OK"){
        console.log("GRAPH LOADED");
    } else {
        console.error("ERROR WHEN LOADING GRAPH")
    }
  
    const PORT = 3002;
    app.listen(PORT, () => console.log(`server listening on port ${PORT}`));
  }
  
startServer();