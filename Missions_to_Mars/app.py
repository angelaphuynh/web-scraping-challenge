from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
# Import scrape_mars
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)


# Create connection variable
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Pass connection to the pymongo instance.
#client = pymongo.MongoClient(conn)

# Set route
@app.route('/')
def index():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scraper():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    #update the mars db w/ mars_data
    mars.update({}, mars_data, upsert=True)
    return index()

if __name__ == "__main__":
    app.run(debug=True) 