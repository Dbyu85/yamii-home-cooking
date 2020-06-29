import pymongo
import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo 
from bson.objectid import ObjectId 

app = Flask(__name__)

MONGODB_URI = os.getenv("MONGO_URI")
DBS_NAME ="yamiiHomeCooking"
COLLECTION_NAME = "category", "recipes"


app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost')
mongo = PyMongo(app)

def mongo_connect("url"):
    try:
        conn = pymongo.MongoClient(url)
        print("mongo")
        return conn
    except pymongo.error.Connectionfailure as e:
        print('error: %s') % e

conn = mongo_connect(MONGODB_URI)

coll = conn[DBS_NAME][COLLECTION_NAME]

documents = coll.find()

for doc in documents:
    print (doc)




#default route. 
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recipes')
def recipes():
    return render_template('recipes.html', recipes=mongo.db.recipes.find())

@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html', recipes=mongo.db.recipes.find(), category=mongo.db.category.find())

@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('recipes'))

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/subscription')
def subscription():
    return render_template('subscription.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)