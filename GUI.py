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
        credentials_path = '/Users/snatch./Downloads/weather_tomorrow/weather-data-429210-af2c31cf7a66.json'
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
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

        # Example usage:
sheet_url = "https://docs.google.com/spreadsheets/d/1QrvWcnT55mAl2NVi7rpZbdm9AzCsAvrEYRrgpMQQ-_I/edit?gid=0#gid=0"
weather_data = read_weather_data_from_google_sheets(sheet_url)
if weather_data:
    print("Weather data retrieved successfully:")
    print(weather_data)
    create_gui(weather_data)  # Call create_gui with retrieved weather_data
else:
    print("No weather data available.")

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
    frame_wind.grid(row=3, column=1, sticky="nw")

    # Load image for wind
    wind_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/wind.png"
    try:
        image_wind = Image.open(wind_image_path)
        image_wind = image_wind.resize((50, 50))  # Resize image to fit within a 50x50 box
        photo_wind = ImageTk.PhotoImage(image_wind)
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
    ttk.Label(frame_wind, text=weather_data.get('Wind Speed(mph)', '')).grid(row=1, column=1, sticky="w", padx=5, pady=5)
    ttk.Label(frame_wind, text="Gust:").grid(row=0, column=2, sticky="e", padx=5, pady=5)
    ttk.Label(frame_wind, text=weather_data.get('Wind Gust(mph)', '')).grid(row=1, column=2, sticky="w", padx=5, pady=5)
    # # Create labels for pressure and humidity
    # frame_pressure_humidity = ttk.Frame(root, padding="10")
    # frame_pressure_humidity.grid(row=3, column=0, sticky="nw")
    # ttk.Label(frame_pressure_humidity, text="Pressure (mb)").grid(row=0, column=0, sticky="w", padx=5, pady=5)
    # ttk.Label(frame_pressure_humidity, text=weather_data.get('Pressure(mb)', '')).grid(row=0, column=1, sticky="w", padx=5, pady=5)
    # ttk.Label(frame_pressure_humidity, text="Humidity (%)").grid(row=1, column=0, sticky="w", padx=5, pady=5)
    # ttk.Label(frame_pressure_humidity, text=weather_data.get('Humidity(%)', '')).grid(row=1, column=1, sticky="w", padx=5, pady=5)

    
    # Create a frame for pollen and UV
    frame_pollen_uv = ttk.Frame(root, padding="10")
    frame_pollen_uv.grid(row=4, column=0, columnspan=2, sticky="nw")

    # Create label for Pollen
    ttk.Label(frame_pollen_uv, text="Pollen").grid(row=0, column=0, sticky="w", padx=5, pady=5)

    # Load image for pollen if 'H', 'M', or 'L'
    pollen_condition = weather_data.get('Pollen', '')
    if pollen_condition == 'H' or pollen_condition == 'M' or pollen_condition == 'L':
        if pollen_condition == 'H':
            pollen_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/red_for_h.png"
        elif pollen_condition == 'L':
            pollen_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/green_for_L.png"
        elif pollen_condition == 'M':
            pollen_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/yellow_for_M.png"

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
            uv_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/red_for_h.png"
        elif uv_condition == 'L':
            uv_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/green_for_L.png"
        elif uv_condition == 'M':
            uv_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/yellow_for_M.png"

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
    frame_temp.grid(row=2, column=0, sticky="nw")

    # Load image for temperature display
    temp_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/temp.png"
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



    # Create a frame for sunrise and sunset
    frame_sunrise_sunset = ttk.Frame(root, padding="10")
    frame_sunrise_sunset.grid(row=5, column=0, columnspan=3, sticky="nsew")

    # Load image for sunrise if available
    sunrise_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/sunrise.png"
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
    sunset_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/sunset.png"
    try:
        image_sunset = Image.open(sunset_image_path)
        image_sunset = image_sunset.resize((50, 50))  # Resize image to fit within a 50x50 box
        photo_sunset = ImageTk.PhotoImage(image_sunset)
        label_sunset_image = ttk.Label(frame_sunrise_sunset, image=photo_sunset)
        label_sunset_image.image = photo_sunset
        label_sunset_image.grid(row=0, column=3, sticky="e", padx=5, pady=5)

        # Display sunset time value
        ttk.Label(frame_sunrise_sunset, text=weather_data.get('Sunset', ''), font=('Helvetica', 14, 'bold')).grid(row=0, column=2, sticky="e", padx=5, pady=5)

    except FileNotFoundError:
        print(f"Image file '{sunset_image_path}' not found for sunset. Displaying text instead.")
        ttk.Label(frame_sunrise_sunset, text=f"Sunset: {weather_data.get('Sunset', '')}", font=('Helvetica', 14, 'bold')).grid(row=0, column=2, sticky="e", padx=5, pady=5)

    except Exception as e:
        print(f"Error loading sunset image: {e}")
        ttk.Label(frame_sunrise_sunset, text=f"Sunset: {weather_data.get('Sunset', '')}", font=('Helvetica', 14, 'bold')).grid(row=0, column=2, sticky="e", padx=5, pady=5)

    # Create labels for rain chance and rain fall
    frame_rain = ttk.Frame(root, padding="10")
    frame_rain.grid(row=6, column=0, columnspan=2, sticky="nsew")

    # Load and display umbrella image
    umbrella_image_path = "/Users/snatch./Downloads/weather_tomorrow/images/umbrella.png"
    try:
        image_umbrella = Image.open(umbrella_image_path)
        image_umbrella = image_umbrella.resize((50, 50))  # Resize image to fit within a 50x50 box
        photo_umbrella = ImageTk.PhotoImage(image_umbrella)
        label_umbrella_image = ttk.Label(frame_rain, image=photo_umbrella)
        label_umbrella_image.image = photo_umbrella  # Keep a reference to the image
        label_umbrella_image.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    except FileNotFoundError:
        print(f"Image file '{umbrella_image_path}' not found.")
        ttk.Label(frame_rain, text="Umbrella Image Not Found").grid(row=0, column=0, sticky="w", padx=5, pady=5)

    except Exception as e:
        print(f"Error loading umbrella image: {e}")
        ttk.Label(frame_rain, text="Error Loading Image").grid(row=0, column=0, sticky="w", padx=5, pady=5)

    # Display rain chance and rain fall values
    ttk.Label(frame_rain, text=f"{weather_data.get('Chance of Rain(%)', '')}%, {weather_data.get('Rain Total (mm)', '')}mm", font=('Helvetica', 14, 'bold')).grid(row=0, column=1, sticky="w", padx=5, pady=5)



    
    root.mainloop()

def get_image_path(weather_condition):
    # Define mappings of weather conditions to image paths
    image_map = {
        "Sunny intervals and a gentle breeze": "/Users/snatch./Downloads/weather_tomorrow/images/sunny_intervals_and_a_gentle_breeze.png",
        # Add more mappings for other weather conditions as needed
    }

    # Return the image path based on the weather condition
    return image_map.get(weather_condition, "")
#------------------------------------------------------------------
# # Example usage:
# file_path = "weather_tomorrow.csv"
# weather_data = read_weather_data_from_csv(file_path)
# if weather_data:
#     create_gui(weather_data)
# else:
#     print("No weather data available.")
