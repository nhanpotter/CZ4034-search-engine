# CZ4034 Search Engine

## Deployed IP: <http://172.21.148.177/>

The search engine is already deployed at <http://172.21.148.177/>. Please
use NTU network or connect to NTU VPN first to access it.

## Usage

### Requirements
Please install below requirements:
- python version 3.8+
- pip version 20.0.2+
- Elasticsearch (<https://www.elastic.co/downloads/elasticsearch>)
- ChromeDriver (<https://chromedriver.chromium.org/>)
- Node (<https://nodejs.org/en/download/>)
- Pipenv (<https://pypi.org/project/pipenv/>)
- python 3 venv library (<https://docs.python.org/3/library/venv.html>)
- Rust (<https://www.rust-lang.org/tools/install>)

### Set environment variables
Set these variables in `.env` file at the project root path.
- `API_KEY`: Google Maps API key. A key is already provided in the .env file
- `API_KEY_BACKUP`: Google Maps API key. A key is already provided in the .env file
- `CHROME_DRIVER_PATH`: Absolute path to the downloaded ChromeDriver. Default is `/usr/local/bin/chromedriver`

> **WARNING**: The `API_KEY` and `API_KEY_BACKUP` are already provided in our
> default .env file in our submission. Please do NOT share these keys publicly 
> as this is only for internal uses.

### Instructions to run

1. Open a new terminal. Start Elasticsearch server.
2. Open a new terminal.
   - Navigate to this project root.
   - Run this command to install requirements and sentiment model.
    ```shell
   ./instruct_install_sentiment_model.sh
   ```
   - Run this command to run sentiment model server.
   ```shell
   ./instruct_run_sentiment_model.sh
   ```
3. Open a new terminal.
   - Navigate to this project root.
   - Run this command to install requirements, aspect model, index data to 
     Elasticsearch and build frontend. Please make sure Elasticsearch server is
     running.
   ```shell
   ./instruct_install_search_engine.sh
   ```
   - Run this command to run the search engine
   ```shell
   ./instruct_run_search_engine.sh
   ```
4. Go to <http://127.0.0.1:5000/> on browser.

## Appendix: API Endpoints:
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
3. `/add` - `POST`: Add reviews from TripAdvisor restaurant URL
- `url`: Tripadvisor URL to restaurant
- `count`: Number of reviews to be crawled from the restaurant
4. `/classify` - `POST`: Classify the review using sentiment and aspect model
- `text`: the review text to be classified