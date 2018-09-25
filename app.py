# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import pymongo
# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# connect to mongo db and collection
db = client.mars_data
collection = db.mars_scrape
# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/weather_app")


# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_dict = collection.find_one()

    # return template and data
    return render_template("index.html", mars_dict=mars_dict)

from scrape_mars import scrape
# Route that will trigger scrape functions
@app.route("/scrape")
def reload():

    # Run scraped functions
    mars_dict = scrape()
    #print (f'line 34 - {type(mars_dict)}')
    #print (f'printing {mars_dict}')  
    # Insert mars_data into database
    collection.update({"id": 1}, {"$set": mars_dict}, upsert = True)
   
    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
