from flask import Flask, render_template
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Function to read weather data from Google Sheets
def read_weather_data_from_google_sheets(sheet_url):
    try:
        # Replace with your own credentials dictionary
        creds_dict = {
            "type": "service_account",
            "project_id": "weather-data-429210",
            "private_key_id": "af2c31cf7a66d123c4177f73f04fd01dca645a70",
            "private_key": "-----BEGIN PRIuth2/auth",
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

    except Exception as e:
        print(f"Error reading Google Sheets data: {e}")
        return None

# Route to render the HTML template with weather data
@app.route('/')
def index():
    # Assuming weather data is retrieved from Google Sheets
    sheet_url = "https://docs.google.com/sprea      AzCsAvrEYRrgpMQQ-_I/edit?gid=0#gid=0"
    weather_data_sheets = read_weather_data_from_google_sheets(sheet_url)

    return render_template('index.html', weather_data_sheets=weather_data_sheets)

if __name__ == '__main__':
    app.run(debug=True)
