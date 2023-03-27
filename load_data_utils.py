from owslib.wfs import WebFeatureService
from data import services, data_wfs

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

