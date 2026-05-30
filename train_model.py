import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier


df = pd.read_csv("weather.csv")s
df = df.dropna()


df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day
df['Weekday'] = df['Date'].dt.weekday
df = df.drop('Date', axis=1)

df['City'] = df['City'].str.lower()
df['State'] = df['State'].str.lower()

encoders = {}

city_enc = LabelEncoder()
df['City'] = city_enc.fit_transform(df['City'])
encoders['City'] = city_enc

state_enc = LabelEncoder()
df['State'] = state_enc.fit_transform(df['State'])
encoders['State'] = state_enc

aqi_enc = LabelEncoder()
df['AQI_Category'] = aqi_enc.fit_transform(df['AQI_Category'])
encoders['AQI_Category'] = aqi_enc

features = [
    'City', 'State',
    'Lat', 'Lon',
    'Temp', 'Humidity',
    'Pressure',
    'Wind', 'Cloud',
    'AQI',
    'Year', 'Month', 'Day', 'Weekday'
]

X = df[features]
y = df['AQI_Category']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

print("Accuracy:", model.score(X_test, y_test))


joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")
joblib.dump(encoders, "encoders.pkl")

print("Model saved successfully!")