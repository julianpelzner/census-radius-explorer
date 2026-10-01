# census-radius-explorer

## What this project does
A Streamlit app: the user enters a US city or address, a radius in miles, and a
geography level (census tracts or ZCTAs). The app geocodes the location, buffers it,
selects areas whose interior point falls inside the circle, pulls ACS 5-year data
for only those areas, validates it, and maps it with downloads.

## Stack
Python 3.11+, pandas, geopandas, pygris, requests, geopy, pandera, pyarrow,
streamlit, folium, streamlit-folium, pyyaml. Dev: pytest, ruff.

## Layout
- app/streamlit_app.py: UI only; calls census_radius_explorer.pipeline.run()
- src/census_radius_explorer/: one module per step (config, geocode, scope,
  extract_acs, extract_shapes, cache, transform, validate, join_geo, pipeline)
- run_pipeline.py: CLI wrapper around pipeline.run()
- scripts/build_reference.py: one-time national county + ZCTA GeoParquet build
- config/pipeline.yaml: ACS year, variables, max radius, cache paths
- tests/: pytest, small fixtures only, no live API calls
- docs/validation.md: validation checks and testing spec

## Rules
- Never hard-code ACS years, variables or radius limits; read config/pipeline.yaml.
- GEOIDs are always strings (tract = 11 chars, ZCTA = 5). Never cast to int.
- Every pandas merge uses validate="one_to_one" (or the correct relationship).
- Buffer and select in EPSG:5070; output in EPSG:4326.
- Center-inside rule: keep an area if geometry.representative_point() is within
  the buffer; if none qualify, fall back to the area containing the point.
- Census sentinel negatives (e.g. -666666666) become nulls in transform.
- Every API call and shape download goes through cache.py.
- Read CENSUS_API_KEY from env or st.secrets; never print or commit it.
- Type hints and docstrings on public functions; keep functions small.

## Validation and testing
Follow the spec in @docs/validation.md. When you add or change a check,
update that file in the same change.

## How to work with me
- Work on one module per request; don't touch unrelated files.
- Add or update tests with every change and run pytest before finishing.
- Ask before adding a dependency or changing the config schema.
- Done means: pytest passes and ruff check is clean.

## Commands
- Install: pip install -e ".[dev]"
- Test: pytest
- Lint: ruff check .
- App: streamlit run app/streamlit_app.py
- CLI: python run_pipeline.py --location "Denver, CO" --radius 10 --geo tract
