from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db_1"
# mongo = PyMongo(app, uri=f'mongodb://{host_name}/mars_app')
mongo = PyMongo(app)
mars = mongo.db
#mars.collection.drop()
@app.route("/")
def home():
    mars_dictionary = mars.mars_dict.find_one()
    print(mars_dictionary)
    return render_template("index.html", mars = mars_dictionary)


@app.route("/scrape")
def scrape():
    mars_dict = mongo.db.mars_dict
    mars_data = scrape_mars.scrape_all()
    mars_dict.update({}, mars_data, upsert=True)
      # redirect to home
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)    