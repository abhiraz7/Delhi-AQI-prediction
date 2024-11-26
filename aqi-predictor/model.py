# Importing necessary libraries
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, KFold
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import xgboost as xgb
import joblib


# Load the combined data
data = pd.read_csv('delhi_aqi_data.csv', on_bad_lines='skip')


# Data Preprocessing: Convert timestamp to datetime and extract temporal features
data['timestamp'] = pd.to_datetime(data['timestamp'])
data['hour'] = data['timestamp'].dt.hour
data['day'] = data['timestamp'].dt.day
data['month'] = data['timestamp'].dt.month
data['weekday'] = data['timestamp'].dt.weekday  # 0=Monday, 6=Sunday

# Fill missing values (if any) using mean imputation for numerical columns
data.fillna(data.mean(), inplace=True)

# Features and target variable
X = data[['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3', 'hour', 'day', 'month', 'weekday']]
y = data['aqi']

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Standardize the data for better model performance (optional but recommended for some models)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Model 1: Linear Regression
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)

# Predictions and Evaluations
y_pred_lr = lr_model.predict(X_test)
lr_rmse = mean_squared_error(y_test, y_pred_lr, squared=False)
lr_mae = mean_absolute_error(y_test, y_pred_lr)
lr_r2 = r2_score(y_test, y_pred_lr)

print(f"Linear Regression RMSE: {lr_rmse}")
print(f"Linear Regression MAE: {lr_mae}")
print(f"Linear Regression R^2: {lr_r2}")

# Model 2: Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Predictions and Evaluations
y_pred_rf = rf_model.predict(X_test)
rf_rmse = mean_squared_error(y_test, y_pred_rf, squared=False)
rf_mae = mean_absolute_error(y_test, y_pred_rf)
rf_r2 = r2_score(y_test, y_pred_rf)

print(f"Random Forest RMSE: {rf_rmse}")
print(f"Random Forest MAE: {rf_mae}")
print(f"Random Forest R^2: {rf_r2}")





# Prepare feature matrix X and target vector y
X = data.drop(columns=['timestamp', 'aqi'])  # Exclude timestamp and target variable
y = data['aqi']

# Set up cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)  # 5-Fold Cross-validation

# Define models
lr_model = LinearRegression()
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
xgb_model = xgb.XGBRegressor(n_estimators=100, random_state=42)

# Cross-validate Linear Regression
lr_rmse_scores = -cross_val_score(lr_model, X, y, scoring="neg_root_mean_squared_error", cv=kf)
lr_mae_scores = -cross_val_score(lr_model, X, y, scoring="neg_mean_absolute_error", cv=kf)
lr_r2_scores = cross_val_score(lr_model, X, y, scoring="r2", cv=kf)

# Cross-validate Random Forest
rf_rmse_scores = -cross_val_score(rf_model, X, y, scoring="neg_root_mean_squared_error", cv=kf)
rf_mae_scores = -cross_val_score(rf_model, X, y, scoring="neg_mean_absolute_error", cv=kf)
rf_r2_scores = cross_val_score(rf_model, X, y, scoring="r2", cv=kf)

# Cross-validate Gradient Boosting
gb_rmse_scores = -cross_val_score(gb_model, X, y, scoring="neg_root_mean_squared_error", cv=kf)
gb_mae_scores = -cross_val_score(gb_model, X, y, scoring="neg_mean_absolute_error", cv=kf)
gb_r2_scores = cross_val_score(gb_model, X, y, scoring="r2", cv=kf)

# Cross-validate XGBoost
xgb_rmse_scores = -cross_val_score(xgb_model, X, y, scoring="neg_root_mean_squared_error", cv=kf)
xgb_mae_scores = -cross_val_score(xgb_model, X, y, scoring="neg_mean_absolute_error", cv=kf)
xgb_r2_scores = cross_val_score(xgb_model, X, y, scoring="r2", cv=kf)

# Print the results
print("Linear Regression Cross-Validation:")
print(f"RMSE: {lr_rmse_scores.mean()} ± {lr_rmse_scores.std()}")
print(f"MAE: {lr_mae_scores.mean()} ± {lr_mae_scores.std()}")
print(f"R^2: {lr_r2_scores.mean()} ± {lr_r2_scores.std()}")

print("\nRandom Forest Cross-Validation:")
print(f"RMSE: {rf_rmse_scores.mean()} ± {rf_rmse_scores.std()}")
print(f"MAE: {rf_mae_scores.mean()} ± {rf_mae_scores.std()}")
print(f"R^2: {rf_r2_scores.mean()} ± {rf_r2_scores.std()}")

print("\nGradient Boosting Cross-Validation:")
print(f"RMSE: {gb_rmse_scores.mean()} ± {gb_rmse_scores.std()}")
print(f"MAE: {gb_mae_scores.mean()} ± {gb_mae_scores.std()}")
print(f"R^2: {gb_r2_scores.mean()} ± {gb_r2_scores.std()}")

print("\nXGBoost Cross-Validation:")
print(f"RMSE: {xgb_rmse_scores.mean()} ± {xgb_rmse_scores.std()}")
print(f"MAE: {xgb_mae_scores.mean()} ± {xgb_mae_scores.std()}")
print(f"R^2: {xgb_r2_scores.mean()} ± {xgb_r2_scores.std()}")



# Save the Random Forest model
joblib.dump(rf_model, 'random_forest_aqi_model.pkl')



