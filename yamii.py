import pymongo
import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env



app = Flask(__name__)


# env connection
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# default route. 


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recipes')
def recipes():
    recipes = mongo.db.recipes.find()
    return render_template('recipes.html', recipes=mongo.db.recipes.find())


@app.route('/add_recipe')
def add_recipe():
    return render_template('add_recipe.html', recipes=mongo.db.recipes.find(), category=mongo.db.category.find())


@app.route('/load_image')
def load_image():
    if 'recipe_image' in request.files:
        recipe_image = request.files['recipe_image']
        mongo.save_file(recipe_image.filename, recipe_image)
    return render_template('add_recipe.html', recipe=mongo.db.recipes.find())


@app.route('/image/<recipe_image>')
def image():
    return mongo.send_file(recipe_image)


@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes = mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('recipes'))


@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    _recipe = mongo.db.recipes.find_one({'_id':ObjectId(recipe_id)})
    _category = mongo.db.category.find()
    category_list = [category for category in _category]
    return render_template('edit_recipe.html', recipe =_recipe, category=category_list)


@app.route('/update_recipe/<recipe_id>', methods = ['POST'])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update({'_id':ObjectId(recipe_id)},
    {
        'recipe_name':request.form.get('recipe_name'),'category_name':request.form.get('category_name'),
        'ingredients':request.form.get('ingredients'),
        'steps':request.form.get('steps')
    })
    return redirect(url_for('recipes'))


@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id':ObjectId(recipe_id)})
    return redirect(url_for('recipes'))
    

@app.route('/shop')
def shop():
    return render_template('shop.html')


@app.route('/shopping_cart')
def shopping_cart():
    return render_template('shopping_cart.html')


@app.route('/subscription')
def subscription():
    return render_template('subscription.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # existing users DB
        existing_user = mongo.db.users.find_one({"username": request.form.get("username").lower()})

        if existing_user:
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # new user 'session' cookie
        session["user"] = request.form.get("username").lower()
    return render_template('register.html')


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if user exist in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password match
            if check_password_hash(existing_user["password"], request.form.get      ("password")):
                    session["user"] = request.form.get("username").lower()
            else:
                return redirect(url_for("login"))

        else:
            return redirect(url_for("login"))

    return render_template('login.html')


if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)
