# RECIPE-MANAGEMENT-SYSTEM
# 🍽️ Recipe Management System

## 📌 Overview
A **Recipe Management System** built using Flask and MySQL that allows users to **add, store, search, and manage recipes** along with their ingredients and categories.

## ✨ Features
- 🔑 **User Authentication** (Register/Login using Flask-Login)
- 📜 **Add, Edit, and Delete Recipes**
- 🛒 **Ingredient & Category Management**
- 🔍 **Search Functionality** for Recipes
- 📸 **Image Upload Support** (Flask-WTF, Werkzeug)
- 🎨 **Interactive UI** (HTML, CSS, JavaScript)
- 📊 **Database Storage using MySQL,XAMP**

## 🛠️ Technologies Used
- **Backend:** Flask (Python), Flask-Login, Flask-WTF
- **Frontend:** HTML, CSS, JavaScript
- **Database:** MySQL (Flask-SQLAlchemy)
- **Authentication:** Flask-Login

## 🚀 Installation & Setup
### 🔹 Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- MySQL
- Virtual Environment (optional but recommended)

### 🔹 Setup Steps

 **Create a Virtual Environment (Optional)**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

 **Install Required Dependencies**
```bash
   pip install -r requirements.txt
```

**Set Up the Database**
- Open MySQL and create a database:
```sql
   CREATE DATABASE recipe_db;
```
- Update **config.py** with your MySQL credentials.
- Run database migrations (if using Flask-Migrate):
```bash
   flask db upgrade
```

 **Run the Application**
```bash
   flask run
``
