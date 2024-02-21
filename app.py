from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import pickle
from monkelib.models.model_diff_repos import clean_code

app = Flask(__name__, template_folder='frontendmd')

# The route() function of the Flask class is a decorator, 
# which tells the application which URL should call 
# the associated function.
@app.route('/')
def index():
    # This will render the search.html template
    return render_template('search.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    # Extract data from form
    
    user_input = request.form['user_input']
    
    
    # Assuming your model's function is named "recommend"
    recommendations = clean_code(user_input)
    
    
    # Return the recommendations to the user
    # You might need to adjust this depending on your output format
    return render_template('search.html', recommendations=recommendations)



# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application 
	# on the local development server.
	app.run(debug=True, port=5000)