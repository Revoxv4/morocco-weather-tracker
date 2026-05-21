# Morocco Weather Tracker

End-to-end data pipeline that extracts current weather and air quality data for major Moroccan cities, transforms it into analytics-ready formats, and stores it in CSV, JSON, and Parquet.

## Status

🚧 In active development. Building as part of a 6-month data engineering learning roadmap.

## Stack

- **Python 3.13** with Poetry for dependency management
- **requests** — API extraction
- **pandas** + **pyarrow** — transformation and Parquet I/O
- **python-dotenv** — config and secrets management
- **OpenWeatherMap API** — data source

## Architecture (planned)

```
OpenWeatherMap API
        ↓
  src/extract.py  →  data/raw/ (JSON)
        ↓
 src/transform.py →  pandas DataFrames (cleaned)
        ↓
   src/load.py    →  data/processed/ (CSV + Parquet)
```

## Cities tracked

Casablanca, Rabat, Marrakech, Fès, Tangier, Agadir, Meknès, Oujda, Tétouan, Ifrane

## Project structure

```
morocco-weather-tracker/
├── src/
│   ├── extract.py      # Pull from OpenWeatherMap API
│   ├── transform.py    # Clean + reshape with pandas
│   └── load.py         # Persist to CSV / JSON / Parquet
├── data/
│   ├── raw/            # Untouched API responses
│   └── processed/      # Cleaned, analytics-ready outputs
├── logs/               # Run logs
├── config.yaml         # City list + run config
├── main.py             # Pipeline entry point
└── pyproject.toml      # Dependencies
```

## Setup

```bash
poetry install
cp .env.example .env
# Add your OpenWeatherMap API key to .env
poetry run python src/extract.py
```

## Roadmap

- [x] Project structure + dependencies
- [x] Basic API extraction
- [ ] Multi-city extraction with error handling
- [ ] CSV / JSON / Parquet output
- [ ] Logging + configuration
- [ ] Dockerize
- [ ] Schedule with cron / Airflow
- [ ] Load into BigQuery
- [ ] Transform with dbt

## Author

Built by [Revoxv4](https://github.com/Revoxv4) — CS student at Al Akhawayn University.

