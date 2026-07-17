from flask import Flask, render_template, request
import pickle
import pandas as pd

# Create Flask App
app = Flask(__name__)

# Load trained model
with open("space_object_classifier.pkl", "rb") as file:
    model = pickle.load(file)

# Load Label Encoder
with open("label_encoder.pkl", "rb") as file:
    le = pickle.load(file)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/reset")
def reset():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    OPS_STATUS_CODE = request.form["OPS_STATUS_CODE"]
    OWNER = request.form["OWNER"]
    LAUNCH_SITE = request.form["LAUNCH_SITE"]

    PERIOD = float(request.form["PERIOD"])
    INCLINATION = float(request.form["INCLINATION"])
    APOGEE = float(request.form["APOGEE"])
    PERIGEE = float(request.form["PERIGEE"])

    ORBIT_CENTER = request.form["ORBIT_CENTER"]
    ORBIT_TYPE = request.form["ORBIT_TYPE"]

    LAUNCH_YEAR = int(request.form["LAUNCH_YEAR"])


    input_data = pd.DataFrame({
        "OPS_STATUS_CODE": [OPS_STATUS_CODE],
        "OWNER": [OWNER],
        "LAUNCH_SITE": [LAUNCH_SITE],
        "PERIOD": [PERIOD],
        "INCLINATION": [INCLINATION],
        "APOGEE": [APOGEE],
        "PERIGEE": [PERIGEE],
        "ORBIT_CENTER": [ORBIT_CENTER],
        "ORBIT_TYPE": [ORBIT_TYPE],
        "LAUNCH_YEAR": [LAUNCH_YEAR]
    })


    # Predict encoded class
    prediction = model.predict(input_data)


    # Decode prediction back to original label
    prediction = le.inverse_transform(prediction)


    prediction = prediction[0]


    prediction_labels = {
        "DEB": "🛰 Debris (DEB)",
        "PAY": "🛰 Payload (PAY)",
        "R/B": "🚀 Rocket Body (R/B)",
        "UNK": "❓ Unknown Object (UNK)"
    }


    result = prediction_labels.get(prediction, prediction)


    return render_template("index.html", result=result)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)