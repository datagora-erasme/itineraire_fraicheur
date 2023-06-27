FROM python:3.10.8-buster

RUN apt update
RUN apt install gdal-bin -y

WORKDIR /app

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./models/ /app/models
# COPY ./script_python/ /app/script_python
COPY ./score_calculation/input_data /app/score_calculation/input_data
COPY ./score_calculation/output_data/network/graph/final_network_2706.gpkg /app/score_calculation/output_data/network/graph/final_network_2706.gpkg
# COPY ./data/geojson /app/data/geojson
COPY ./data_informations.json /app/data_informations.json
# COPY ./raw_data/ /app/raw_data

COPY ./calculate_itinerary.py /app/
COPY ./load_network.py /app/
COPY ./app.py /app/




#CMD ["Flask", "run", "-h", "0.0.0.0", "-p", "3002",]

CMD ["python", "app.py"]