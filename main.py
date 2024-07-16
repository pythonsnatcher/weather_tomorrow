"""
the json credentials file needs to be locally accessible for this script to function
this script requires a google sheets documument with permission to edit, that is shared via the url.
"""

import requests
from lxml import html
import csv
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def weather_com_(url, xpath_expression):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        tree = html.fromstring(response.content)
        chance_of_rain = tree.xpath(xpath_expression)

        if chance_of_rain:
            chance_of_rain_text = chance_of_rain[0].text_content().strip()
            chance_of_rain_value = chance_of_rain_text.replace('%', '')
            return chance_of_rain_value
        else:
            return "Chance of rain not found on the webpage."

    except Exception as e:
        print(f"Error fetching chance of rain from {url}: {e}")
        return None

def the_weather_outlook(url):
    try:
        xpath_date = '//*[@id="2"]/td[1]/div/text()'
        xpath_high_temp = '//*[@id="2"]/td[3]/span/text()'
        xpath_wind_speed = '//*[@id="2"]/td[4]/span/text()'
        xpath_humidity = '//*[@id="2"]/td[7]/text()'
        xpath_pressure = '//*[@id="2"]/td[8]/text()'
        xpath_rain_total = '//*[@id="rt2"]/text()'
        xpath_wind_gust = '//*[@id="2"]/td[6]/span/text()'

        response = requests.get(url)
        response.encoding = 'utf-8'
        tree = html.fromstring(response.content)

        date = tree.xpath(xpath_date)[0].strip()
        high_temp_text = tree.xpath(xpath_high_temp)[0].strip()
        wind_speed_text = tree.xpath(xpath_wind_speed)[0].strip()
        humidity_text = tree.xpath(xpath_humidity)[0].strip()
        pressure_text = tree.xpath(xpath_pressure)[0].strip()
        rain_total_text = tree.xpath(xpath_rain_total)[0].strip()

        high_temp = extract_numeric_value(high_temp_text)
        wind_speed = extract_numeric_value(wind_speed_text)
        humidity = extract_numeric_value(humidity_text.rstrip('%'))
        pressure = extract_numeric_value(pressure_text)
        rain_total = extract_numeric_value(rain_total_text.rstrip('mm'))

        wind_gust_text = tree.xpath(xpath_wind_gust)[0].strip()
        wind_gust = extract_numeric_value(wind_gust_text)

        weather_data = {
            'Location': 'London',
            'Date': date,
            'High Temperature(C)': high_temp,
            'Wind Speed(mph)': wind_speed,
            'Humidity(%)': humidity,
            'Pressure(mb)': pressure,
            'Rain Total (mm)': rain_total,
            'Wind Gust(mph)': wind_gust
        }

        return weather_data

    except Exception as e:
        print(f"Error fetching weather data from The Weather Outlook: {e}")
        return None

def extract_numeric_value(text):
    try:
        numeric_text = ''.join(filter(lambda x: x.isdigit() or x == '.', text))
        numeric_value = float(numeric_text) if '.' in numeric_text else int(numeric_text)
        return numeric_value
    except ValueError:
        return text

def get_bbc_weather_data(url):
    try:
        xpath_tomorrow_pollen = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[2]/span[1]/span[1]/span[2]/text()'
        xpath_tomorrow_uv = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[2]/span[2]/span[1]/span[2]/text()'
        xpath_sunrise = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[1]/span[1]/span[2]/text()'
        xpath_sunset = '//*[@id="wr-forecast"]/div[4]/div/div[1]/div[4]/div/div[2]/div[1]/span[2]/span[2]/text()'
        xpath_weather_description = '//*[@id="daylink-1"]/div[4]/div[2]/div/text()'
        xpath_low_temperature = '//*[@id="daylink-1"]/div[4]/div[1]/div/div[4]/div/div[2]/span[2]/span/span[1]/text()'

        response = requests.get(url)
        response.encoding = 'utf-8'
        tree = html.fromstring(response.content)

        tomorrow_pollen = tree.xpath(xpath_tomorrow_pollen)[0].strip()
        tomorrow_uv = tree.xpath(xpath_tomorrow_uv)[0].strip()
        sunrise_time = tree.xpath(xpath_sunrise)[0].strip()
        sunset_time = tree.xpath(xpath_sunset)[0].strip()
        weather_description = tree.xpath(xpath_weather_description)[0].strip()
        low_temperature = tree.xpath(xpath_low_temperature)[0].strip()

        bbc_weather_data = {
            'Pollen': tomorrow_pollen,
            'UV': tomorrow_uv,
            'Sunrise': sunrise_time,
            'Sunset': sunset_time,
            'Weather Description': weather_description,
            'Low Temperature(C)': low_temperature
        }

        return bbc_weather_data

    except Exception as e:
        print(f"Error fetching weather data from BBC Weather: {e}")
        return None



def fetch_moon_data(url):
    try:
        xpath_moon_phase = '//*[@id="upcomingmoonphases"]/div/div/div[1]/div[3]/text()'

        response = requests.get(url)
        response.encoding = 'utf-8'
        tree = html.fromstring(response.content)

        moon_phase = tree.xpath(xpath_moon_phase)
        if moon_phase:
            moon_phase_text = moon_phase[0].strip()
            return moon_phase_text
        else:
            return "Moon phase not found on the webpage."

    except Exception as e:
        print(f"Error fetching moon data: {e}")
        return None

def get_combined_weather_data(url_weather_outlook, url_bbc_weather, url_weather_com):
    combined_weather_data = {}

    weather_outlook_data = the_weather_outlook(url_weather_outlook)
    if weather_outlook_data:
        combined_weather_data.update(weather_outlook_data)

    bbc_weather_data = get_bbc_weather_data(url_bbc_weather)
    if bbc_weather_data:
        combined_weather_data.update(bbc_weather_data)

    

    url_moon_phase = "https://timesprayer.com/en/moon/united-kingdom-gb/london/#upcomingmoonphases"
    moon_phase_data = fetch_moon_data(url_moon_phase)
    if moon_phase_data:
        combined_weather_data['Moon Phase'] = moon_phase_data
    else:
        combined_weather_data['Moon Phase'] = "Moon phase data not available."

    xpath_weather_com = '/html/body/div[1]/main/div[2]/main/div[1]/section/div[2]/div[2]/details[2]/summary/div/div/div[3]/span'
    chance_of_rain = weather_com_(url_weather_com, xpath_weather_com)
    combined_weather_data['Chance of Rain(%)'] = chance_of_rain

    return combined_weather_data

def write_to_google_sheets(data, sheet_name):
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    
    # JSON credentials directly in the script
    creds_dict = {
        "type": "service_account",
        "project_id": "weather-data-429210",
        "private_key_id": "af2c31cf7a66d123c4177f73f04fd01dca645a70",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCrVky4KtVU4WMl\nv82TyT/jTDyNv4Auk475CsROQgLSgIA6/EZ9fd+sIwbImEPkNw4bThe+coobn+Je\nu5lRg7yRVmXakqDCFPjq+2nV2riB0M2dBn3sgiCSxusYc1G0ieC3tpNBncy8M8ga\n/kBnAT9HRm/RHQP3so7hgRRghPE1ZmFq9buzDueqIy1TTTD89ZWnAS/sLNxefJhg\nIRMSCf1IBS/7fakNtch1WGbZr4Z1HuKXR8MajmCN1iOR1hcAHOn50uwGp78sYnel\nj8E2PC1sK1MMIGQc/k1UwG6jo1YV1k0Eu2IyXA3JukiSwBLfc2qHCw5Bq2+EGDjI\n6ChLkZllAgMBAAECggEAVYlZ9796jUuQQfJFYXhhKsqOmH14Msh74hzb7+3IluqM\nGeaEEnZaygcahd5uVmqd4kfUVsG77Rqe2ohxfF52L2CgrMPy+bGaq0Ukix0Ma9Kg\nM7pf90jnlh80kxpPOgBzbYP6dBGhenundMJlyIa43o5tmEoSBwDfj/jvAVidSvim\nTlweUrhBeT+5psdrsmHAk/Xv1Tqf9hPdnU8J9uz+5ATgjpIuB8InDlFD+yjhWHkZ\nF1FpoJaDaN69wHnYCE2TQVdbprkiPsOa9151kj+Gc/yBOMgGSvjsH7qTC9bptlz6\nzkgUHCjLum1Q/2r9jQj+9jHSB2H+O3q9j9wvPpZr6QKBgQDdYBVzqUee7r6sngY5\nDeKhBeIMpiHt4P4UMV0MmBQEaoRHm9LZSELlYQ/Btye2NDl4fIIByYHeEYEl6Chd\nxZtXJ1Z04P4txLmb0T4m+4/BVWwztwXklrO09Kgm62lYhbtqYbJfHJY4H41Xfqk9\nIePRkXkoTWoV7hA/Q4O0dVYVQwKBgQDGIqy6iNPBN3KQZmYDG9WKuFMsAx/gSor1\nqL5duBxUNyhkpVCLTtQvdS3aElvGCjMpWKTqmSxm8s74EQ7qLVU2YIq6u+avV47e\nN01qtrKtISFDQI/7RKKEhwoYoQEAMpT3/NpUEO4hoWdtEw50h4lmi37mFeZy2PQr\ns8sVt+xYNwKBgQCkWMbUPSIsvbXU1ORtyv8q6AEvvs6FmXlHaHZZ+TUzKhjWSLq6\nEMmJHQvjlqPmwtK/vj+OMBk30er9R2NgammuxEeNMdPCCsB5C1iG/E93CoHvyrqX\nP8JeXxvO+QoWbAH9MlaIAeML+3ClOiVOezB0zvkRkJdnfHuXW/oVKN8lnQKBgCfT\nTm7ME+wxbfiybGzRinGwrR8anayirx3DxkfmOuN+lsLsK61ksee8IPRFXmcHI9N6\nuuNg2Hj08z8PhrTxWcBtVVVFcY/rBI+MBCagBHgiQaJX9tjlqdkDn7blneLhR+o0\ny9m78XGXFMfq3av0llyjS2WKH2EUVLf4EqkR6BKvAoGAIE02RZ6Cj5fJa7WeTh/f\na1PV0pEzH4A44tOM68C6aDimDUdm37WLCR/5fmH+DT4IHljzg2rWSSzpD0rWMA2G\neScy6Qs0efX8BuasmZHzg15DuiAiZqvUFoejt9gsFQ0lxd42IZOiukCX1rn/ghXF\nacrHmWIWcgU31Uo0Z+Hyxws=\n-----END PRIVATE KEY-----\n",
        "client_email": "weather-data@weather-data-429210.iam.gserviceaccount.com",
        "client_id": "117847726458310784712",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/weather-data%40weather-data-429210.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/1QrvWcnT55mAl2NVi7rpZbdm9AzCsAvrEYRrgpMQQ-_I/edit?gid=0#gid=0')
    worksheet = sheet.worksheet(sheet_name)
    worksheet.clear()
    headers = list(data.keys())
    worksheet.append_row(headers)
    row_data = list(data.values())
    worksheet.append_row(row_data)


url_weather_outlook = "https://www.theweatheroutlook.com/forecast/uk/london"
url_bbc_weather = "https://www.bbc.co.uk/weather/2643743"

url_weather_com = "https://weather.com/en-GB/weather/tenday/l/4c5ad40da52894d049451564c63c55bb65acbafdca5e334eba01d5aaec4983fc"

combined_weather_data = get_combined_weather_data(url_weather_outlook, url_bbc_weather, url_weather_com)

if combined_weather_data:
    print("Combined Weather Data:")
    fieldnames = [
        'Date', 'Location', 'Weather Description', 'High Temperature(C)', 'Low Temperature(C)', 
        'Wind Speed(mph)', 'Wind Gust(mph)', 'Chance of Rain(%)', 'Rain Total (mm)', 
        'Humidity(%)', 'Pressure(mb)', 'Pollen', 'UV', 'Sunrise', 'Sunset', 'Moon Phase',
    ]
    for field in fieldnames:
        print(f"{field}: {combined_weather_data[field]}")

    csv_file_path = "weather_tomorrow.csv"
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(combined_weather_data)

    print(f"\nWeather data has been written to {csv_file_path}")

    write_to_google_sheets(combined_weather_data, 'Sheet1')
    print("Weather data has been written to Google Sheets")
else:
    print("No weather data available.")


















#the json credentials file needs to be locally accessible for this to work

import tkinter as tk
from tkinter import ttk
import csv
from PIL import Image, ImageTk
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#--------------------------------------------------------------------------------------
# Function to read weather data from CSV
# def read_weather_data_from_csv(file_path):
#     try:
#         with open(file_path, mode='r', newline='', encoding='utf-8') as file:
#             reader = csv.DictReader(file)
#             # Assuming there is only one row of data in the CSV
#             return next(reader, None)
#     except FileNotFoundError:
#         print(f"Error: File '{file_path}' not found.")
#         return None
#     except Exception as e:
#         print(f"Error reading CSV file '{file_path}': {e}")
#         return None


#-------------------------------------------------------------------------------------
# Function to read weather data from Google Sheets
def read_weather_data_from_google_sheets(sheet_url):
    try:
        # JSON credentials directly in the script
        creds_dict = {
            "type": "service_account",
            "project_id": "weather-data-429210",
            "private_key_id": "af2c31cf7a66d123c4177f73f04fd01dca645a70",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCrVky4KtVU4WMl\nv82TyT/jTDyNv4Auk475CsROQgLSgIA6/EZ9fd+sIwbImEPkNw4bThe+coobn+Je\nu5lRg7yRVmXakqDCFPjq+2nV2riB0M2dBn3sgiCSxusYc1G0ieC3tpNBncy8M8ga\n/kBnAT9HRm/RHQP3so7hgRRghPE1ZmFq9buzDueqIy1TTTD89ZWnAS/sLNxefJhg\nIRMSCf1IBS/7fakNtch1WGbZr4Z1HuKXR8MajmCN1iOR1hcAHOn50uwGp78sYnel\nj8E2PC1sK1MMIGQc/k1UwG6jo1YV1k0Eu2IyXA3JukiSwBLfc2qHCw5Bq2+EGDjI\n6ChLkZllAgMBAAECggEAVYlZ9796jUuQQfJFYXhhKsqOmH14Msh74hzb7+3IluqM\nGeaEEnZaygcahd5uVmqd4kfUVsG77Rqe2ohxfF52L2CgrMPy+bGaq0Ukix0Ma9Kg\nM7pf90jnlh80kxpPOgBzbYP6dBGhenundMJlyIa43o5tmEoSBwDfj/jvAVidSvim\nTlweUrhBeT+5psdrsmHAk/Xv1Tqf9hPdnU8J9uz+5ATgjpIuB8InDlFD+yjhWHkZ\nF1FpoJaDaN69wHnYCE2TQVdbprkiPsOa9151kj+Gc/yBOMgGSvjsH7qTC9bptlz6\nzkgUHCjLum1Q/2r9jQj+9jHSB2H+O3q9j9wvPpZr6QKBgQDdYBVzqUee7r6sngY5\nDeKhBeIMpiHt4P4UMV0MmBQEaoRHm9LZSELlYQ/Btye2NDl4fIIByYHeEYEl6Chd\nxZtXJ1Z04P4txLmb0T4m+4/BVWwztwXklrO09Kgm62lYhbtqYbJfHJY4H41Xfqk9\nIePRkXkoTWoV7hA/Q4O0dVYVQwKBgQDGIqy6iNPBN3KQZmYDG9WKuFMsAx/gSor1\nqL5duBxUNyhkpVCLTtQvdS3aElvGCjMpWKTqmSxm8s74EQ7qLVU2YIq6u+avV47e\nN01qtrKtISFDQI/7RKKEhwoYoQEAMpT3/NpUEO4hoWdtEw50h4lmi37mFeZy2PQr\ns8sVt+xYNwKBgQCkWMbUPSIsvbXU1ORtyv8q6AEvvs6FmXlHaHZZ+TUzKhjWSLq6\nEMmJHQvjlqPmwtK/vj+OMBk30er9R2NgammuxEeNMdPCCsB5C1iG/E93CoHvyrqX\nP8JeXxvO+QoWbAH9MlaIAeML+3ClOiVOezB0zvkRkJdnfHuXW/oVKN8lnQKBgCfT\nTm7ME+wxbfiybGzRinGwrR8anayirx3DxkfmOuN+lsLsK61ksee8IPRFXmcHI9N6\nuuNg2Hj08z8PhrTxWcBtVVVFcY/rBI+MBCagBHgiQaJX9tjlqdkDn7blneLhR+o0\ny9m78XGXFMfq3av0llyjS2WKH2EUVLf4EqkR6BKvAoGAIE02RZ6Cj5fJa7WeTh/f\na1PV0pEzH4A44tOM68C6aDimDUdm37WLCR/5fmH+DT4IHljzg2rWSSzpD0rWMA2G\neScy6Qs0efX8BuasmZHzg15DuiAiZqvUFoejt9gsFQ0lxd42IZOiukCX1rn/ghXF\nacrHmWIWcgU31Uo0Z+Hyxws=\n-----END PRIVATE KEY-----\n",
            "clie    
            
            
            .com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/weather-data%40weather-data-429210.iam.gserviceaccount.com",
            "universe_domain": "googleapis.com"
        }

        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(credentials)
        doc = client.open_by_url(sheet_url)
        sheet = doc.sheet1
        data = sheet.get_all_records()
        return data[0] if data else None

    except FileNotFoundError:
        print(f"Error: File 'credentials.json' not found.")
        return None
    except Exception as e:
        print(f"Error reading Google Sheets data: {e}")
        return None
        

# Function to create the GUI
def create_gui(weather_data):
    root = tk.Tk()
    root.title("Weather Forecast")

    # Create a frame for date
    frame_date = ttk.Frame(root, padding="10")
    frame_date.grid(row=0, column=0, sticky="w")

    # Create label for date (left-aligned)
    ttk.Label(frame_date, text=weather_data.get('Date', ''), anchor="w").pack(padx=5, pady=5)

    # Create a frame for location
    frame_location = ttk.Frame(root, padding="10")
    frame_location.grid(row=0, column=1, sticky="e")

    # Create label for location (right-aligned)
    ttk.Label(frame_location, text=weather_data.get('Location', ''), anchor="e").pack(padx=5, pady=5)

    # Create a frame for weather display (either image or text)
    frame_weather_display = ttk.Frame(root, padding="10")
    frame_weather_display.grid(row=1, column=0, columnspan=2, sticky="nsew")

    # Attempt to load and display weather image based on weather condition
    weather_condition = weather_data.get('Weather Description', '')
    image_path = get_image_path(weather_condition)

    try:
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image.resize((150, 150)))  # Resize image to fit within a 150x150 box

        # Create label for weather image
        label_image = ttk.Label(frame_weather_display, image=photo)
        label_image.image = photo  # Keep a reference to the image
        label_image.pack(padx=10, pady=10)

    except FileNotFoundError:
        print(f"Image file '{image_path}' not found. Displaying text instead.")
        # Create label for weather description (if image loading fails)
        ttk.Label(frame_weather_display, text=weather_condition, font=('Helvetica', 14, 'bold')).pack(pady=10)

    except Exception as e:
        print(f"Error loading image: {e}")
        # Fallback to displaying weather description as text
        ttk.Label(frame_weather_display, text=weather_condition, font=('Helvetica', 14, 'bold')).pack(pady=10)

    





    # Create a frame for wind speed and gust
    frame_wind = ttk.Frame(root, padding="10")
    frame_wind.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=50, pady=10)  # Center align with padding

    # Load image for wind
    wind_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/wind.png"
    try:
        image_wind = Image.open(wind_image_path)
        image_wind = image_wind.resize((50, 50))  # Resize image to fit within a 50x50 box
        photo_wind = ImageTk.PhotoImage(image_wind)

        # Create label for wind image
        label_wind_image = ttk.Label(frame_wind, image=photo_wind)
        label_wind_image.image = photo_wind
        label_wind_image.grid(row=0, column=0, rowspan=2, sticky="w", padx=5, pady=5)  # Span two rows for wind image

    except FileNotFoundError:
        print(f"Image file '{wind_image_path}' not found for wind.")
        ttk.Label(frame_wind, text="Wind", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, rowspan=2, sticky="w", padx=5, pady=5)

    except Exception as e:
        print(f"Error loading wind image: {e}")
        ttk.Label(frame_wind, text="Wind", font=('Helvetica', 12, 'bold')).grid(row=0, column=0, rowspan=2, sticky="w", padx=5, pady=5)

    # Display wind speed above wind gust on the right side of the image
    ttk.Label(frame_wind, text="Speed:").grid(row=0, column=1, sticky="e", padx=5, pady=5)
    ttk.Label(frame_wind, text=weather_data.get('Wind Speed(mph)', '')).grid(row=0, column=2, sticky="w", padx=5, pady=5)
    ttk.Label(frame_wind, text="Gust:").grid(row=1, column=1, sticky="e", padx=5, pady=5)
    ttk.Label(frame_wind, text=weather_data.get('Wind Gust(mph)', '')).grid(row=1, column=2, sticky="w", padx=5, pady=5)

    # Center-align contents within frame_wind
    frame_wind.grid_columnconfigure(0, weight=1)  # Make the first column expandable
    frame_wind.grid_columnconfigure(1, weight=1)  # Make the second column expandable
    frame_wind.grid_columnconfigure(2, weight=1)  # Make the third column expandable



    # # Create labels for pressure and humidity
    # frame_pressure_humidity = ttk.Frame(root, padding="10")
    # frame_pressure_humidity.grid(row=3, column=0, sticky="nw")
    # ttk.Label(frame_pressure_humidity, text="Pressure (mb)").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    # ttk.Label(frame_pressure_humidity, text=weather_data.get('Pressure(mb)', '')).grid(row=0, column=1, sticky="w", padx=5, pady=5)
    # ttk.Label(frame_pressure_humidity, text="Humidity (%)").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    # ttk.Label(frame_pressure_humidity, text=weather_data.get('Humidity(%)', '')).grid(row=1, column=1, sticky="w", padx=5, pady=5)

    





    # Create a frame for pollen and UV
    frame_pollen_uv = ttk.Frame(root, padding="10")
    frame_pollen_uv.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=50, pady=10)  # Center align with padding


    # Create label for Pollen
    ttk.Label(frame_pollen_uv, text="Pollen").grid(row=0, column=0, sticky="w", padx=5, pady=5)

    # Load image for pollen if 'H', 'M', or 'L'
    pollen_condition = weather_data.get('Pollen', '')
    if pollen_condition == 'H' or pollen_condition == 'M' or pollen_condition == 'L':
        if pollen_condition == 'H':
            pollen_image_path = "images/red_for_h.png"
        elif pollen_condition == 'L':
            pollen_image_path = "images/green_for_L.png"
        elif pollen_condition == 'M':
            pollen_image_path = "images/yellow_for_M.png"

        try:
            image_pollen = Image.open(pollen_image_path)
            image_pollen = image_pollen.resize((50, 50))  # Resize image to fit within a 50x50 box
            photo_pollen = ImageTk.PhotoImage(image_pollen)
            label_pollen_image = ttk.Label(frame_pollen_uv, image=photo_pollen)
            label_pollen_image.image = photo_pollen
            label_pollen_image.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        except FileNotFoundError:
            print(f"Image file '{pollen_image_path}' not found for pollen. Displaying text instead.")
            ttk.Label(frame_pollen_uv, text=weather_data.get('Pollen', '')).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        except Exception as e:
            print(f"Error loading pollen image: {e}")
            ttk.Label(frame_pollen_uv, text=weather_data.get('Pollen', '')).grid(row=0, column=1, sticky="w", padx=5, pady=5)
    else:
        ttk.Label(frame_pollen_uv, text=weather_data.get('Pollen', '')).grid(row=0, column=1, sticky="w", padx=5, pady=5)

    # Create label for UV
    ttk.Label(frame_pollen_uv, text="UV").grid(row=0, column=3, sticky="w", padx=5, pady=5)

    # Load image for UV if 'H', 'M', or 'L'
    uv_condition = weather_data.get('UV', '')
    if uv_condition == 'H' or uv_condition == 'M' or uv_condition == 'L':
        if uv_condition == 'H':
            uv_image_path = "images/red_for_h.png"
        elif uv_condition == 'L':
            uv_image_path = "images/green_for_L.png"
        elif uv_condition == 'M':
            uv_image_path = "images/yellow_for_M.png"

        try:
            image_uv = Image.open(uv_image_path)
            image_uv = image_uv.resize((50, 50))  # Resize image to fit within a 50x50 box
            photo_uv = ImageTk.PhotoImage(image_uv)
            label_uv_image = ttk.Label(frame_pollen_uv, image=photo_uv)
            label_uv_image.image = photo_uv
            label_uv_image.grid(row=0, column=2, sticky="w", padx=5, pady=5)
        except FileNotFoundError:
            print(f"Image file '{uv_image_path}' not found for UV. Displaying text instead.")
            ttk.Label(frame_pollen_uv, text=weather_data.get('UV', '')).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        except Exception as e:
            print(f"Error loading UV image: {e}")
            ttk.Label(frame_pollen_uv, text=weather_data.get('UV', '')).grid(row=0, column=2, sticky="w", padx=5, pady=5)
    else:
        ttk.Label(frame_pollen_uv, text=weather_data.get('UV', '')).grid(row=0, column=2, sticky="w", padx=5, pady=5)





    
    # Create a frame for temperature with image and arrows
    frame_temp = ttk.Frame(root, padding="10")
    frame_temp.grid(row=2, column=0, sticky="nsew",columnspan= 3, padx=50, pady=10)  # Center align with padding

    # Load image for temperature display
    temp_image_path = "images/temp.png"
    try:
        image_temp = Image.open(temp_image_path)
        image_temp = image_temp.resize((50, 50))  # Resize image to fit within a 50x50 box
        photo_temp = ImageTk.PhotoImage(image_temp)

        # Create label for temperature image
        label_temp_image = ttk.Label(frame_temp, image=photo_temp)
        label_temp_image.image = photo_temp
        label_temp_image.grid(row=0, column=0, rowspan=2, padx=5, pady=5)

        # Determine the temperature values
        high_temp = weather_data.get('High Temperature(C)', '')
        low_temp = weather_data.get('Low Temperature(C)', '')

        # Create labels for high and low temperatures with arrows
        ttk.Label(frame_temp, text=f"{high_temp} °C", font=('Helvetica', 14)).grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(frame_temp, text=f"↑", font=('Helvetica', 14)).grid(row=0, column=2, sticky="w", padx=5, pady=5)
        ttk.Label(frame_temp, text=f"{low_temp} °C", font=('Helvetica', 14)).grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(frame_temp, text=f"↓", font=('Helvetica', 14)).grid(row=1, column=2, sticky="w", padx=5, pady=5)

    except FileNotFoundError:
        print(f"Temperature image file '{temp_image_path}' not found.")
        ttk.Label(frame_temp, text="Temperature Image Not Found").grid(row=0, column=0, sticky="w", padx=5, pady=5)

    except Exception as e:
        print(f"Error loading temperature image: {e}")
        ttk.Label(frame_temp, text="Error Loading Image").grid(row=0, column=0, sticky="w", padx=5, pady=5)

    # Center-align contents within frame_temp
    frame_temp.grid_columnconfigure(0, weight=1)  # Make the first column expandable
    frame_temp.grid_columnconfigure(1, weight=1)  # Make the second column expandable
    frame_temp.grid_columnconfigure(2, weight=1)  # Make the third column expandable





    # Create a frame for sunrise and sunset
    frame_sunrise_sunset = ttk.Frame(root, padding="10")
    frame_sunrise_sunset.grid(row=5, column=0, columnspan=3, sticky="nsew")  # Center align with padding

    # Load image for sunrise if available
    sunrise_image_path = "images/sunrise.png"
    try:
        image_sunrise = Image.open(sunrise_image_path)
        image_sunrise = image_sunrise.resize((50, 50))  # Resize image to fit within a 50x50 box
        photo_sunrise = ImageTk.PhotoImage(image_sunrise)
        label_sunrise_image = ttk.Label(frame_sunrise_sunset, image=photo_sunrise)
        label_sunrise_image.image = photo_sunrise
        label_sunrise_image.grid(row=0, column=0, sticky="w", padx=5, pady=5)

        # Display sunrise time value
        ttk.Label(frame_sunrise_sunset, text=weather_data.get('Sunrise', ''), font=('Helvetica', 14, 'bold')).grid(row=0, column=1, sticky="w", padx=5, pady=5)

    except FileNotFoundError:
        print(f"Image file '{sunrise_image_path}' not found for sunrise. Displaying text instead.")
        ttk.Label(frame_sunrise_sunset, text=f"Sunrise: {weather_data.get('Sunrise', '')}", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=5)

    except Exception as e:
        print(f"Error loading sunrise image: {e}")
        ttk.Label(frame_sunrise_sunset, text=f"Sunrise: {weather_data.get('Sunrise', '')}", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, sticky="w", padx=5, pady=5)

    # Load image for sunset if available
    sunset_image_path = "images/sunset.png"
    try:
        image_sunset = Image.open(sunset_image_path)
        image_sunset = image_sunset.resize((50, 50))  # Resize image to fit within a 50x50 box
        photo_sunset = ImageTk.PhotoImage(image_sunset)
        label_sunset_image = ttk.Label(frame_sunrise_sunset, image=photo_sunset)
        label_sunset_image.image = photo_sunset
        label_sunset_image.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        # Display sunset time value
        ttk.Label(frame_sunrise_sunset, text=weather_data.get('Sunset', ''), font=('Helvetica', 14, 'bold')).grid(row=0, column=3, sticky="e", padx=5, pady=5)

    except FileNotFoundError:
        print(f"Image file '{sunset_image_path}' not found for sunset. Displaying text instead.")
        ttk.Label(frame_sunrise_sunset, text=f"Sunset: {weather_data.get('Sunset', '')}", font=('Helvetica', 14, 'bold')).grid(row=0, column=3, sticky="e", padx=5, pady=5)

    except Exception as e:
        print(f"Error loading sunset image: {e}")
        ttk.Label(frame_sunrise_sunset, text=f"Sunset: {weather_data.get('Sunset', '')}", font=('Helvetica', 14, 'bold')).grid(row=0, column=3, sticky="e", padx=5, pady=5)

    # Center-align both contents within frame_sunrise_sunset
    frame_sunrise_sunset.grid_columnconfigure(0, weight=1)  # Make the first column expandable
    frame_sunrise_sunset.grid_columnconfigure(1, weight=1)  # Make the second column expandable
    frame_sunrise_sunset.grid_columnconfigure(2, weight=1)  # Make the third column expandable
    frame_sunrise_sunset.grid_columnconfigure(3, weight=1)  # Make the fourth column expandable







        # Create a frame for rain chance and rain fall
    frame_rain = ttk.Frame(root, padding="10")
    frame_rain.grid(row=6, column=0, columnspan=2, sticky="nsew")  # Center align with padding

    # Load and display umbrella image
    umbrella_image_path = "images/umbrella.png"
    try:
        image_umbrella = Image.open(umbrella_image_path)
        image_umbrella = image_umbrella.resize((50, 50))  # Resize image to fit within a 50x50 box
        photo_umbrella = ImageTk.PhotoImage(image_umbrella)
        label_umbrella_image = ttk.Label(frame_rain, image=photo_umbrella)
        label_umbrella_image.image = photo_umbrella  # Keep a reference to the image
        label_umbrella_image.grid(row=0, column=0, padx=5, pady=5)

    except FileNotFoundError:
        print(f"Image file '{umbrella_image_path}' not found.")
        ttk.Label(frame_rain, text="Umbrella Image Not Found").grid(row=0, column=0, padx=5, pady=5)

    except Exception as e:
        print(f"Error loading umbrella image: {e}")
        ttk.Label(frame_rain, text="Error Loading Image").grid(row=0, column=0, padx=5, pady=5)

    # Display rain chance and rain fall values, center aligning them
    rain_text = f"{weather_data.get('Chance of Rain(%)', '')}%, {weather_data.get('Rain Total (mm)', '')}mm"
    ttk.Label(frame_rain, text=rain_text, font=('Helvetica', 14, 'bold')).grid(row=0, column=1, padx=5, pady=5)

    # Center-align both contents within frame_rain
    frame_rain.grid_columnconfigure(0, weight=1)  # Make the first column expandable
    frame_rain.grid_columnconfigure(1, weight=1)  # Make the second column expandable






    # Create a frame for moon phase
    frame_moon_phase = ttk.Frame(root, padding="10")
    frame_moon_phase.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=50, pady=10)

    # Check if the moon phase is 'First Quarter'
    moon_phase = weather_data.get('Moon Phase', '')
    if moon_phase == 'First Quarter':
        moon_image_path = "images/first_quarter_moon.png"
        try:
            moon_image = Image.open(moon_image_path)
            moon_image = moon_image.resize((50, 50))  # Resize image to fit within a 50x50 box
            moon_photo = ImageTk.PhotoImage(moon_image)

            # Create label for moon phase image
            label_moon_image = ttk.Label(frame_moon_phase, image=moon_photo)
            label_moon_image.image = moon_photo
            label_moon_image.pack(padx=10, pady=10)

        except FileNotFoundError:
            print(f"Image file '{moon_image_path}' not found for moon phase.")
            ttk.Label(frame_moon_phase, text="Moon Phase Image Not Found").pack(padx=10, pady=10)

        except Exception as e:
            print(f"Error loading moon phase image: {e}")
            ttk.Label(frame_moon_phase, text="Error Loading Image").pack(padx=10, pady=10)

    else:
        ttk.Label(frame_moon_phase, text=f"Moon Phase: {moon_phase}").pack(padx=10, pady=10)





    
    root.mainloop()

def get_image_path(weather_condition):
    # Define mappings of weather conditions to image paths
    image_map = {
        "Sunny intervals and a gentle breeze": "images/sunny_intervals_and_a_gentle_breeze.png",
        'Light rain showers and a gentle breeze': 'images/light_rain_showers.png'
        # Add more mappings for other weather conditions as needed
    }

    # Return the image path based on the weather condition
    return image_map.get(weather_condition, "")




# Main function to run the application
def main():
    sheet_url = 'https://docs.        -_I/edit?gid=0#gid=0'
    weather_data = read_weather_data_from_google_sheets(sheet_url)
    if weather_data:
        create_gui(weather_data)
    else:
        print("Failed to retrieve weather data from Google Sheets.")

if __name__ == "__main__":
    main()
#------------------------------------------------------------------
# # Example usage:
# file_path = "weather_tomorrow.csv"
# weather_data = read_weather_data_from_csv(file_path)
# if weather_data:
#     create_gui(weather_data)
# else:
#     print("No weather data available.")
