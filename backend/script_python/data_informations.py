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
        "wfs_key": 'ms:gin_nettoiement.gintoilettepublique',
        "service" : "data.grandlyon_wfs",
    },
    "fontaines_ornementales": {
        "wfs_key": 'ms:adr_voie_lieu.adrfontaineornem_latest',
        "service" : "data.grandlyon_wfs",
    },
    "parcs_jardins_metropole": {
        "wfs_key": 'ms:com_donnees_communales.comparcjardin_1_0_0',
        "service" : "data.grandlyon_wfs",
    },
    "bancs": {
        "wfs_key" : 'ms:adr_voie_lieu.adrbanc_latest',
        "service" : "data.grandlyon_wfs",
    },
    "arbres_alignement" : {
        "wfs_key" : 'ms:abr_arbres_alignement.abrarbre',
        "service" : "data.grandlyon_wfs",
    },
}