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
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCrVky4KtVU4WMl\nv82TyT/jTDyNv4Auk475CsROQgLSgIA6/EZ9fd+sIwbImEPkNw4bThe+coobn+Je\nu5lRg7yRVmXakqDCFPjq+2nV2riB0M2dBn3sgiCSxusYc1G0ieC3tpNBncy8M8ga\n/kBnAT9HRm/RHQP3so7hgRRghPE1ZmFq9buzDueqIy1TTTD89ZWnAS/sLNxefJhg\nIRMSCf1IBS/7fakNtch1WGbZr4Z1HuKXR8MajmCN1iOR1hcAHOn50uwGp78sYnel\nj8E2PC1sK1MMIGQc/k1UwG6jo1YV1k0Eu2IyXA3JukiSwBLfc2qHCw5Bq2+EGDjI\n6ChLkZllAgMBAAECggEAVYlZ9796jUuQQfJFYXhhKsqOmH14Msh74hzb7+3IluqM\nGeaEEnZaygcahd5uVmqd4kfUVsG77Rqe2ohxfF52L2CgrMPy+bGaq0Ukix0Ma9Kg\nM7pf90jnlh80kxpPOgBzbYP6dBGhenundMJlyIa43o5tmEoSBwDfj/jvAVidSvim\nTlweUrhBeT+5psdrsmHAk/Xv1Tqf9hPdnU8J9uz+5ATgjpIuB8InDlFD+yjhWHkZ\nF1FpoJaDaN69wHnYCE2TQVdbprkiPsOa9151kj+Gc/yBOMgGSvjsH7qTC9bptlz6\nzkgUHCjLum1Q/2r9jQj+9jHSB2H+O3q9j9wvPpZr6QKBgQDdYBVzqUee7r6sngY5\nDeKhBeIMpiHt4P4UMV0MmBQEaoRHm9LZSELlYQ/Btye2NDl4fIIByYHeEYEl6Chd\nxZtXJ1Z04P4txLmb0T4m+4/BVWwztwXklrO09Kgm62lYhbtqYbJfHJY4H41Xfqk9\nIePRkXkoTWoV7hA/Q4O0dVYVQwKBgQDGIqy6iNPBN3KQZmYDG9WKuFMsAx/gSor1\nqL5duBxUNyhkpVCLTtQvdS3aElvGCjMpWKTqmSxm8s74EQ7qLVU2YIq6u+avV47e\nN01qtrKtISFDQI/7RKKEhwoYoQEAMpT3/NpUEO4hoWdtEw50h4lmi37mFeZy2PQr\ns8sVt+xYNwKBgQCkWMbUPSIsvbXU1ORtyv8q6AEvvs6FmXlHaHZZ+TUzKhjWSLq6\nEMmJHQvjlqPmwtK/vj+OMBk30er9R2NgammuxEeNMdPCCsB5C1iG/E93CoHvyrqX\nP8JeXxvO+QoWbAH9MlaIAeML+3ClOiVOezB0zvkRkJdnfHuXW/oVKN8lnQKBgCfT\nTm7ME+wxbfiybGzRinGwrR8anayirx3DxkfmOuN+lsLsK61ksee8IPRFXmcHI9N6\nuuNg2Hj08z8PhrTxWcBtVVVFcY/rBI+MBCagBHgiQaJX9tjlqdkDn7blneLhR+o0\ny9m78XGXFMfq3av0llyjS2WKH2EUVLf4EqkR6BKvAoGAIE02RZ6Cj5fJa7WeTh/f\na1PV0pEzH4A44tOM68C6aDimDUdm37WLCR/5fmH+DT4IHljzg2rWSSzpD0rWMA2G\neScy6Qs0efX8BuasmZHzg15DuiAiZqvUFoejt9gsFQ0lxd42IZOiukCX1rn/ghXF\nacrHmWIWcgU31Uo0Z+Hyxws=\n-----END PRIVATE KEY-----\n",
            "client_email": "weather-data@weather-data-429210.iam.gserviceaccount.com",
            "client_id": "117847726458310784712",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
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
    sheet_url = "https://docs.google.com/spreadsheets/d/1QrvWcnT55mAl2NVi7rpZbdm9AzCsAvrEYRrgpMQQ-_I/edit?gid=0#gid=0"
    weather_data_sheets = read_weather_data_from_google_sheets(sheet_url)

    return render_template('index.html', weather_data_sheets=weather_data_sheets)

if __name__ == '__main__':
    app.run(debug=True)
