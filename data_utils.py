import os
os.environ['USE_PYGEOS'] = '0'
from owslib.wfs import WebFeatureService
import geopandas as gpd
import json

def create_data_informations_file():
    """ Fonction to instantiate data_informations.json file """

    data_informations = {
        "services" : {
            "data.grandlyon_wfs": "https://download.data.grandlyon.com/wfs/grandlyon?SERVICE=WFS&VERSION=2.0.0"
        },
        "data_wfs" : {
            "fontaines_potables": {
                "wfs_key": "ms:epo_eau_potable.epobornefont",
                "service": "data.grandlyon_wfs",
                "buffer_size" : 10
            },
            "toilettes_publiques": {
                "wfs_key": "ms:gin_nettoiement.gintoilettepublique",
                "service": "data.grandlyon_wfs",
                "buffer_size" : 10
            },
            "fontaines_ornementales": {
                "wfs_key": "ms:adr_voie_lieu.adrfontaineornem_latest",
                "service": "data.grandlyon_wfs",
                "buffer_size" : 10
            },
            "parcs_jardins_metropole": {
                "wfs_key": "ms:com_donnees_communales.comparcjardin_1_0_0",
                "service": "data.grandlyon_wfs",
                "buffer_size" : 10
            },
            "bancs": {
                "wfs_key": "ms:adr_voie_lieu.adrbanc_latest",
                "service": "data.grandlyon_wfs",
                "buffer_size" : 10
            },
            "arbres_alignement": {
                "wfs_key": "ms:abr_arbres_alignement.abrarbre",
                "service": "data.grandlyon_wfs",
                "buffer_size" : 10
            },
            # à mettre dans un second temps 
            # "hauteur_batiment": {
            #     "wfs_key": "ms:fpc_fond_plan_communaut.fpctoit_2018",
            #     "service": "data.grandlyon_wfs"
            # }
                
        }
    }
    with open("data_informations.json", "w") as f:
        json.dump(data_informations, f, indent=4)

def create_folder(folder_path):
    exist = os.path.exists(folder_path)
    if not exist:
        os.makedirs(folder_path)
        print(f"{folder_path} created")


def connection_wfs(url, service_name, version):
    """ Return a wfs object after connecting to a service thanks the url provided """
    print(f"Connecting {service_name} WFS ... ")
    wfs=None
    try:
        wfs = WebFeatureService(url, version)
        print(f"SUCCESS : Connected to {service_name}")
    except NameError:
        print(f"Error while connecting to {service_name} ... : {NameError}")

    return wfs


def download_data(service_name, version, path):
    """ load a list of data from one specific service 
        the data are stored in a json file as a dictionnary wich elements have the folowing form : 

        "data_name" : {
            "wfs_key" : 'key',
            "service" : 'service_name',
            "download_path": "path/file.gml"
        }
    """

    with open("data_informations.json", "r") as f:
        data_informations = json.load(f)

    data_wfs = data_informations["data_wfs"]
    services = data_informations["services"]

    wfs = connection_wfs(services[f"{service_name}"], service_name, version)

    for d_name, d_info in data_wfs.items():
        if(d_info["service"] == service_name):

            print(f"### {d_name} ###")

            # the boundingBox define the area where the data should belong to
            box = wfs.contents[f"{d_info['wfs_key']}"].boundingBoxWGS84

            print(f"fetching {d_name} ..")
            try:
                new_data = wfs.getfeature(typename=f"{d_info['wfs_key']}", bbox=box)
                print(f"SUCCESS")
            except NameError:
                print(f"Error while fetching {d_name} from {service_name}... : {NameError}")


            print(f"writing {d_name} GML file into {path} \n")

            #write file into given folder (path)
            file = open(f"{path}/{d_name}.gml", "wb")
            file.write(new_data.read())
            file.close()

            #store download path into data_informations.json
            data_informations["data_wfs"][d_name]["download_path"] = f"{path}/{d_name}.gml"

    # re-write data_informations.json => store all download path
    with open("data_informations.json", "w") as f:
        json.dump(data_informations, f, indent=4)

def convert_gml(input_path, output_path, driver, extension='.gpkg', folder=False):
    """Convert GML file into shapefile.
    If folder = TRUE, all of the GML files of the given folder are converted to shapefile. 
    Careful about the path : either a folder or a file one. 
    """
    print("converting ... ")
    if(folder):
        for filename in os.listdir(input_path):
            print(f"filename : {filename}")
            if filename.endswith('.gml'):
                # Read input GML file into a GeoDataFrame
                gdf = gpd.read_file(os.path.join(input_path, filename))
                
                # Set output file path and name
                output_name = filename.replace('.gml', extension)
                new_output_path = os.path.join(output_path, output_name)
                
                # Write GeoDataFrame to output Shapefile
                gdf.to_file(new_output_path, driver=driver)

                print("Done, all GML files converted into GPKG")
    else:

        gdf = gpd.read_file(input_path)
        gdf.to_file(output_path, driver=driver)
        print(f"Done, {input_path} converted into GPKG")
    

def convert_all_gml(output_path_folder):

    """Convert all data stored in data_informations from GML to Shapefile"""

    with open("data_informations.json", "r") as f:
        data_informations = json.load(f)
    
    data_wfs = data_informations['data_wfs']
    for d_name, d_info in data_wfs.items():
        download_path = d_info["download_path"]
        if(download_path.endswith(".gml")):
            gpkg_path = f"{output_path_folder}{d_name}.gpkg"
            convert_gml(download_path, gpkg_path, driver="GPKG")
            data_informations["data_wfs"][d_name]["gpkg_path"] = gpkg_path

    with open("data_informations.json", "w") as f:
        json.dump(data_informations, f, indent=4)

def points_to_polygon(point_path, polygon_path, buffer_size):
    """
        Computes the convex hull of a point shapefile and converts it to a polygon shapefile
    """

    points = gpd.read_file(point_path)

    # change temporarily the CRS (projection system) because buffering need meter
    points.to_crs(epsg=3857)

    # Create a buffer around each point
    buffered_points = points.to_crs(epsg=3857).buffer(buffer_size)

    # Convert the buffered points to polygons
    polygons = buffered_points.geometry.apply(lambda x: x.convex_hull)

    # Create a new GeoDataFrame with the polygon geometry and any additional attributes from the original points shapefile
    polygon_gdf = gpd.GeoDataFrame(points.drop('geometry', axis=1), geometry=polygons, crs=3857)

    final_polygon = polygon_gdf.to_crs(epsg=4171)

    final_polygon.to_file(polygon_path, driver="GPKG")

def convert_all_points_into_polygons(output_path_folder):
    """ Convert all shapefile with Points Type into Polygons """

    with open("data_informations.json", "r") as f:
        data_informations = json.load(f)

    for d_name, d_info in data_informations["data_wfs"].items():
        original_gpkg_file = gpd.read_file(d_info["cleaned_data_path"])
        if(original_gpkg_file.geom_type[0] == "Point"):
            buffered_path = f"{output_path_folder}{d_name}_buffered.gpkg"

            print(f"Converting {d_name} into Polygons ... ")

            points_to_polygon(d_info["cleaned_data_path"], buffered_path, d_info["buffer_size"])
            data_informations["data_wfs"][d_name]["buffered_path"] = buffered_path
    
    with open("data_informations.json", "w") as f:
        json.dump(data_informations, f, indent=4)
            

def get_attributes_list(file_path):
    file = gpd.read_file(file_path)
    attribute_list = list(file.columns)
    return(attribute_list)

def write_all_atributes():
    """ Write into data_informations.json all attributes of the layer """

    print("Writing all attributes into data_informations.json file ...")

    with open("data_informations.json", "r") as f:
        data_informations = json.load(f)

    data_wfs = data_informations['data_wfs']
    for d_name, d_info in data_wfs.items():
        #the shape file is the original file containing all attributes
        file_path = data_wfs[d_name]["gpkg_path"]
        attribute_list = get_attributes_list(file_path)
        print(f"{d_name} = {attribute_list}")
        data_informations["data_wfs"][d_name]["all_attributes"] = attribute_list

    with open("data_informations.json", "w") as f:
        json.dump(data_informations, f, indent=4)

    print("DONE")

def write_attributes_to_add_and_remove(data_name, attributes_to_add, attributes_to_remove):
    """ Write into data_informations.json all attributes to add or remove for one data
        attributes_to_add is a dictionnary with the pair key, values, 
        attributes_to_remove is a list of attributes

        attributes_to_add = {
            attribute1 : default_value1
            attribute2 : default_value2
        }
        attributes_to_remove = ["attribute1", "attribute2"]
    """

    with open("data_informations.json", "r") as f: 
        data_informations = json.load(f)

    data_informations['data_wfs'][data_name]['attributes_to_remove'] = attributes_to_remove
    data_informations['data_wfs'][data_name]['attributes_to_add'] = attributes_to_add

    with open("data_informations.json", "w") as f:
        json.dump(data_informations, f, indent=4)
    



def remove_attributes(input_path, output_path, attributes_to_remove):
    file = gpd.read_file(input_path)
    file = file.drop(attributes_to_remove, axis=1)
    file.to_file(output_path)

def add_attributes(input_path, output_path, attributes_to_add):
    """attributes_to_add should be a dictionnary with the following structure : 
    
    attributes_to_add = {
        'new_attribute1': [1, 2, 3],
        'new_attribute2': ['a', 'b', 'c']
    }
    
    """
    file = gpd.read_file(input_path)

    for attribute_name, values in attributes_to_add.items():
        file[attribute_name] = values
    
    file.to_file(output_path)



def remove_and_add_attributes(output_path_folder):
    """ """

    with open("data_informations.json", "r") as f:
        data_informations = json.load(f)

    data_wfs = data_informations["data_wfs"]
    for d_name, d_info in data_wfs.items():
        print(f"Remove and Add attributes for {d_name}")
        input_path = d_info["gpkg_path"]
        output_path = f"{output_path_folder}{d_name}_cleaned.gpkg"
        remove_attributes(input_path, output_path, d_info["attributes_to_remove"])
        add_attributes(output_path, output_path, d_info["attributes_to_add"])

        data_informations["data_wfs"][d_name]["cleaned_data_path"] = output_path
    
    with open("data_informations.json", "w") as f:
        json.dump(data_informations, f, indent=4)
