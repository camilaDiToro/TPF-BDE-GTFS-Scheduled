#!/bin/bash

export PGUSER=postgres
export PGPASSWORD=admin
export PGDATABASE=transport_ny

REGIONS=("brooklyn" "bronx" "queens" "island" "busco")
DIRS=("gtfs_b" "gtfs_bx" "gtfs_q" "gtfs_si" "gtfs_busco")

echo "Importing GTFS data into PostgreSQL..."
echo "Importing manhattan GTFS data..."

npm exec -- gtfs-to-sql --require-dependencies -- ./gtfs_m/*.txt | psql --host=localhost --port=5432 -U postgres -b

for i in "${!REGIONS[@]}"; do
  REGION=${REGIONS[$i]}
  DATASET_DIR=${DIRS[$i]}

  echo "Importing $REGION GTFS data..."
  npm exec -- gtfs-to-sql --require-dependencies --schema $REGION -- $DATASET_DIR/*.txt | psql --host=localhost --port=5432 -U postgres -b

done