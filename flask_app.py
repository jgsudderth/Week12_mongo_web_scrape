from flask import Flask, render_template, jsonify, redirect
import pymongo
import scrape_mars

app = Flask(__name__)
print(app)
conn ='mongodb://localhost:27017'

mongo = pymongo.MongoClient(conn)

db=mongo.mars_db
# Use flask_pymongo to set up mongo connection
#mongo = PyMongo(app)

@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   print(mars)
   return render_template("index.html", mars=mars)
   
   
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    mars.update({}, mars_data, upsert=True)
    message = "Scraping Successful!"
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
