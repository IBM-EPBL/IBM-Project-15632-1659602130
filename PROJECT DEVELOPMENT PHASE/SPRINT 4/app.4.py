import os
import numpy as np 
from flask import Flask,request,render_template 
import pickle
import requests



# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "YdvedR02ZwG55_f0h2MOZ6AqnfX8cUoa5k9vNev56q8X"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}




app= Flask(__name__)
# model = pickle.load(open('/Users/balasaravananvp/Documents/tensorflow-test/IBM-Project-26380-1660025744/Project Development Phase/Sprint 4/gow.pkl', 'rb')) # loading the trained model

@app.route("/") 
def about():
    return render_template("about.html")

@app.route("/about")
def home():
    return render_template("about.html")

@app.route("/info") 
def information():
    return render_template("info.html")


@app.route("/predict",methods=["GET","POST"]) 
def upload():
    if request.method=='POST':
        init_features = [float(x) for x in request.form.values()]

        payload_scoring = {"input_data": 
			[{"field": [["f0", "f1","f2","f3","f4","f5"]], 
                "values": [init_features]}]}
        print(payload_scoring)
        response_scoring = requests.post('https://eu-gb.ml.cloud.ibm.com/ml/v4/deployments/1729ff17-6cec-4697-afee-e59bb6cc3c9c/predictions?version=2022-11-13', json=payload_scoring, headers={'Authorization': 'Bearer ' + mltoken})
        print("Scoring response")
        predictions =response_scoring.json()
        print(predictions)
        print('Final Prediction Result',predictions['predictions'][0]['values'][0][0])


        pred =response_scoring.json()

        output = pred['predictions'][0]['values'][0][0]
        return render_template("result.html",prediction='The WQI predicted is {:.2f}'.format(output))

    else:
        return render_template("predict.html")


if __name__=="__main__":
    app.run(debug=False,port=5500)
            
            