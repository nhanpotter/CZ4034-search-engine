# CZ4034-search-engine

## Endpoints:
1. `/list` - `GET`: Get list of restaurants
2. `/query` - `POST`:
- `query`: term to search
- `res_ids` **(Optional)**: list of restaurant ids (e.g. `[0, 5, 10]`). If 
  omitted, query all.
- `sentiments` **(Optional)**: list of sentiments (e.g. `[0, 1]`). If omitted, 
  query all.
    - `0`: Negative
    - `1`: Neutral
    - `2`: Positive