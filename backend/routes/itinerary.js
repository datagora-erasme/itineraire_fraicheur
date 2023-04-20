const express = require('express');
const Itinerary = require('../models/itinerary');
const fs = require("fs")

const itineraryRouter = express.Router();


itineraryRouter.get('/', async (req, res) => {
    //TODO : send all data awailable (layers)
    if(req.query.start && req.query.end){
      try {
        console.log("calculating itinerary ...");
        let results = await Itinerary.calculateItinerary(req.query.start, req.query.end);
        results = results.split("\n")[0]
        const geojson = JSON.parse(fs.readFileSync(results))
        console.log("done")
        console.log("geojson send");
        res.send(geojson);
        
      } catch (err) {
        console.error(err);
        res.sendStatus(500);
      }
    }

  });


  // itineraryRouter.get('/:id', async (req, res) => {
  //   // TODO : send a specific layer (through id)
  //   try {
  //     const data = await Itinerary.findOne(req.params.id);
  //     if (!data) res.sendStatus(404);
  //     else res.send(data);
  //   } catch (err) {
  //     console.error(err);
  //     res.sendStatus(500);
  //   }
  // });

  module.exports = itineraryRouter;