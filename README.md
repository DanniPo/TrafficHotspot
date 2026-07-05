# TrafficHotspot

Spatial clustering project for Chicago traffic crashes using HDBSCAN.

## Included files

- `Cali.ipynb`: full exploratory notebook workflow
- `generate_clusters_map.py`: script version that creates an interactive cluster map
- `requirements.txt`: Python dependencies

## Setup

```bash
pip install -r requirements.txt
```

## Run script

```bash
python generate_clusters_map.py
```

Notes:
- Update `CSV_PATH` in `generate_clusters_map.py` to your local crash CSV file.
- Generated HTML map files are intentionally gitignored.
