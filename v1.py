import requests
from lxml import html

def the_weather_outlook(url):
    try:
        # Define XPath expressions
        xpath_date = '//*[@id="2"]/td[1]/div/text()'           # XPath for date
        xpath_high_temp = '//*[@id="2"]/td[3]/span/text()'     # XPath for high temperature
        xpath_wind_speed = '//*[@id="2"]/td[4]/span/text()'    # XPath for wind speed
        xpath_humidity = '//*[@id="2"]/td[7]/text()'           # XPath for humidity
        xpath_pressure = '//*[@id="2"]/td[8]/text()'           # XPath for pressure
        xpath_rain_total = '//*[@id="rt2"]/text()'             # XPath for rain total
        xpath_wind_direction_img = '//*[@id="im5"]/img/@alt'   # XPath for wind direction (alt attribute of img)
        xpath_wind_direction_text = '//*[@id="im5"]/text()'    # XPath for wind direction (text format)
        
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
        
        # Extract wind direction
        wind_direction = ''
        # First, try to get wind direction from alt attribute of image
        wind_direction_img = tree.xpath(xpath_wind_direction_img)
        if wind_direction_img:
            wind_direction = wind_direction_img[0].strip()
        
        # If wind direction is not found in alt attribute, try to get it from text
        if not wind_direction:
            wind_direction_text = tree.xpath(xpath_wind_direction_text)
            if wind_direction_text:
                wind_direction = wind_direction_text[0].strip()
        
        # Prepare and return the extracted data as a dictionary
        weather_data = {
            'Location': 'London',
            'Date': date,
            'High Temperature(C)': high_temp,
            'Wind Speed(mph)': wind_speed,
            'Humidity(%)': humidity,
            'Pressure(mb)': pressure,
            'Rain Total (mm)': rain_total,
            'Wind Direction': wind_direction
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
        # Define XPath expressions
        xpath_tomorrow_pollen = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[2]/span[1]/span[1]/span[2]/text()'
        xpath_tomorrow_uv = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[2]/span[2]/span[1]/span[2]/text()'
        xpath_sunrise = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[1]/span[1]/span[2]/text()'
        xpath_sunset = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[1]/span[2]/span[2]/text()'

        # Fetch the webpage content
        response = requests.get(url)
        response.encoding = 'utf-8'  # Set the encoding explicitly to utf-8
        tree = html.fromstring(response.content)

        # Extract tomorrow's pollen, UV, sunrise, and sunset using XPath
        tomorrow_pollen = tree.xpath(xpath_tomorrow_pollen)[0].strip()
        tomorrow_uv = tree.xpath(xpath_tomorrow_uv)[0].strip()
        sunrise_time = tree.xpath(xpath_sunrise)[0].strip()
        sunset_time = tree.xpath(xpath_sunset)[0].strip()

        # Prepare and return the extracted data as a dictionary
        bbc_weather_data = {
            'Pollen Tomorrow': tomorrow_pollen,
            'UV Tomorrow': tomorrow_uv,
            'Sunrise': sunrise_time,
            'Sunset': sunset_time
        }
        
        return bbc_weather_data
    
    except Exception as e:
        print(f"Error fetching weather data from BBC Weather: {e}")
        return None

# Function to get combined weather data from both sources
def get_combined_weather_data(url_weather_outlook, url_bbc_weather):
    combined_weather_data = {}

    # Fetch data from The Weather Outlook
    weather_outlook_data = the_weather_outlook(url_weather_outlook)
    if weather_outlook_data:
        combined_weather_data.update(weather_outlook_data)
    
    # Fetch data from BBC Weather
    bbc_weather_data = get_bbc_weather_data(url_bbc_weather)
    if bbc_weather_data:
        combined_weather_data.update(bbc_weather_data)
    
    return combined_weather_data

# Example usage with multiple URLs
url_weather_outlook = "https://www.theweatheroutlook.com/forecast/uk/london"
url_bbc_weather = "https://www.bbc.co.uk/weather/2643743"

combined_weather_data = get_combined_weather_data(url_weather_outlook, url_bbc_weather)

# Print combined results if data is fetched successfully
if combined_weather_data:
    print("Combined Weather Data:")
    for key, value in combined_weather_data.items():
        print(f"{key}: {value}")
