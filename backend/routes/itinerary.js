const express = require('express');
const Itinerary = require('../models/itinerary');
const fs = require("fs")

const itineraryRouter = express.Router();


itineraryRouter.get('/', async (req, res) => {
    if(req.query.start && req.query.end){
      try {
        console.log("calculating itinerary ...");
        let results = await Itinerary.pythonCalculateItinerary(req.query.start, req.query.end);
        console.log("Itineraries routes : ", results)
        // pathLength = results[0]
        // pathIf = results[1]

        // const geoJsonLength = JSON.parse(fs.readFileSync(pathLength))
        // const geoJsonIf = JSON.parse(fs.readFileSync(pathIf))

        res.send([
          {
            geojson: results, 
            color: "blue"
          }
        ])

        // res.send([
        //   {
        //     geojson: geoJsonLength,
        //     color: "red"
        //   },
        //   {
        //     geojson: geoJsonIf,
        //     color: "blue"
        //   }
        // ])

        console.log("Itineraries send")
        //TODO remove files
        // fs.unlink(pathLength)
        // fs.unlink(pathIf)
        // console.log("Files deleted")
        
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