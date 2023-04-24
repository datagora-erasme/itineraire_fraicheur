const { spawn } = require("child_process");

const pythonCalculateItinerary = function (start, end) {
  //TODO : create a unique id path for the temp file itinerary + send it to python

  return new Promise((resolve, reject) => {
    const pythonItineraryCalculation = spawn("python", [
      "script_python/calculate_itinerary.py",
      start.lat,
      start.lon,
      end.lat,
      end.lon,
    ]);
    let test;

    pythonItineraryCalculation.stdout.on("data", (data) => {
      console.log("test");
      test = data.toString();
    });

    pythonItineraryCalculation.stderr.on("data", (data) => {
      console.error(`error : ${data}`);
      reject(data);
    });

    pythonItineraryCalculation.on("close", (code) => {
      console.log(`child process close all stdio with code ${code}`);
      console.log(test);
      resolve(test);
    });
  });
};

module.exports.calculateItinerary = (start, end) => {
  return new Promise(function (resolve, reject) {
    pythonCalculateItinerary(start, end)
      .then((itinerary) => {
        console.log("itinerary : ", itinerary);
        resolve(itinerary);
      })
      .catch((err) => {
        console.error("error calculating itinerary", err);
        reject(err);
      });
  });
};
