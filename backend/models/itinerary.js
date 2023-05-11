let uniqid = require("uniqid")

const { spawn } = require("child_process");

module.exports.pythonCalculateItinerary = function (start, end) {
  //TODO : create a unique id path for the temp file itinerary + send it to python

  path_length = "./temp/sp_length_" + uniqid()
  path_if = "./temp/sp_if_" +uniqid()

  return new Promise((resolve, reject) => {
    const pythonItineraryCalculation = spawn("python", [
      "calculate_itinerary.py",
      start.lat,
      start.lon,
      end.lat,
      end.lon,
      path_length,
      path_if
    ]);
    let result;

    pythonItineraryCalculation.stdout.on("data", (data) => {
      result = data
    });

    pythonItineraryCalculation.stderr.on("data", (data) => {
      console.error(`error : ${data}`);
      reject(data);
    });

    pythonItineraryCalculation.on("close", (code) => {
      console.log(`child process close all stdio with code ${code}`);
      resolve(JSON.parse(result));
    });
  });
};

// module.exports.calculateItinerary = (start, end) => {
//   return new Promise(function (resolve, reject) {
//     pythonCalculateItinerary(start, end)
//       .then((itineraries) => {
//         console.log("model :", itineraries)
//         resolve(itineraries);
//       })
//       .catch((err) => {
//         console.error("error calculating itinerary", err);
//         reject(err);
//       });
//   });
// };
