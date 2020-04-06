import pandas as pd
import math

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


# Register the '/' route to this function, this handles the main page: 'http://localhost:5000/'
@app.route('/')
def main_page():  # Just a normal function, I named it this way for cleaner code
    # Okay, we render the index.html, then return the html string.

	d = pd.read_html('https://koronavirus.gov.hu/elhunytak')
	df = d[0]

	# converting to list 
	#meg kell adni az oszlop nevét, itt valamiért nagyon rosszul fogadta csak be
	#ageList = df.loc[:,'\n          Kor        '].tolist()
	ageList = df[df.columns[2]].tolist()

	average = math.floor(sum(ageList)/len(ageList))

	#return 'Az elhunytak átlagéletkora:   %d' % average

	return render_template('index.html', average=average)
if __name__ == "__main__":
    app.run(
        debug=True, # Allow verbose error reports
        port=5000 # Set custom port
    )
