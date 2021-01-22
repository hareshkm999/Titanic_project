from wsgiref import simple_server
from flask import Flask, request, render_template
import pickle
import json
import numpy as np
"""
*****************************************************************************
*
* filename:       main.py
* version:        1.0
* author:         Harish
* creation date:  22-JAN-2021
*
* change history:
*
* who             when           version  change (include bug# if apply)
* ----------      -----------    -------  ------------------------------
* HARISH          22-JAN-2021    1.0      initial creation
*
*
* description:    flask main file to run application
*
****************************************************************************
"""

app = Flask(__name__)

def predict_servival(Pclass, Sex, Age, SibSp, Parch, Fare, Cabin, Lname, NamePrefix):
    """
    * method: predict_servival
    * description: method to predict the results
    * return: prediction result
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * HARISH          22-JAN-2021    1.0      initial creation
    *
    """
    with open('models/Titanic.pkl', 'rb') as f:
        model = pickle.load(f)

    with open("models/columns.json", "r") as f:
        data_columns = json.load(f)['data_columns']

    x = np.zeros(len(data_columns))
    x[0] = Pclass
    x[1] = Sex
    x[2] = Age
    x[3] = SibSp
    x[4] = Parch
    x[5] = Fare
    x[6] = Cabin
    x[7] = Lname
    x[8] = NamePrefix

    if model.predict([x])[0] == 0:
        str1 = 'No more'
    else:
        str1 = 'Servived'

    return str1

@app.route('/')
def index_page():
    """
    * method: index_page
    * description: method to call index html page
    * return: index.html
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * HARISH          22-JAN-2021    1.0      initial creation
    *
    * Parameters
    *   None
    """
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    """
    * method: predict
    * description: method to predict
    * return: index.html
    *
    * who             when           version  change (include bug# if apply)
    * ----------      -----------    -------  ------------------------------
    * HARISH          22-JAN-2021    1.0      initial creation
    *
    * Parameters
    *   None
    """
    if request.method == 'POST':
        Pclass = request.form['Pclass']
        Sex = request.form["Sex"]
        Age = request.form["Age"]
        SibSp = request.form["SibSp"]

        Parch = request.form['Parch']
        Fare = request.form["Fare"]
        Cabin = request.form["Cabin"]
        Lname = request.form["Lname"]
        NamePrefix = request.form["NamePrefix"]

        output = predict_servival(Pclass, Sex, Age, SibSp, Parch, Fare, Cabin, Lname, NamePrefix)
        return render_template('index.html',show_hidden=True, prediction_text='This Project copy rights to Harish Musti and Pasenger is  {}'.format(output))


if __name__ == "__main__":
    #app.run(debug=True)
    host = '0.0.0.0'
    port = 5005
    httpd = simple_server.make_server(host, port, app)
    httpd.serve_forever()