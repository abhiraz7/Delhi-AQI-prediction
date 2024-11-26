from flask import Flask, request, jsonify
import joblib
import pandas as pd

model = joblib.load('random_forest_aqi_model.pkl')
app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Convert the JSON data into a pandas DataFrame, passing an index to avoid scalar error
        input_data = pd.DataFrame(data, index=[0])

        # Predict AQI using the trained model
        prediction = model.predict(input_data)

        # Return the predicted AQI as a JSON response
        return jsonify({'predicted_aqi': prediction[0]})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
