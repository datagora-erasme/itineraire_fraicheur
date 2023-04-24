import sys
from calculate_itinerary_utils import shortest_path

startLat = float(sys.argv[1])
startLon = float(sys.argv[2])

endLat = float(sys.argv[3])
endLon = float(sys.argv[4])

start = (startLat, startLon)
end = (endLat, endLon)

# print(start, end)
temp_path = "./temp/temp_sp.json"

shortest_path("./script_python/data/osm/lyon_drive.gpkg", temp_path, origin_point=start, destination_point=end, weight="IF")

print(temp_path)

sys.stdout.flush()