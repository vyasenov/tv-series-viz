# tv-series-viz

Interactive visualizations of TV series episode ratings. The Streamlit app lets you compare shows side-by-side on a normalized season timeline with LOWESS smoothing. Utility scripts can also generate static heatmaps and time series PNGs.

### Quick start

Requires Python 3.10+.

```bash
# 1) Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the Streamlit app
streamlit run code/streamlit_app.py
```

Then open the URL from the terminal (typically `http://localhost:8501`).

### What you can do

- Compare multiple shows at once via a multi-select.
- View ratings along a continuous season axis with vertical boundaries between seasons.
- See smoothed trends per season using LOWESS.
- Hover for precise values; dark-themed Plotly visuals.

### Data format

CSV files live in `data/` and must follow this naming pattern and schema:

- Filename: `<show_name>_ratings.csv` (lowercase with underscores)
- Columns: `episode, season, rating`

Example:

```csv
episode,season,rating
1,1,7.8
2,1,7.6
3,1,7.6
```

The app automatically discovers available shows by scanning `data/` for files ending with `_ratings.csv`.

### Add a new show

1. Create `data/<your_show>_ratings.csv` with the schema above.
2. Run or refresh the app. The show will appear in the selector automatically.

### Generate static charts (optional)

You can create PNGs in `graphs/` using the helper scripts:

```bash
# Heatmaps per show (saved to graphs/heatmaps/)
python code/heatmaps.py

# Time series per show (saved to graphs/time_series/)
python code/time_series.py
```

### Project structure

```text
.
├── code/
│   ├── streamlit_app.py       # Interactive Streamlit app (Plotly)
│   ├── heatmaps.py            # Generates per-show episode heatmaps (Seaborn)
│   └── time_series.py         # Generates per-show time series (Matplotlib)
├── data/                      # CSVs named <show>_ratings.csv
├── graphs/
│   ├── heatmaps/              # Output PNGs from heatmaps.py
│   └── time_series/           # Output PNGs from time_series.py
├── requirements.txt
└── README.md
```

### Notes

- The app uses absolute paths relative to the repository to find `data/`.
- LOWESS smoothing is provided by `statsmodels`.
- Plotly color palettes are chosen to work well on dark backgrounds.

### Author

Created by Vasco Yasenov — `https://vyasenov.github.io/`.