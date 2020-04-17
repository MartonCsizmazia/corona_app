import pandas as pd
import math
from collections import Counter
import operator


from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

GENDER = 1
AGE = 2
SICKNESS = 3

def dataFrameMaker():
    d = pd.read_html('https://koronavirus.gov.hu/elhunytak')
    df = d[0]
    return df

def ageListMaker():
    df = dataFrameMaker()
    # converting to list
    # in normal you have to give the coulms name, in this it accepted only this way
    # ageList = df.loc[:,'\n          Kor        '].tolist()
    ageList = df[df.columns[2]].tolist()
    x = 0
    urlBase = 'https://koronavirus.gov.hu/elhunytak?page='
    while True:
        try:
            x += 1
            url = urlBase + str(x)
            d = pd.read_html(url)
            df = d[0]
            ageList2 = df[df.columns[2]].tolist()
            ageList += ageList2
        except ValueError:
            break
    return ageList

def tempListMaker(column):
    df = dataFrameMaker()
    tempList = df[df.columns[column]].tolist()
    x = 0
    urlBase = 'https://koronavirus.gov.hu/elhunytak?page='
    while True:
        try:
            x += 1
            url = urlBase + str(x)
            d = pd.read_html(url)
            df = d[0]
            sicknessList2 = df[df.columns[column]].tolist()
            tempList += sicknessList2
        except ValueError:
            break
    return tempList

def ListMaker(column):
    List = []
    comaList = []
    tempList = tempListMaker(column)
    for string in tempList:
        if "," in string:
            sliced = string.split(", ")
            for word in sliced:
                comaList.append(word)
        else:
            comaList.append(string)

    for string in comaList:
        if "," in string:
            sliced = string.split(",")
            for word in sliced:
                List.append(word)
        else:
            List.append(string)

    return List



def DictionaryMaker(column):
    List = ListMaker(column)
    how_many = dict(Counter(List))
    how_many = sorted(how_many.items(), key=operator.itemgetter(1), reverse=True)
    return how_many


def mostCommonMaker():
    how_many = DictionaryMaker(SICKNESS)
    most_common = []
    HOW_MUCH_MOST_COMMON = 3
    for idx, sickness in enumerate(how_many):
        if idx < HOW_MUCH_MOST_COMMON:
            print(sickness[0])
            most_common.append(sickness)
        else:
            break
    return most_common

@app.route('/')
def main_page():
    # Just a normal function, I named it this way for cleaner code
    # Okay, we render the index.html, then return the html string.

    ageList = ageListMaker()
    most_common = mostCommonMaker()
    average = math.floor(sum(ageList) / len(ageList))

    return render_template('index.html', average=average, most_common=most_common, number_of_deaths=len(ageList))


# A welcome message to test our server
@app.route('/welcome')
def index():
    return "<h1>Welcome to our server !!</h1>"

@app.route('/main')
def newindex():
    ageList = ageListMaker()
    most_common = mostCommonMaker()
    average = math.floor(sum(ageList) / len(ageList))
    minAge = min(ageList)
    maxAge = max(ageList)

    genderDictionary = DictionaryMaker(GENDER)
    print (genderDictionary)
    return render_template('newindex.html', average=average, most_common=most_common, number_of_deaths=len(ageList), minAge=minAge, maxAge=maxAge,genderDictionary=genderDictionary)

@app.route('/diseases')
def diseases():
    sicknesses = DictionaryMaker(SICKNESS)
    return render_template("disease.html", sicknesses=sicknesses)

if __name__ == "__main__":
    app.run(
        debug=True,  # Allow verbose error reports
        port=5000  # Set custom port
    )
