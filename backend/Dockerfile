FROM python:3.10.8-buster

RUN apt update
RUN apt install gdal-bin -y

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./models/ /app/models
COPY ./script_python/ /app/script_python
COPY ./data/osm/final_network_30_05_debug.gpkg /app/data/osm/final_network_30_05_debug.gpkg
COPY ./data/geojson /app/data/geojson
COPY ./data/data_informations.json /app/data/data_informations.json
# COPY ./raw_data/ /app/raw_data

COPY ./calculate_itinerary.py /app/
COPY ./load_network.py /app/
COPY ./app.py /app/




#CMD ["Flask", "run", "-h", "0.0.0.0", "-p", "3002",]

CMD ["python", "app.py"]