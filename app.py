from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import requests
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import json

app = Flask(__name__)

try:
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
    encoders = joblib.load("encoders.pkl")
    
    city_encoder = encoders["City"]
    state_encoder = encoders["State"]
    aqi_encoder = encoders["AQI_Category"]
except:
    print("[WARNING] Model files not found. Using demo mode.")

API_KEY = "cea123473c163513c49f1ca68f3b3afa"

AQI_HEALTH_DB = {
    "Good": {
        "range": (0, 50),
        "color": "#10b981",
        "message": "[GOOD] Air quality is satisfactory. You can safely go outside!"
    },
    "Satisfactory": {
        "range": (51, 100),
        "color": "#f59e0b",
        "message": "[CAUTION] Air quality is acceptable. Sensitive groups should limit outdoor activities."
    },
    "Moderately Polluted": {
        "range": (101, 200),
        "color": "#ff9800",
        "message": "[POOR] Air quality is poor. Everyone should reduce outdoor activities."
    },
    "Poor": {
        "range": (201, 300),
        "color": "#ef4444",
        "message": "[HAZARDOUS] Air quality is very poor. Avoid outdoor activities completely."
    },
    "Very Poor": {
        "range": (301, 500),
        "color": "#7c3aed",
        "message": "[EMERGENCY] Air quality is hazardous. Stay indoors and use air purifiers."
    }
}


def get_aqi_category(aqi_value):
    """Get AQI category and health info based on numeric value"""
    try:
        aqi_num = int(aqi_value) if isinstance(aqi_value, str) else aqi_value
    except:
        aqi_num = 0
    
    for category, info in AQI_HEALTH_DB.items():
        if info["range"][0] <= aqi_num <= info["range"][1]:
            return category, info
    
    return "Very Poor", AQI_HEALTH_DB["Very Poor"]


def get_coordinates(area, city, state):
    """Get latitude and longitude from area/city/state"""
    try:
        geolocator = Nominatim(user_agent="weather_app")
        query = f"{area}, {city}, {state}, India"
        location = geolocator.geocode(query)

        if location:
            return location.latitude, location.longitude
    except:
        pass

    return 0, 0


def get_location_details(lat, lon):
    """Get detailed location information from coordinates"""
    try:
        geolocator = Nominatim(user_agent="weather_app")
        location = geolocator.reverse((lat, lon), language='en')
        address = location.raw.get('address', {})

        return {
            "area": address.get('suburb', '') or address.get('village', ''),
            "city": address.get('city', '') or address.get('town', ''),
            "state": address.get('state', ''),
            "country": address.get('country', '')
        }
    except:
        return {}


def get_weather(lat, lon):
    """Get current weather data"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        data = requests.get(url, timeout=10).json()

        return {
            "temp": round(data["main"]["temp"], 1),
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind": round(data["wind"]["speed"], 1),
            "cloud": data["clouds"]["all"],
            "description": data["weather"][0]["description"].title()
        }
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None


def get_weather_by_date(lat, lon, target_date):
    """Get weather forecast for a specific date"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        data = requests.get(url, timeout=10).json()

        for item in data["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            if dt.strftime('%Y-%m-%d') == target_date:
                return {
                    "temp": round(item["main"]["temp"], 1),
                    "humidity": item["main"]["humidity"],
                    "pressure": item["main"]["pressure"],
                    "wind": round(item["wind"]["speed"], 1),
                    "cloud": item["clouds"]["all"]
                }
    except Exception as e:
        print(f"Error fetching forecast: {e}")

    return None


def get_7day_forecast(lat, lon):
    """Get 7-day forecast"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        data = requests.get(url, timeout=10).json()

        forecast_dict = {}
        for item in data["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            date_str = dt.strftime('%Y-%m-%d')
            
            if date_str not in forecast_dict:
                forecast_dict[date_str] = {
                    "date": dt.strftime('%a, %d %b'),
                    "temp": round(item["main"]["temp"], 1),
                    "humidity": item["main"]["humidity"],
                    "aqi": "N/A",
                    "desc": item["weather"][0]["description"].title()
                }

        return list(forecast_dict.values())[:7]
    except Exception as e:
        print(f"Error fetching 7-day forecast: {e}")
        return []


def get_aqi(lat, lon):
    """Get current AQI value"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
        data = requests.get(url, timeout=10).json()
        aqi_value = data["list"][0]["main"]["aqi"]
        # Convert numeric AQI to approximate value
        return int(aqi_value * 50) if aqi_value else 50
    except Exception as e:
        print(f"Error fetching AQI: {e}")
        return 50


def get_aqi_color(aqi_category):
    """Get color for AQI category"""
    info = AQI_HEALTH_DB.get(aqi_category, AQI_HEALTH_DB["Good"])
    return info["color"]


def get_hyperlocal_nearby_locations(lat, lon):
    """Get nearby locations (hyperlocal feature)"""
    nearby = [
        {"lat": lat + 0.01, "lon": lon + 0.01, "name": "North East Area"},
        {"lat": lat - 0.01, "lon": lon + 0.01, "name": "North West Area"},
        {"lat": lat + 0.01, "lon": lon - 0.01, "name": "South East Area"},
        {"lat": lat - 0.01, "lon": lon - 0.01, "name": "South West Area"},
    ]

    nearby_data = []
    for loc in nearby:
        try:
            aqi_val = get_aqi(loc["lat"], loc["lon"])
            weather = get_weather(loc["lat"], loc["lon"])
            category, info = get_aqi_category(aqi_val)
            
            nearby_data.append({
                "name": loc["name"],
                "aqi": f"{aqi_val} ({category})",
                "temp": weather["temp"] if weather else "N/A",
                "color": info["color"]
            })
        except:
            pass

    return nearby_data


def get_chart_data(lat, lon):
    """Prepare data for charts"""
    try:
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        data = requests.get(url, timeout=10).json()

        temps = []
        times = []
        aqi_categories = {"Good": 0, "Satisfactory": 0, "Moderately Polluted": 0, "Poor": 0, "Very Poor": 0}

        for i, item in enumerate(data["list"][:8]):  # 8 time steps = 24 hours
            dt = datetime.fromtimestamp(item["dt"])
            times.append(dt.strftime('%H:%M'))
            temps.append(round(item["main"]["temp"], 1))

        return {
            "temp": {"labels": times, "values": temps},
            "aqi": {"labels": list(aqi_categories.keys()), "values": list(aqi_categories.values())}
        }
    except Exception as e:
        print(f"Error preparing chart data: {e}")
        return {"temp": {}, "aqi": {}}



@app.route("/", methods=["GET", "POST"])
def index():
    """Main route for weather prediction"""
    
    prediction = None
    weather = None
    location = None
    aqi_color = None
    aqi_status = None
    aqi_health_message = None
    forecast = []
    nearby_locations = []
    aqi_chart_data = {}
    temp_chart_data = {}
    area = ""
    error = None

    if request.method == "POST":
        try:
            area = request.form.get("area", "").lower().strip()
            city = request.form.get("city", "").lower().strip()
            state = request.form.get("state", "").lower().strip()
            date_input = request.form.get("date")

            lat = request.form.get("lat")
            lon = request.form.get("lon")

            
            if lat and lon:
                lat, lon = float(lat), float(lon)
            else:
                lat, lon = get_coordinates(area, city, state)
                if lat == 0 and lon == 0:
                    error = "[ERROR] Location not found. Please enter valid location details."
                    return render_template(
                        "index.html",
                        error=error,
                        datetime_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        area=area
                    )

           
            location = get_location_details(lat, lon)
            weather = get_weather(lat, lon)

            if not date_input:
                date_input = datetime.now().strftime('%Y-%m-%d')

            # Get weather for specific date
            future = datetime.strptime(date_input, "%Y-%m-%d")
            future_weather = get_weather_by_date(lat, lon, date_input)

            if not future_weather:
                error = "[ERROR] No data available for the selected date. Try a date within 5 days."
                return render_template(
                    "index.html",
                    error=error,
                    datetime_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    area=area
                )

            
            aqi_real = get_aqi(lat, lon)
            aqi_status, aqi_info = get_aqi_category(aqi_real)
            aqi_color = aqi_info["color"]
            aqi_health_message = aqi_info["message"]

            
            try:
                city_enc = city_encoder.transform([city])[0] if city in city_encoder.classes_ else 0
                state_enc = state_encoder.transform([state])[0] if state in state_encoder.classes_ else 0

                input_data = np.array([[
                    city_enc,
                    state_enc,
                    lat,
                    lon,
                    future_weather["temp"],
                    future_weather["humidity"],
                    future_weather["pressure"],
                    future_weather["wind"],
                    future_weather["cloud"],
                    aqi_real,
                    future.year,
                    future.month,
                    future.day,
                    future.weekday()
                ]])

                input_scaled = scaler.transform(input_data)
                pred = model.predict(input_scaled)
                prediction = aqi_encoder.inverse_transform(pred)[0]
            except Exception as e:
                print(f"Model prediction error: {e}")
                prediction = aqi_status  

           
            forecast = get_7day_forecast(lat, lon)

            
            nearby_locations = get_hyperlocal_nearby_locations(lat, lon)

            
            chart_data = get_chart_data(lat, lon)
            temp_chart_data = chart_data.get("temp", {})
            aqi_chart_data = chart_data.get("aqi", {})

        except Exception as e:
            print(f"Error in prediction: {e}")
            error = f"[ERROR] An error occurred: {str(e)}"

    return render_template(
        "index.html",
        prediction=prediction,
        weather=weather,
        location=location,
        aqi_color=aqi_color,
        aqi_status=aqi_status,
        aqi_health_message=aqi_health_message,
        forecast=forecast,
        nearby_locations=nearby_locations,
        aqi_chart_data=aqi_chart_data,
        temp_chart_data=temp_chart_data,
        datetime_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        area=area,
        error=error
    )


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template("index.html", error="Page not found"), 404


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template("index.html", error="Server error occurred"), 500


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)