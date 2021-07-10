from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from flask import Flask, render_template, redirect, url_for 
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)
# use flask_pymongo to set up mongo connection
app.config["MONGO_URI"]="mongodb://localhost:27017/mars_app"
mongo=PyMongo(app)

# Define route for HTML page
@app.route("/")
def index():
    mars=mongo.db.mars.find_one()
    return render_template("index.html",mars=mars)

# Set up our scraping route then return a message when successful
@app.route("/scrape")
def scrape():
    # assign a new variable to point to our mongo db
    mars=mongo.db.mars
    # create a variable to hold scraped data
    mars_data=scraping.scrape_all()
    # update the database with an empty JSON object {}
    mars.update({},mars_data,upsert=True)
    # navigate back to our page where we can see the content
    return redirect('/', code=302)

if __name__ == "__main__":
    app.run()