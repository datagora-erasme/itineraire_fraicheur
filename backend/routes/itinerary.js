const express = require('express');
const Itinerary = require('../models/data');

const itineraryRouter = express.Router();


itineraryRouter.get('/', async (req, res) => {
    //TODO : send all data awailable (layers)
    try {
      console.log("fetching data ...");
      const results = await Itinerary.findMany();
      console.log("data send");
      res.send(results);
      
    } catch (err) {
      console.error(err);
      res.sendStatus(500);
    }
  });


  itineraryRouter.get('/:id', async (req, res) => {
    // TODO : send a specific layer (through id)
    try {
      const data = await Itinerary.findOne(req.params.id);
      if (!data) res.sendStatus(404);
      else res.send(data);
    } catch (err) {
      console.error(err);
      res.sendStatus(500);
    }
  });

  module.exports = itineraryRouter;