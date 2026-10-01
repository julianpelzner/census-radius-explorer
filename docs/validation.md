# Validation and testing spec

This is the single source of truth for data checks and test expectations in census-radius-explorer. `validate.py` and `tests/` implement what's here. If this file and the code disagree, fix one in the same PR.

## Validation

`validate.py` returns a report in which each entry is `{check, level, passed, detail}`.

- **Hard** failures raise `ValidationError`, and the app shows the message instead of a map.
- **Soft** failures are only recorded as warnings in the report.

### Hard checks

| Check | Stage |
| --- | --- |
| Geocode returned exactly one US location (ambiguous → show candidates) | geocode |
| `0 < radius <= max_radius_mi` from config | input |
| At least one area selected, or the containing-area fallback was used | scope |
| GEOID is unique, a string, and 11 characters (tract) or 5 (ZCTA) | transform |
| Required columns present with expected dtypes (one pandera schema per geography level) | transform |
| No Census sentinel negatives remain (e.g. -666666666) | transform |
| Derived rates fall within [0, 1] | transform |
| Every selected tract GEOID was returned by the API | join |
| Every pandas merge passes `validate="one_to_one"` | join |
| Geometry is valid and output CRS is EPSG:4326 | join |

### Soft checks

| Check | Stage |
| --- | --- |
| Selected ZCTAs missing from the API response (a few have no ACS data) | join |
| Null share per column above `max_null_share` from config | transform |

## Testing

- Unit-test pure functions; mock all HTTP. Tests never call the live API.
- Fixtures live in `tests/fixtures/`: small API JSON samples and tiny GeoJSON shapes.
- Center-inside tests must cover:
  - an area fully inside the circle (kept)
  - an area fully outside (dropped)
  - an area straddling the edge (kept only if its interior point is inside)
  - an irregular shape whose plain centroid falls outside the shape itself (`representative_point()` must handle it)
  - zero qualifying areas, which triggers the containing-area fallback
- Every hard check gets one passing test and one failing test.
- Every soft check gets one test confirming it warns without raising.

## Definition of done

A change is done when `pytest` passes, `ruff check .` is clean, and any check added or changed is reflected in this file.
