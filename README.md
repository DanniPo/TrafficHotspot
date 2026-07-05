# TrafficHotspot

Spatial clustering project for Chicago traffic crashes using HDBSCAN.

## Dataset

The raw crash dataset is too large to keep in this repository.

- Source: https://data.cityofchicago.org/Transportation/Traffic-Crashes-Crashes/85ca-t3if
- Download CSV and save it locally (for example in a local `data/` folder).
- Keep dataset files out of git and reference the local path in your notebook/script.

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
- Local dataset files are intentionally gitignored.
