import pandas as pd
import math
from collections import Counter
import operator


from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# Register the '/' route to this function, this handles the main page: 'http://localhost:5000/'
@app.route('/')
def main_page():  # Just a normal function, I named it this way for cleaner code
    # Okay, we render the index.html, then return the html string.

    d = pd.read_html('https://koronavirus.gov.hu/elhunytak')
    df = d[0]

    # converting to list
    # in normal you have to give the coulms name, in this it accepted only this way
    # ageList = df.loc[:,'\n          Kor        '].tolist()
    ageList = df[df.columns[2]].tolist()
    tempSicknessList = df[df.columns[3]].tolist()

    x = 0
    urlBase = 'https://koronavirus.gov.hu/elhunytak?page='
    while True:
        try:
            x += 1
            url = urlBase + str(x)
            d = pd.read_html(url)
            df = d[0]
            ageList2 = df[df.columns[2]].tolist()
            sicknessList2 = df[df.columns[3]].tolist()
            ageList += ageList2
            tempSicknessList += sicknessList2
        except ValueError:
            break

    # print(df)
    sicknessList = []

    for string in tempSicknessList:
        if "," in string:
            sliced = string.split(", ")
            for word in sliced:
                sicknessList.append(word)
        else:
            sicknessList.append(string)
    print(sicknessList[0])

    how_many = dict(Counter(sicknessList))

    how_many = sorted(how_many.items(), key=operator.itemgetter(1), reverse=True)
    most_common = []

    HOW_MUCH_MOST_COMMON = 3
    for idx, sickness in enumerate(how_many):
        if idx < HOW_MUCH_MOST_COMMON:
            print(sickness[0])
            most_common.append(sickness)
        else:
            break

    print(most_common)
    average = math.floor(sum(ageList) / len(ageList))

    return render_template('index.html', average=average, most_common=most_common, number_of_deaths=len(ageList))


# A welcome message to test our server
@app.route('/welcome')
def index():
    return "<h1>Welcome to our server !!</h1>"


if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
