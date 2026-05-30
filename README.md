# 🌍 HyperWeather - Advanced Hyperlocal Weather & AQI Prediction

A professional, modern weather prediction application with hyperlocal AQI forecasting, interactive visualizations, and real-time data.

## ✨ Features

### 🎯 Core Features
- **Hyperlocal Weather Prediction**: Get detailed weather forecasts for your exact location
- **AQI Prediction**: AI-powered Air Quality Index predictions using Machine Learning
- **Real-Time Weather Data**: Live weather conditions from OpenWeatherMap API
- **Interactive Map**: Leaflet-powered map with location tracking

### 🚀 Advanced Features
- **7-Day Forecast**: Extended weather predictions for the next week
- **Hyperlocal Nearby Locations**: Check AQI for 4 nearby areas (N/E, N/W, S/E, S/W)
- **Interactive Charts**:
  - Temperature trend graphs
  - AQI distribution analysis
- **Health Recommendations**: AQI-based health alerts and activity suggestions
- **Geolocation Support**: One-click location detection
- **Responsive Design**: Works seamlessly on mobile, tablet, and desktop

### 🎨 UI/UX Enhancements
- Modern gradient design with professional color scheme
- Card-based layout for easy information scanning
- Smooth animations and transitions
- Icon-rich interface for quick visual understanding
- Accessible and clean typography
- Real-time datetime display

## 📊 AQI Health Categories

| Category | Range | Status | Recommendation |
|----------|-------|--------|-----------------|
| Good | 0-50 | ✅ Safe | Go outside! |
| Satisfactory | 51-100 | ⚠️ Caution | Sensitive groups limit outdoors |
| Moderately Polluted | 101-200 | ⚠️ Poor | Reduce outdoor activities |
| Poor | 201-300 | 🚫 Hazardous | Avoid outdoors |
| Very Poor | 301-500 | 🚨 Emergency | Stay indoors |

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Data Visualization**: Chart.js
- **Mapping**: Leaflet.js
- **Weather API**: OpenWeatherMap
- **Geocoding**: Nominatim (OpenStreetMap)
- **ML Model**: Scikit-learn (Random Forest)
- **Icons**: Font Awesome

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone or download the project**
   ```bash
   cd weather_project
   ```

2. **Install dependencies**
   ```bash
   pip install flask numpy scikit-learn joblib requests geopy
   ```

3. **Train the model** (if needed)
   ```bash
   python train_model.py
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://127.0.0.1:5000
   ```

## 🚀 Usage

### Manual Location Entry
1. Enter Area, City, and State details
2. Select a date (within 5 days for best accuracy)
3. Click "Get Prediction"

### Geolocation
1. Click "📍 Use My Location"
2. Allow browser location access
3. Select a future date
4. Click "Get Prediction"

### Interpreting Results
- **Location Details**: Shows exact area, city, state
- **Live Weather**: Current temperature, humidity, wind speed, cloud cover
- **AQI Prediction**: AI-predicted AQI category with health recommendations
- **7-Day Forecast**: Weather predictions for the next week
- **Nearby Locations**: Check AQI in nearby areas for hyperlocal insights
- **Charts**: Visual representation of temperature trends and AQI distribution

## 📁 Project Structure

```
weather_project/
├── app.py                 # Main Flask application
├── train_model.py         # ML model training script
├── weather.csv           # Training dataset
├── model.pkl             # Trained ML model
├── scaler.pkl            # Feature scaler
├── encoders.pkl          # Label encoders
├── static/
│   └── style.css         # Professional styling
├── templates/
│   └── index.html        # Modern UI template
└── README.md             # Documentation
```

## 🔧 Configuration

### API Key
The app uses OpenWeatherMap's free tier API. To use your own API key:

1. Sign up at [openweathermap.org](https://openweathermap.org/api)
2. Get your free API key
3. Replace `API_KEY` in `app.py`

### Debug Mode
- **Development**: `debug=True` (auto-reload on changes)
- **Production**: `debug=False` (disable in `app.py`)

## 📊 Data Sources

- **Weather Data**: OpenWeatherMap API
- **AQI Data**: OpenWeatherMap Air Pollution API
- **Geocoding**: Nominatim (OpenStreetMap)
- **ML Model**: Random Forest Classifier trained on `weather.csv`

## 🎯 Future Enhancements

- [ ] Historical AQI trends
- [ ] Hourly AQI updates
- [ ] Pollution source mapping
- [ ] Health alert notifications
- [ ] Export data as PDF/CSV
- [ ] Multiple city tracking
- [ ] Dark mode toggle
- [ ] Multilingual support
- [ ] Progressive Web App (PWA)

## ⚠️ Limitations

- Weather forecast accuracy: Up to 5 days
- AQI predictions based on trained model (may vary)
- API rate limits: Limited free tier requests
- Geolocation requires browser permission

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

## 📝 License

Open source project - Free to use and modify

## 📧 Support

For issues, suggestions, or feedback, feel free to reach out.

---

**Made with ❤️ for weather enthusiasts** | Last Updated: 2026
