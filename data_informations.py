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
    }, 
    "toilettes_publiques" : {
        "wfs_key": 'ms:gin_nettoiement.gintoilettepublique'
    },
    "fontaines_ornementales": {
        "wfs_key": 'ms:adr_voie_lieu.adrfontaineornem_latest'
    },
    "parcs_jardins_metropole": {
        "wfs_key": 'ms:com_donnees_communales.comparcjardinpct'
    },
    "bancs": {
        "wfs_key" : 'ms:adr_voie_lieu.adrbanc_latest'
    },
    "arbres_alignement" : {
        "wfs_key" : 'ms:abr_arbres_alignement.abrarbre'
    },
}