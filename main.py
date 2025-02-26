from flask import Flask, redirect, render_template, request, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import send_from_directory
from sqlalchemy import or_
from datetime import datetime

local_server = True
app = Flask(__name__)
app.secret_key = "seiashibu"

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Configure the upload set and destination
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 22 * 1024 * 1024  

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/cook'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','image/*','pdf'}  # Add more if needed

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


db = SQLAlchemy(app)

# Association table for Recipe and Ingredient


# Association table for Recipe and Category
recipe_category = db.Table(
    'recipe_category',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True),
    db.Column('category_id', db.Integer, db.ForeignKey('category.category_id'), primary_key=True)
)

# Define your SQLAlchemy models
class Recipe(db.Model):
    __tablename__ = 'recipe'
    recipe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=True)
    category = db.Column(db.String(255), nullable=False)
    photo_data = db.Column(db.LargeBinary, nullable=True)

    type = db.Column(db.String(255), nullable=False)
    cuisine = db.Column(db.String(255), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
class Category(db.Model):
    __tablename__ = 'category'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(255), nullable=False)
    cuisine = db.Column(db.String(255), nullable=False)

class Ingredient(db.Model):
    __tablename__ = 'ingredient'
    ingredient_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)

class Register(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(1000))
    name = db.Column(db.String(255))
    dob = db.Column(db.String(255))

@login_manager.user_loader
def load_user(user_id):
    return Register.query.get(user_id)



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

@app.route('/recipe', methods=['POST'])
def upload_file():
    try:
        # Ensure 'photo' file is uploaded
        if 'photo' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)

        file = request.files['photo']

        # Ensure a file is selected
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)

        # Save file to UPLOAD_FOLDER
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        # Create new Recipe object and populate fields
        new_recipe = Recipe(
            name=request.form['name'],
            filename=file.filename,
            category=request.form['category'],  # Assign category from form data

            cuisine=request.form['cuisine'],
            type=request.form['type'],  # Ensure 'type' is included in form
            ingredients=request.form['ingredients'],
            description=request.form['description']

        )

        # Read and store photo_data
        with open(filename, 'rb') as f:
            new_recipe.photo_data = f.read()

        # Add new recipe to database session and commit
        db.session.add(new_recipe)
        db.session.commit()

        # Set flash message for successful upload
        flash('File successfully uploaded', 'success')
        return redirect(url_for('add'))# Redirect to 'return_page' route (return.html)

    except Exception as e:
        # Rollback changes on exception and return error response
        db.session.rollback()
        print(str(e))
        flash('not uploaded', 'danger')
        return redirect(url_for('add'))

    
@app.route('/add_ingredient', methods=['POST'])
def add_ingredient():
    try:

        name = request.form.get('name')
        description = request.form.get('description')

        new_ingredient = Ingredient(name=name, description=description)

        db.session.add(new_ingredient)
        db.session.commit()

        flash('Ingredient added successfully', 'success')
        return jsonify({'success': 'Ingredient added successfully'})

    except Exception as e:
        flash('Error adding ingredient: ' + str(e), 'danger')
        print(f"Error: {str(e)}")
        db.session.rollback()

    return jsonify({'error': 'Failed to add ingredient'})

@app.route('/search')
def search():
    query = request.args.get('query')
    if query:
        # Perform a search across multiple fields using ilike and or_
        results = Recipe.query.filter(
            or_(
                Recipe.name.ilike(f'%{query}%'),
                Recipe.type.ilike(f'%{query}%'),
                 Recipe.cuisine.ilike(f'%{query}%'),

                Recipe.category.ilike(f'%{query}%')
            )
        ).all()
    else:
        results = []

    recipes = [{
        'name': recipe.name,
        'filename': recipe.filename,
        'category': recipe.category,
        'photo_data': recipe.photo_data,
        'type': recipe.type,
        'cuisine': recipe.cuisine,
        'description': recipe.description,
        'ingredients': recipe.ingredients
    } for recipe in results]

    return render_template('search.html', results=recipes)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")  
@app.route("/register")
def registe():
    return render_template("register.html")    
def my_function():
    dob = "01-01-2000"
    print(dob)  # Now 'dob' is defined before usage

my_function()

@app.route("/signup", methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        user_id = request.form.get('id')
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        dob_str = request.form.get('dob')  # Get dob from form data

        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.today()
        if dob > today:
            flash("Date of Birth cannot be a future date.", "warning")
            return render_template("register.html")

        encpassword = generate_password_hash(password)
        user = Register.query.filter_by(id=user_id).first()
        emailUser = Register.query.filter_by(email=email).first()
        

        new_user = Register(id=user_id, name=name, email=email, password=encpassword, dob=dob)
        db.session.add(new_user)
        db.session.commit()
        flash("Register success, please login", "info")
        return render_template("login.html")

    return render_template("register.html")

# Route for logging in
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == "POST":
        id = request.form.get('id')
        email = request.form.get('email')
        password = request.form.get('password')
        user = Register.query.filter_by(id=id).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash("Login success", "info")
            return render_template("index.html")
        else:
            flash("Invalid credentials", "danger")
            return render_template("login.html")

    return render_template("login.html")
@app.route('/add_category', methods=['POST'])
def add_category():
    try:
        recipe_id = request.form.get('recipe_id')
        if recipe_id is None or not recipe_id.isdigit():
            flash('Invalid recipe ID', 'danger')
            return jsonify({'error': 'Invalid recipe ID'})

        recipe_id = int(recipe_id)  # Convert to integer if possible

        recipe = db.session.get(Recipe, recipe_id)

        if not recipe:
            flash('Recipe not found', 'danger')
            return jsonify({'error': 'Recipe not found'})

        type = request.form.get('type')
        cuisine = request.form.get('cuisine')

        new_category = Category(type=type, cuisine=cuisine)
        recipe.categories.append(new_category)

        db.session.add(new_category)
        db.session.commit()

        return jsonify({'success': 'Category added successfully'})

    except Exception as e:
        flash('Error adding category', 'danger')
        print(str(e))  # Print the actual exception for debugging
        db.session.rollback()
        return jsonify({'error': 'Failed to add category'})

# Route for logging out
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout success", "success")
    return redirect(url_for('signin'))

# Route for adding a recipe or navigating to the add page
@app.route('/add', methods=['GET'])
def add():
    return render_template("add.html")

@app.route ('/added', methods=['GET'])
def added():
    return render_template("added.html")

if __name__ == "__main__":
    app.run(debug=True)
