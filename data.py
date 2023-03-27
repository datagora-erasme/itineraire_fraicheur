services = {
    "data.grandlyon_wfs" : "https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0"
}

data_wfs = {
    "fontaines_potables" : {
        "wfs_key" : 'ms:epo_eau_potable.epobornefont',
        "service" : "data.grandlyon_wfs",
        "version" : "2.0.0",
        "request" : "GetFeature",
        "typename" : "epo_eau_potable.epobornefont",
        "srsname" : "EPSG:4171",
        "outputFormat" : "application/shapefile",
        "count": "100",
        "startIndex" : 0
    }
}