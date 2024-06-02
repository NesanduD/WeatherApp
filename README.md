# Weather App README

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Functions](#functions)
7. [Outputs](#outputs)
8. [Contributing](#contributing)
9. [License](#license)

## Introduction
This Weather App is a Python-based tool designed to scrape weather data from multiple sources, calculate the average rain probability, and display the results in a user-friendly tabulated format. The data is specifically gathered for the University of Moratuwa located in Katubedda, Sri Lanka.

## Features
- Scrapes weather data from multiple sources:
  - MSN
  - Weather.com
  - AccuWeather
  - Weather-Atlas
  - DateAndTime.com
- Calculates average rain probability for today and tomorrow, both daytime and nighttime.
- Displays data in a clear tabulated format.

## Prerequisites
- Python 3.x
- The following Python libraries:
  - requests
  - beautifulsoup4
  - fake_headers
  - tabulate

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/weather-app.git
   ```
2. Navigate to the project directory:
   ```bash
   cd weather-app
   ```
3. Install the required libraries:
   ```bash
   pip install requests beautifulsoup4 fake_headers tabulate
   ```

## Usage
Run the script to fetch and display the weather data:
```bash
python weather_app.py
```

## Functions
### Imports
```python
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import sys
import time
import json
from tabulate import tabulate
```
These libraries are used for making HTTP requests, parsing HTML, faking headers for requests, handling JSON data, and formatting output.

### Custom Functions
- **`responses(url)`**: Makes a GET request to the given URL with the specified headers.
- **`status_check(resp)`**: Checks if the response status code is not 200.
- **`average(array_name)`**: Calculates the average of an array of numbers.
- **`connecting_animation()`**: Displays a connecting animation.

## Outputs
The script displays the weather data in a tabulated format, showing the average rain probability for different periods.

Example output:
```
+-----------------+---------------------+-------------------+
|     Period      | Rain Probability (%)| Used sources Count|
+-----------------+---------------------+-------------------+
|  Today Daytime  |        45.67        |         3         |
|  Today Nighttime|        30.50        |         3         |
| Tomorrow Daytime|        55.33        |         3         |
| Tomorrow Nighttime|      40.00        |         3         |
+-----------------+---------------------+-------------------+
```

## Contributing
Contributions are welcome! Please create a pull request or submit an issue if you have any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

By keeping the README focused on the main aspects and adding a section for functions and outputs, you provide necessary information without making the document too lengthy.
