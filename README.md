# Meteor Helpers

Meteor Helpers is a Python-based tool for fetching, storing, and visualizing weather data. It retrieves historical weather data and forecasts from an API, stores them in a Cassandra database, and plots the data for analysis.
This repository is a part of the Meteor project on Bittensor, dedicated to breakthroughs in metorology, climatology, and extreme weather event prediction through incentivized AI and distributed comuting. To learn more, see https://github.com/opentensor/bittensor

## Features

- Fetch weather forecasts and historical data.
- Store weather data in a Cassandra database.
- Plot weather data for comparison and analysis.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x installed
- Access to a Cassandra database
- An internet connection to fetch data from the weather API

## Installation

Clone the repository to your local machine:

```bash
git clone https://github.com/sakrobinson/meteor-helpers.git
```

Navigate to the repository directory:

```bash
cd meteor-helpers
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

To run the main script which fetches and stores weather data:

```bash
python3 run.py
```

To plot the forecasts and historical data:

```bash
python3 plot_forecasts.py
```

## Configuration

- Update `worldcities_sample.csv` with the cities you want to fetch weather data for. Cities data provided by SimpleMaps: https://simplemaps.com/data/world-cities
- Ensure the Cassandra cluster IPs in `run.py` match your Cassandra setup.
- Modify the date range in `get_forecast.py` to fetch the desired forecast period.

## Contributing

Contributions to Meteor Helpers are welcome. Please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

Project Link: https://github.com/sakrobinson/meteor-helpers
```
