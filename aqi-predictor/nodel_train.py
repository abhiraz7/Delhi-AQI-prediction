from sklearn.ensemble import RandomForestRegressor
import joblib
import pandas as pd

# Load your training data (delhi_aqi_data.csv, or another dataset you're using for training)
data = pd.read_csv('delhi_aqi_data.csv')

# Prepare your features (X) and target (y) for training
X = data[['latitude', 'longitude', 'frp', 'month', 'day', 'day_of_week', 'season']]  # Update according to your dataset
y = data['aqi']  # Update this column according to your target variable

# Initialize the RandomForestRegressor model
random_forest_model = RandomForestRegressor(n_estimators=100, random_state=42)

# Train the model
random_forest_model.fit(X, y)

# Save the trained model to a file using joblib
joblib.dump(random_forest_model, 'random_forest_aqi_model.pkl')

print("Model training and saving complete.")
