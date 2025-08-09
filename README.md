# 🍽️ Recipe Notebook API

A **FastAPI-powered backend** for managing and sharing cooking recipes, with **secure authentication**, the ability to **rate and save recipes**, and powerful **search** capabilities.

***

## 🚀 Core Features

### 👤 **User Accounts**
- **Register** with a unique email & username
- **Login** using JWT-based authentication
- **Password security** with `bcrypt` hashing
- **Profile** – View all recipes created by the logged-in user (with average ratings)

***

### 📄 **Recipes**
A registered user can:
- **Create** recipes – including:
  - Title
  - List of ingredients
  - Cooking instructions
  - Tags (comma-separated categories)
- **Edit & Delete** only their own recipes
- **View** all recipes from all users
- **Get recipe details** by ID (including its average rating)

***

### 🌟 **Ratings**
- Users can **rate other users’ recipes** (1–5 stars, integers)
- Limitations:
  - ❌ Can’t rate your own recipe
  - ❌ Can rate a recipe **only once**
- Average rating is calculated automatically whenever recipes are listed or fetched

***

### 📌 **Saved Recipes**
- Users can **save/bookmark** recipes from other users for later viewing
- Limitations:
  - ❌ Can’t save your own recipe
  - ❌ Can’t save the same recipe twice
- Saved recipes can be **unsaved anytime**
- View all saved recipes in one place

***

### 🔍 **Searching Recipes**
- Find recipes by:
  - **Name** (case-insensitive partial match)
  - **Ingredients** (comma-separated list; finds recipes containing all given ingredients)
- Search works across the entire recipe database

***

## 🔐 **Permissions & Limitations Overview**

| Feature                        | Who Can Use?             | Limitations                                                                 |
|--------------------------------|--------------------------|------------------------------------------------------------------------------|
| **Register**                   | Anyone                   | Email must be unique                                                        |
| **Login**                      | Registered users         | Requires correct email+password                                             |
| **Create Recipe**               | Logged-in users          | None (except valid data)                                                     |
| **Edit Recipe**                 | Recipe owner only        | ❌ Cannot edit others’ recipes                                               |
| **Delete Recipe**               | Recipe owner only        | ❌ Cannot delete others’ recipes                                             |
| **Rate Recipe**                 | Logged-in users          | ❌ Cannot rate own recipe ❌ Can rate only once per recipe                |
| **Save Recipe**                 | Logged-in users          | ❌ Cannot save own recipe ❌ Cannot save same recipe twice                |
| **Unsave Recipe**               | Logged-in users          | Only for recipes they have saved                                             |
| **View All Recipes**            | Anyone                   | No login required                                                            |
| **View Saved Recipes**          | Logged-in users          | Shows only logged-in user’s saved recipes                                    |
| **Search Recipes**              | Anyone                   | No login required                                                            |
| **View Profile**                | Logged-in users          | Shows only logged-in user’s own recipes                                      |

***

## 🛠️ Tech Stack

- **FastAPI** – Web framework
- **SQLAlchemy** – ORM for DB operations
- **SQL** - DataBase
- **JWT** – Authentication (`python-jose`)
- **Pydantic** – Request/response validation
- **Uvicorn** – ASGI server

***
## DataBase SQL example URL: ```mysql+pymysql://username:password@localhost:3306/mydatabase```
## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Raghu889/Recipe-NoteBook.git
cd Recipe-NoteBook

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install --no-cache-dir -r requirements-docker.txt
```

***

## ▶️ Running the App

```bash
uvicorn app.main:app --reload
```

The API will be available at:  
**http://127.0.0.1:8000**  

Open the **interactive API docs** at:  
**http://127.0.0.1:8000/docs**

***

## 📫 API Endpoints

### **Authentication**
| Method | Endpoint             | Description           |
| ------ | -------------------- | --------------------- |
| POST   | `/api/auth/register` | Register new user     |
| POST   | `/api/auth/login`    | Login and get JWT     |
| GET    | `/api/auth/profile`  | View your own recipes |

***

### **Recipes**
| Method | Endpoint                                | Description                                 |
| ------ | --------------------------------------- | ------------------------------------------- |
| GET    | `/api/recipe/`                          | List all recipes                            |
| GET    | `/api/recipe/{id}`                      | Get recipe by ID                            |
| POST   | `/api/recipe/`                          | Create recipe (auth required)               |
| PUT    | `/api/recipe/{id}`                      | Update own recipe (auth required)           |
| DELETE | `/api/recipe/{id}`                      | Delete own recipe (auth required)           |

***

### **Saved Recipes**
| Method | Endpoint                  | Description                                 |
| ------ | ------------------------- | ------------------------------------------- |
| GET    | `/api/recipe/user/save`   | View your saved recipes                     |
| POST   | `/api/recipe/{id}/save`   | Save recipe (auth required)                 |
| DELETE | `/api/recipe/{id}/unsave` | Unsave recipe (auth required)               |

***

### **Ratings**
| Method | Endpoint                  | Description                                 |
| ------ | ------------------------- | ------------------------------------------- |
| POST   | `/api/recipe/{id}/rate`   | Rate recipe (auth required)                 |

***

### **Search**
| Method | Endpoint                  | Description                                 |
| ------ | ------------------------- | ------------------------------------------- |
| GET    | `/api/recipe/user/search` | Search by name and/or ingredients           |

***

## 📝 Example Usage Flow

1. **Register & Login** to receive your JWT token
2. **Create** a recipe
3. Another user **rates** and **saves** your recipe
4. Users can **search**, **view**, and **unsave** recipes
5. You can only **edit/delete** recipes you created
6. You cannot rate or save your own recipes

***

