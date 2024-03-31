from flask import Flask, request, render_template
import sys
import os

# __file__ here refers to the location of this script: backend/__init__.py
# We need to go up one level to the root of the project to get the correct paths
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
codecompasslib_path = os.path.join(project_root, 'codecompasslib')
frontend_path = os.path.join(project_root, 'frontend')
sys.path.insert(0, codecompasslib_path)
sys.path.insert(0, frontend_path)

# Now you can import from codecompasslib
from codecompasslib.models.model_diff_repos_mlops import main

app = Flask(__name__, template_folder=os.path.join(project_root, 'frontend'))

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
    recommendations = main(user_input, number_of_recommendations=1, return_neighbors=False)
    
    # Return the recommendations to the user
    # You might need to adjust this depending on your output format
    return render_template('search.html', recommendations=recommendations)