const express = require('express');
const Data = require('../models/data');

const dataRouter = express.Router();


dataRouter.get('/', async (req, res) => {
    if(req.query.id){
        try {
          const data = await Data.findOne(req.query.id);
          if (!data) res.sendStatus(404);
          else res.send(data);
        } catch (err) {
          console.error(err);
          res.sendStatus(500);
        }
    } else {
        try {
          const results = await Data.findMany();
          res.setHeader('Content-Type', 'application/json')
          res.send(results);
        } catch (err) {
          console.error(err);
          res.sendStatus(500);
        }
    }

  });


// dataRouter.get('/:id', async (req, res) => {
//   try {
//     const data = await Data.findOne(req.params.id);
//     if (!data) res.sendStatus(404);
//     else res.send(data);
//   } catch (err) {
//     console.error(err);
//     res.sendStatus(500);
//   }
// });

  module.exports = dataRouter;