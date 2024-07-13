import requests
from lxml import html
import csv

def weather_com_(url, xpath_expression):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.encoding = 'utf-8'  # Set the encoding explicitly to utf-8
        tree = html.fromstring(response.content)

        # Extract chance of rain using XPath expression
        chance_of_rain = tree.xpath(xpath_expression)
        
        if chance_of_rain:
            # Since we're expecting a single element with the percentage value,
            # we directly extract the text content of the element and strip whitespace
            chance_of_rain_text = chance_of_rain[0].text_content().strip()
            # Remove the percentage sign
            chance_of_rain_value = chance_of_rain_text.replace('%', '')
            return chance_of_rain_value
        else:
            return "Chance of rain not found on the webpage."

    except Exception as e:
        print(f"Error fetching chance of rain from {url}: {e}")
        return None

def the_weather_outlook(url):
    try:
        # Define XPath expressions for weather outlook
        xpath_date = '//*[@id="2"]/td[1]/div/text()'           # XPath for date
        xpath_high_temp = '//*[@id="2"]/td[3]/span/text()'     # XPath for high temperature
        xpath_wind_speed = '//*[@id="2"]/td[4]/span/text()'    # XPath for wind speed
        xpath_humidity = '//*[@id="2"]/td[7]/text()'           # XPath for humidity
        xpath_pressure = '//*[@id="2"]/td[8]/text()'           # XPath for pressure
        xpath_rain_total = '//*[@id="rt2"]/text()'             # XPath for rain total
        xpath_wind_gust = '//*[@id="2"]/td[6]/span/text()'     # XPath for wind gust
        
        # Fetch the webpage content
        response = requests.get(url)
        response.encoding = 'utf-8'  # Set the encoding explicitly to utf-8
        tree = html.fromstring(response.content)
        
        # Extract data using XPath
        date = tree.xpath(xpath_date)[0].strip()
        high_temp_text = tree.xpath(xpath_high_temp)[0].strip()  # Get high temperature as text
        wind_speed_text = tree.xpath(xpath_wind_speed)[0].strip()  # Get wind speed as text
        humidity_text = tree.xpath(xpath_humidity)[0].strip()  # Get humidity as text
        pressure_text = tree.xpath(xpath_pressure)[0].strip()  # Get pressure as text
        rain_total_text = tree.xpath(xpath_rain_total)[0].strip()  # Get rain total as text
        
        # Extract numeric values from extracted text
        high_temp = extract_numeric_value(high_temp_text)
        wind_speed = extract_numeric_value(wind_speed_text)
        humidity = extract_numeric_value(humidity_text.rstrip('%'))  # Strip trailing '%' from humidity
        pressure = extract_numeric_value(pressure_text)
        rain_total = extract_numeric_value(rain_total_text.rstrip('mm'))  # Strip 'mm' from rain total
        
        # Extract wind gust
        wind_gust_text = tree.xpath(xpath_wind_gust)[0].strip()  # Get wind gust as text
        wind_gust = extract_numeric_value(wind_gust_text)
        
        # Prepare and return the extracted data as a dictionary
        weather_data = {
            'Location': 'London',
            'Date': date,
            'High Temperature(C)': high_temp,
            'Wind Speed(mph)': wind_speed,
            'Humidity(%)': humidity,
            'Pressure(mb)': pressure,
            'Rain Total (mm)': rain_total,
            'Wind Gust(mph)': wind_gust  # Include wind gust in the dictionary
        }
        
        return weather_data
    
    except Exception as e:
        print(f"Error fetching weather data from The Weather Outlook: {e}")
        return None

def extract_numeric_value(text):
    """
    Function to extract numeric value from text.
    Returns None if numeric value cannot be extracted.
    """
    try:
        # Remove non-numeric characters except for '.' to handle decimal values
        numeric_text = ''.join(filter(lambda x: x.isdigit() or x == '.', text))
        numeric_value = float(numeric_text) if '.' in numeric_text else int(numeric_text)
        return numeric_value
    except ValueError:
        return text  # Return original text if numeric extraction fails

def get_bbc_weather_data(url):
    try:
        # Define XPath expressions for BBC weather
        xpath_tomorrow_pollen = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[2]/span[1]/span[1]/span[2]/text()'
        xpath_tomorrow_uv = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[2]/span[2]/span[1]/span[2]/text()'
        xpath_sunrise = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[1]/span[1]/span[2]/text()'
        xpath_sunset = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[1]/span[2]/span[2]/text()'
        xpath_weather_description = '//*[@id="daylink-1"]/div[4]/div[2]/div/text()'  # XPath for weather description

        # Fetch the webpage content
        response = requests.get(url)
        response.encoding = 'utf-8'  # Set the encoding explicitly to utf-8
        tree = html.fromstring(response.content)

        # Extract tomorrow's pollen, UV, sunrise, sunset, and weather description using XPath
        tomorrow_pollen = tree.xpath(xpath_tomorrow_pollen)[0].strip()
        tomorrow_uv = tree.xpath(xpath_tomorrow_uv)[0].strip()
        sunrise_time = tree.xpath(xpath_sunrise)[0].strip()
        sunset_time = tree.xpath(xpath_sunset)[0].strip()
        weather_description = tree.xpath(xpath_weather_description)[0].strip()

        # Prepare and return the extracted data as a dictionary
        bbc_weather_data = {
            'Pollen': tomorrow_pollen,
            'UV': tomorrow_uv,
            'Sunrise': sunrise_time,
            'Sunset': sunset_time,
            'Weather Description': weather_description  # Include weather description in the dictionary
        }
        
        return bbc_weather_data
    
    except Exception as e:
        print(f"Error fetching weather data from BBC Weather: {e}")
        return None

def get_met_office_weather_data(url):
    try:
        # Define XPath expressions specific to Met Office
        xpath_low_temp = '//*[@id="dayTab1"]/div/div[1]/div[1]/div/div[2]/span[3]/text()'  # XPath for low temperature

        # Fetch the webpage content
        response = requests.get(url)
        response.encoding = 'utf-8'  # Set the encoding explicitly to utf-8
        tree = html.fromstring(response.content)

        # Extract data using XPath
        low_temp_text = tree.xpath(xpath_low_temp)[0].strip()  # Get low temperature as text

        # Extract numeric value from extracted text
        low_temp = extract_numeric_value(low_temp_text)

        # Prepare and return the extracted data as a dictionary
        met_office_weather_data = {
            'Low Temperature(C)': low_temp
        }

        return met_office_weather_data

    except Exception as e:
        print(f"Error fetching weather data from Met Office: {e}")
        return None

def fetch_moon_data(url):
    try:
        # Define XPath expression for moon phase
        xpath_moon_phase = '//*[@id="upcomingmoonphases"]/div/div/div[1]/div[3]/text()'

        # Fetch the webpage content
        response = requests.get(url)
        response.encoding = 'utf-8'  # Set the encoding explicitly to utf-8
        tree = html.fromstring(response.content)

        # Extract moon phase using XPath
        moon_phase = tree.xpath(xpath_moon_phase)
        if moon_phase:
            moon_phase_text = moon_phase[0].strip()  # Strip whitespace
            return moon_phase_text
        else:
            return "Moon phase not found on the webpage."

    except Exception as e:
        print(f"Error fetching moon data: {e}")
        return None

# Function to get combined weather data from multiple sources
def get_combined_weather_data(url_weather_outlook, url_bbc_weather, url_met_office, url_weather_com):
    combined_weather_data = {}

    # Fetch data from The Weather Outlook
    weather_outlook_data = the_weather_outlook(url_weather_outlook)
    if weather_outlook_data:
        combined_weather_data.update(weather_outlook_data)
    
    # Fetch data from BBC Weather
    bbc_weather_data = get_bbc_weather_data(url_bbc_weather)
    if bbc_weather_data:
        combined_weather_data.update(bbc_weather_data)

    # Fetch data from Met Office
    met_office_weather_data = get_met_office_weather_data(url_met_office)
    if met_office_weather_data:
        combined_weather_data.update(met_office_weather_data)
    
    # Fetch moon phase data
    url_moon_phase = "https://timesprayer.com/en/moon/united-kingdom-gb/london/#upcomingmoonphases"
    moon_phase_data = fetch_moon_data(url_moon_phase)
    if moon_phase_data:
        combined_weather_data['Moon Phase'] = moon_phase_data
    else:
        combined_weather_data['Moon Phase'] = "Moon phase data not available."
    
    # Fetch chance of rain from weather.com
    xpath_weather_com = '/html/body/div[1]/main/div[2]/main/div[1]/section/div[2]/div[2]/details[2]/summary/div/div/div[3]/span'
    chance_of_rain = weather_com_(url_weather_com, xpath_weather_com)
    combined_weather_data['Chance of Rain(%)'] = chance_of_rain  # Include chance of rain
    
    return combined_weather_data

# Example usage with multiple URLs
url_weather_outlook = "https://www.theweatheroutlook.com/forecast/uk/london"
url_bbc_weather = "https://www.bbc.co.uk/weather/2643743"
url_met_office = "https://www.metoffice.gov.uk/weather/forecast/gcpvj0v07#?date=2024-07-14"
url_weather_com = "https://weather.com/en-GB/weather/tenday/l/4c5ad40da52894d049451564c63c55bb65acbafdca5e334eba01d5aaec4983fc"

combined_weather_data = get_combined_weather_data(url_weather_outlook, url_bbc_weather, url_met_office, url_weather_com)

# Write combined results to a CSV file if data is fetched successfully
if combined_weather_data:
    print("Combined Weather Data:")
    # Print in the same order as fieldnames for clarity
    fieldnames = [
        'Date',
        'Location',
        'Weather Description',
        'High Temperature(C)',
        'Low Temperature(C)',
        'Wind Speed(mph)',
        'Wind Gust(mph)',
        'Chance of Rain(%)',
        'Rain Total (mm)',
        'Humidity(%)',
        'Pressure(mb)',
        
        'Pollen',
        'UV',
        'Sunrise',
        'Sunset',
        
        
        'Moon Phase',
    ]
    for field in fieldnames:
        print(f"{field}: {combined_weather_data[field]}")

    # Specify the CSV file path
    csv_file_path = "weather_tomorrow.csv"
    
    # Write the combined weather data to a CSV file with specified field order
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(combined_weather_data)
    
    print(f"\nWeather data has been written to {csv_file_path}")
else:
    print("No weather data available.")
