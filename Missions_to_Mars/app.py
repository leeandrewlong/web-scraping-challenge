# 1. import Flask
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")
# 3. Define what to do when a user hits the index route
@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    print("mars text debug log", mars)
    return render_template('index.html', mars=mars)


# 4. Define what to do when a user hits the /about route
@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scrape_mars.scrape()
    print("mars text debug log scrape", mars_data)
    mars.update_one(
        {},
        {"$set":mars_data},
        upsert=True
    )
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
