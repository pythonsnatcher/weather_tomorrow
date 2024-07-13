# 🌦️ Weather Data Retrieval and Integration 

This project includes Python scripts designed to retrieve weather data from multiple websites and integrate them into a single dataset. The collected data encompasses various meteorological parameters such as temperature, humidity, wind speed, and more, from sources like The Weather Outlook, BBC Weather, Met Office, and weather.com.

## Scripts

### 1. `get_data.py` 📊

#### Purpose:
This script fetches weather data from multiple sources, combines it into a structured format, and then writes the combined data into a CSV file.

#### Usage:
- **Dependencies:** Ensure you have Python installed (preferably Python 3) with the necessary libraries (`requests`, `lxml`).
- **Setup:** Replace the URLs in the script (`url_weather_outlook`, `url_bbc_weather`, `url_met_office`, `url_weather_com`) with the URLs corresponding to your desired locations and dates.
- **Execution:** Run the script. It will fetch weather data from each source, combine it into a dictionary (`combined_weather_data`), and then write this data to a CSV file named `weather_tomorrow.csv`.

#### Features:
- **Error Handling:** Includes basic error handling to manage exceptions that might occur during web scraping or data extraction.
- **XPath Usage:** Utilizes XPath expressions to navigate and extract specific elements from the HTML structure of each webpage.
- **Data Integration:** Combines weather data from multiple sources into a single dataset, making it easier to analyze or visualize.

### 2. `GUI.py` 🖥️

#### Purpose:
This script provides a graphical user interface (GUI) for interacting with weather data. It utilizes the `get_data.py` script to fetch and display weather information.

#### Usage:
- **Dependencies:** Requires Python with `tkinter` (standard Python GUI toolkit) installed.
- **Execution:** Run the script. It will launch a GUI window where users can view and interact with weather data fetched using `get_data.py`.

#### Features:
- **User Interface:** Provides a visual interface for users to easily view weather data without needing to run scripts or interact directly with the command line.
- **Integration:** Utilizes the functionality of `get_data.py` to ensure real-time updates and accuracy in displayed weather information.

---

### Notes:

- **XPath Considerations:** XPath expressions used in `get_data.py` are sensitive to changes in the structure of the webpages. Ensure they are updated if the structure of the target websites changes.
- **Data Integrity:** Validate and preprocess data as needed (e.g., numeric extraction, handling missing values) to ensure the accuracy and consistency of the collected weather data.
- **Documentation:** For further details on specific functions or utilities (`extract_numeric_value`, error handling approaches, etc.), refer to the inline comments within the scripts.

By using these scripts, you can automate the retrieval and integration of weather data from various sources and provide a user-friendly interface for accessing this information.

---

This README provides an overview of how to use and understand the provided scripts for retrieving weather data and utilizing a graphical user interface (GUI) for interaction. Adjustments may be needed based on specific requirements or updates to the web sources accessed.
