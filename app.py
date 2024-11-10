from flask import Flask, request, render_template
import numpy as np
import joblib
import pandas as pd

# Load the trained model and scaler(s)
model = joblib.load('model.joblib')
standard_scaler = joblib.load('standscaler.joblib')

# Create a Flask app
app = Flask(__name__)

# Mapping crops to their corresponding image filenames
crop_image_map = {
    "Apple": "Apple.jpg",
    "Banana": "Banana.jpg",
    "Blackgram": "Blackgram.jpg",
    "Chickpea": "Chickpea.jpg",
    "Coconut": "Coconut.jpg",
    "Coffee": "Coffee.jpg",
    "Cotton": "Cotton.jpg",
    "Grapes": "Grapes.jpg",
    "Jute": "Jute.jpg",
    "Kidneybeans": "Kidneybeans.jpg",
    "Lentil": "Lentil.jpg",
    "Maize": "Maize.jpg",
    "Mango": "Mango.jpg",
    "Mothbeans": "Mothbeans.jpg",
    "Mungbean": "Mungbean.jpg",
    "Muskmelon": "Muskmelon.jpg",
    "Orange": "Orange.jpg",
    "Papaya": "Papaya.jpg",
    "Pigeonpeas": "Pigeonpeas.jpg",
    "Pomegranate": "Pomegranate.jpg",
    "Rice": "Rice.jpg",
    "Watermelon": "Watermelon.jpg"
}

@app.route('/')
def index():
    # Provide a default value for crop_image
    return render_template("index.html", result="", crop_image="default.jpg")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route("/predict", methods=['POST'])
def predict():
    try:
        # Retrieve input values from the form
        N = request.form.get('Nitrogen')
        P = request.form.get('Phosphorus')
        K = request.form.get('Potassium')
        temp = request.form.get('Temperature')
        humidity = request.form.get('Humidity')
        ph = request.form.get('Ph')
        rainfall = request.form.get('Rainfall')

        # Validate all inputs are filled and numeric
        input_values = [N, P, K, temp, humidity, ph, rainfall]
        if None in input_values or "" in input_values:
            raise ValueError("Please fill in all the fields with numeric values.")

        # Convert inputs to a numeric feature list
        feature_list = [float(val) for val in input_values]

        # Create a DataFrame with column names matching those used in training
        feature_df = pd.DataFrame(
            [feature_list],
            columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']  # Adjusted names
        )

        # Apply scaling transformations
        final_features = standard_scaler.transform(feature_df)

        # Make prediction
        prediction = model.predict(final_features)

        # Format the prediction result for display
        result = prediction[0].title()

        # Get the corresponding image filename based on the predicted crop
        crop_image = crop_image_map.get(result, "default.jpg")  # Default image if crop is not in the map

    except ValueError as ve:
        result = str(ve)
        crop_image = "default.jpg"  # Default image for error
    except Exception as e:
        result = f"An error occurred: {str(e)}"
        crop_image = "default.jpg"  # Default image for error

    return render_template('index.html', result=result, crop_image=crop_image)

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
