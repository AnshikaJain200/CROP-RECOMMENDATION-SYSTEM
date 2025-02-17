from flask import Flask, request, render_template
import numpy as np
import pickle

# Importing model and scalers
model = pickle.load(open('model.pkl', 'rb'))
sc = pickle.load(open('standscaler.pkl', 'rb'))
ms = pickle.load(open('minmaxscaler.pkl', 'rb'))

# Creating Flask app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route("/predict", methods=['POST'])
def predict():
    # Getting data from form
    try:
        N = float(request.form['Nitrogen'])
        P = float(request.form['Phosporus'])
        K = float(request.form['Potassium'])
        temp = float(request.form['Temperature'])
        humidity = float(request.form['Humidity'])
        ph = float(request.form['Ph'])
        rainfall = float(request.form['Rainfall'])
    except ValueError:
        return render_template('index.html', result="Invalid input. Please enter numeric values.")

    # Preparing data for prediction
    feature_list = [N, P, K, temp, humidity, ph, rainfall]
    single_pred = np.array(feature_list).reshape(1, -1)

    # Debugging: Print feature list and shape
    print(f"Features: {feature_list}")
    print(f"Features shape: {single_pred.shape}")

    try:
        # Scaling features
        scaled_features = ms.transform(single_pred)
        final_features = sc.transform(scaled_features)

        # Debugging: Print scaled features
        print(f"Scaled features: {scaled_features}")
        print(f"Final features: {final_features}")

        # Predicting the crop
        prediction = model.predict(final_features)

        # Debugging: Print prediction
        print(f"Prediction: {prediction}")

        # Crop dictionary
        crop_dict = {
            1: "Rice", 2: "Maize", 3: "Jute", 4: "Cotton", 5: "Coconut", 6: "Papaya",
            7: "Orange", 8: "Apple", 9: "Muskmelon", 10: "Watermelon", 11: "Grapes",
            12: "Mango", 13: "Banana", 14: "Pomegranate", 15: "Lentil", 16: "Blackgram",
            17: "Mungbean", 18: "Mothbeans", 19: "Pigeonpeas", 20: "Kidneybeans",
            21: "Chickpea", 22: "Coffee"
        }

        if prediction[0] in crop_dict:
            crop = crop_dict[prediction[0]]
            result = "{} is the best crop to be cultivated right there.".format(crop)
        else:
            result = "Sorry, we could not determine the best crop to be cultivated with the provided data."
    except Exception as e:
        print(f"Error: {e}")
        result = "An error occurred during prediction."

    # Rendering result
    return render_template('index.html', result=result)


# Running the Flask app
if __name__ == "__main__":
    app.run(debug=True)
