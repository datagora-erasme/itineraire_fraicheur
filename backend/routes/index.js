const dataRouter = require('./data');
const itineraryRouter = require('./itinerary');

const setupRoutes = (app) => {
  app.use('/data', dataRouter);
  app.use('/itinerary', itineraryRouter);
};

module.exports = {
  setupRoutes,
};