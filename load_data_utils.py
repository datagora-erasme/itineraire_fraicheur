from owslib.wfs import WebFeatureService
import geopandas as gpd
import os

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


def load_data(url, service_name, version, data_list, path):
    """ load a list of data from one specific service """

    wfs = connection_wfs(url, service_name, version)

    for d_name, d_info in data_list.items():
        print(f"### {d_name} ###")
        box = wfs.contents[f"{d_info['wfs_key']}"].boundingBoxWGS84
        print(f"get {d_name} ..")
        try:
            new_data = wfs.getfeature(typename=f"{d_info['wfs_key']}", bbox=box)
            print(f"SUCCESS")
        except NameError:
            print(f"Error while fetching {d_name} from {service_name}... : {NameError}")

        print(f"writing {d_name} GML file into {path} \n")
        file = open(f"{path}/{d_name}.gml", "wb")
        file.write(new_data.read())
        file.close()

def gml_to_shapefile(input_path, output_path, folder=False):
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
                output_name = filename.replace('.gml', '.shp')
                new_output_path = os.path.join(output_path, output_name)
                
                # Write GeoDataFrame to output Shapefile
                gdf.to_file(new_output_path, driver='ESRI Shapefile')
    else:

        gdf = gpd.read_file(input_path)
        gdf.to_file(output_path, driver='ESRI Shapefile')

    print("Done, all GML files converted into Shapefile")
