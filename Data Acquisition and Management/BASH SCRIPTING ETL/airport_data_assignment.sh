#!/bin/bash

# Downloading the airport data
curl -o airports.dat https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat

# Transforming and loading data
python3 transformation.py airports.dat

# Remove downloaded data
rm airports.dat airport_data_processed.csv

echo "ETL process completed!"
