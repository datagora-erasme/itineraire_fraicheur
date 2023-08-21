import os
### GLOBAL VARIABLES OF THE PROJECT ###

base_path = os.path.dirname(os.path.abspath(__file__))

def globpath(path):
    return os.path.join(base_path, path)

### BOUDING LYON METROPOLE PATH ###
bounding_metrop_path = globpath("./score_calculation_it/input_data/bounding_metrop.gpkg")

### NETWORK PATH ###
metrop_network_bouding_path = globpath("./score_calculation_it/input_data/network/metrop_network_bounding.gpkg")

### GRAPH PATH ###
final_network_path = globpath("./score_calculation_it/output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E5Ca0_01.gpkg")
final_network_pickle_path = globpath("./score_calculation_it/output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E5Ca0_01.pickle")
final_network_multidigraph_pickle_path = globpath("./score_calculation_it/output_data/network/graph/final_network_P0_01O5At0_01Ar10C0_01E5Ca0_01_multidigraph.pickle")

### EDGES PATH ###
edges_buffer_path = globpath("./score_calculation_it/input_data/network/edges_buffered_12_bounding.gpkg")
edges_buffer_disolved_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_dissolved_path.gpkg")

edges_buffer_arbres_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_arbres_prop_bounding.gpkg")
edges_buffer_arbustes_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_arbustes_prop_bounding.gpkg")
edges_buffer_prairies_prop_path = globpath("./score_calculation_it/output_data/network/edges/edges_buffered_prairies_prop_bounding.gpkg")


### DATA PATH ###
#### VEGETATION ####
raw_veget_strat_path = globpath("./score_calculation_it/input_data/vegetation/raw_veget_strat.gpkg")
veget_strat_path = globpath("./score_calculation_it/input_data/vegetation/clipped_veget_12.gpkg")
veget_strat_class_folder = globpath("./score_calculation_it/output_data/vegetation/veget_strat/")
clipped_arbres_veget_strat_path = globpath("./score_calculation_it/output_data/vegetation/veget_strat/veget_strat_arbre.gpkg")
clipped_arbustes_veget_strat_path = globpath("./score_calculation_it/output_data/vegetation/veget_strat/veget_strat_arbuste.gpkg")
clipped_prairie_veget_strat_path = globpath("./score_calculation_it/output_data/vegetation/veget_strat/veget_strat_prairie.gpkg")

arbres_align_gpkg_path = globpath("./score_calculation_it/input_data/arbres/arbres.gpkg")
arbres_align_class_folder = globpath("./score_calculation_it/output_data/vegetation/arbres_align/")
class_arbres_align_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/arbres_align_arbre.gpkg")
class_arbustes_align_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/arbres_align_arbuste.gpkg")

arbres_align_buffer_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/class_arbres_align_buffer_2.gpkg")
arbustes_align_buffer_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/class_arbustes_align_buffer_2.gpkg")

clipped_arbres_align_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/clipped_arbres_align.gpkg")
clipped_arbustes_align_path = globpath("./score_calculation_it/output_data/vegetation/arbres_align/clipped_arbustes_align.gpkg")

arbres_align_veget_diff_path = globpath("./output_data/vegetation/arbres_align/diff_arbres_align_veget_2.gpkg")
arbustes_align_veget_diff_path = globpath("./output_data/vegetation/arbres_align/diff_arbustes_align_veget_2.gpkg")

merged_veget_align_arbres_path = globpath("./output_data/vegetation/merged_veget_align_arbres_2.gpkg")
merged_veget_align_arbustes_path = globpath("./output_data/vegetation/merged_veget_align_arbustes_2.gpkg")


### DATA PARAMS ###
data_params = {
    "batiments" : {
        "wfs_key": "metropole-de-lyon:fpc_fond_plan_communaut.fpctoit_2018",
        "gpkg_path": globpath("./score_calculation_it/input_data/batiments/batiments.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/batiments/batiments.json"),
        "onMap": False #should not be displayed on map
    },
    "parcs": {
        "name": "Parcs et jardins",
        "wfs_key": "metropole-de-lyon:com_donnees_communales.comparcjardin_1_0_0",
        "gpkg_path": globpath("./score_calculation_it/input_data/parcs/parcs.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/parcs/parcs.json"),
        "onMap": True,
        "marker_option": {
            "iconUrl": "arbre.svg"
        },
    },
    "parcs_canop": {
        "wfs_key": "metropole-de-lyon:evg_esp_veg.evgparcindiccanope_latest",
        "gpkg_path": globpath("./score_calculation_it/input_data/parcs/parcs_canop.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/parcs/parcs_canop.json"),
        "onMap": False
    },
    "fontaines_potables": {
        "name": "Fontaines potables",
        "wfs_key": "metropole-de-lyon:adr_voie_lieu.adrbornefontaine_latest",
        "gpkg_path": globpath("./score_calculation_it/input_data/fontaines/fontaines_potables.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/fontaines/fontaines_potables.json"),
        "onMap": True,
        "marker_option": {
            "iconUrl": "droplet.svg",
            "iconRetinaUrl": "droplet.svg",
            "popupAnchor": [
                0,
                0
            ],
            "iconSize": [
                40,
                40
            ],
            "clusterCountStyle": "position:absolute;top:20px;left:-9px;color:white;font-weight:bold;"
        },
    },
    "fontaines_ornementales": {
        "name": "Fontaines ornementales",
        "wfs_key": "metropole-de-lyon:adr_voie_lieu.adrfontaineornem_latest",
        "gpkg_path": globpath("./score_calculation_it/input_data/fontaines/fontaines_ornementales.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/fontaines/fontaines_ornementales.json"),
        "onMap": True,
        "marker_option": {
            "iconUrl": "fountain.svg",
            "iconRetinaUrl": "fountain.svg",
            "popupAnchor": [
                0,
                0
            ],
            "iconSize": [
                40,
                40
            ],
            "clusterCountStyle": "position:absolute;top:48px;left:0px;color:black;font-weight:bold;"
        },
    },
    "toilettes": {
        "name": "Toilettes publiques",
        "wfs_key": "metropole-de-lyon:adr_voie_lieu.adrtoilettepublique_latest",
        "gpkg_path": globpath("./score_calculation_it/input_data/toilettes/toilettes.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/toilettes/toilettes.json"),
        "onMap": True,
        "marker_option": {
            "iconUrl": "toilet.svg",
            "iconRetinaUrl": "toilet.svg",
            "popupAnchor": [
                0,
                0
            ],
            "iconSize": [
                40,
                40
            ],
            "clusterCountStyle": "position:absolute;top:48px;left:-6px;color:black;font-weight:bold;"
        },
    },
    "eaux_details": {
        "wfs_key" : "metropole-de-lyon:fpc_fond_plan_communaut.fpcplandeaudetail",
        "gpkg_path": globpath("./score_calculation_it/input_data/eaux/eaux_details.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/eaux/eaux_details.json"),
        "onMap": False
    },
    "eaux_importants": {
        "wfs_key": "metropole-de-lyon:fpc_fond_plan_communaut.fpcplandeau",
        "gpkg_path": globpath("./score_calculation_it/input_data/eaux/eaux_importants.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/eaux/eaux_importants.json"),
        "onMap": False
    },
    "bancs": {
        "name": "Bancs",
        "wfs_key": "metropole-de-lyon:adr_voie_lieu.adrbanc_latest",
        "gpkg_path": globpath("./score_calculation_it/input_data/bancs/bancs.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/bancs/bancs.json"),
        "onMap": True,
        "marker_option": {
            "iconUrl": "bench.svg",
            "iconRetinaUrl": "bench.svg",
            "popupAnchor": [
                0,
                0
            ],
            "iconSize": [
                25,
                25
            ],
            "clusterCountStyle": "position:absolute;top:40px;left:0px;color:white;background-color:#d6eff8;font-weight:bold;"
        },
    },
    "arbres" : {
        "name": "Arbres d'alignement",
        "wfs_key": "metropole-de-lyon:abr_arbres_alignement.abrarbre",
        "gpkg_path": globpath("./score_calculation_it/input_data/arbres/arbres.gpkg"),
        "geojson_path": globpath("./score_calculation_it/input_data/arbres/arbres.json"),
        "onMap": False
    }
}