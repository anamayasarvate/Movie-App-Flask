from flask import Flask, escape, request, render_template
import json
import requests
import os

url = 'https://www.omdbapi.com/?s={}&apikey=82793b2a' # Using this one to display a list of results
url_2 = 'https://www.omdbapi.com/?t={}&apikey=82793b2a' # Using this one to see detail of a movie
results = [] # This list will help display search results
fav_list = [] # This list will be used to write in JSON file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') # Displaying the home page

@app.route('/favorites-list')
def favorites_list():
    #Read out favorited movies.
    filename = os.path.join('data.json')
    with open(filename) as data_file:
        data = json.load(data_file)
        return render_template('favorites.html', data = data)

# Displaying the details of a movie
@app.route('/detail', methods=['POST'])
def detail():
	if request.method == 'POST':
		movie = request.form['movie']
		r = requests.get(url_2.format(movie)).json()
		title = r['Title']
		year = r['Year']
		plot = r['Plot']
		type = r['Type']
		poster = r['Poster']
		return render_template('movie.html', movie = movie, title = title, year = year, plot = plot, type= type, poster = poster )

# This will add the selected movie to json file
@app.route('/favorites-add', methods=['POST'])
def favorites_add():
	if request.method == 'POST':
		title = request.form['title']
		fav_list.append(title)
		with open('data.json', 'w') as f:
			json.dump(fav_list, f)
			
		return render_template('index.html')

# Finding the list of movies with the API and sending the results to search_results.html
@app.route('/search', methods=['POST'])
def search():
	if request.method == 'POST':
		title = request.form['title']
		r = requests.get(url.format(title)).json()
		if r['Response'] == 'False':
			return render_template('index.html')
		else:
			results.clear()
			for movie in r['Search']:		
				results.append(movie['Title'])
			return render_template('search_results.html', results = results, title = title)

