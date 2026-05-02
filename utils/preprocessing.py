import pandas as pd

ZONE_MAP = {'downtown': 0, 'airport': 1, 'suburbs': 2, 'mall': 3, 'hospital': 4, 'university': 5, 'station': 6, 'business_park': 7, 'old_city': 8}
WEATHER_MAP = {'clear': 0, 'cloudy': 1, 'rain': 2, 'heavy_rain': 3, 'fog': 4}

def preprocess_data(df):
    df = df.copy()

    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek

    if 'zone' in df.columns:
        df['zone'] = df['zone'].str.lower().str.replace(' ', '_').map(ZONE_MAP).fillna(0).astype(int)

    if 'weather' in df.columns:
        df['weather'] = df['weather'].str.lower().map(WEATHER_MAP).fillna(0).astype(int)

    if 'day_of_week' in df.columns and df['day_of_week'].dtype == object:
        day_map = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
        df['day_of_week'] = df['day_of_week'].str.lower().map(day_map).fillna(0).astype(int)

    feature_cols = ['hour', 'day_of_week', 'zone', 'weather', 'temperature']
    available = [c for c in feature_cols if c in df.columns]
    X = df[available].fillna(0)
    y = df['demand'].fillna(0)
    return X, y
