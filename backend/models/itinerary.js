const {spawn} = require("child_process");

module.exports.calculateItinerary = (start, end) => {
    console.log("python")
    const pythonItineraryCalculation = spawn('python', ["calculate_itinerary.py", start.lat, start.lon, end.lat, end.lon])
    let test;
    pythonItineraryCalculation.stdout.on('data', (data) => {
        console.log("test")
        test = data.toString()
        // jsonResults = data.toJson()
        // console.log(jsonResults)
        // console.log(JSON.parse(data.toString()))
    })

    pythonItineraryCalculation.stderr.on('data', data => {
        console.error(`error : ${data}`)
    })


    pythonItineraryCalculation.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        console.log(test)
        });
    return test
}
