# 🍽️ Recipe Notebook API

A FastAPI-based backend for managing and sharing cooking recipes, with user authentication, recipe rating, saving, and searching features.

## 🚀 Features

- ✅ User registration and JWT-based login
- 🔐 Password hashing using `bcrypt` (`passlib`)
- 📄 Create, Read, Update, Delete (CRUD) operations for recipes
- 🌟 Rate recipes (users can rate others' recipes only once)
- 📌 Save/unsave favorite recipes (users can't save their own)
- 🔍 Search recipes by **name** or **ingredients**
- 🔐 Protected routes with role-based permissions

---

## 🛠️ Tech Stack

- **FastAPI** – Web framework
- **SQLAlchemy** – ORM
- **SQLite** – Default DB (easily swappable)
- **JWT** – Authentication via `python-jose`
- **Pydantic** – Data validation
- **Uvicorn** – ASGI server

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Raghu889/Recipe-NoteBook.git
cd Recipe-NoteBook

# (Optional) Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


```

Running App
uvicorn app.main:app --reload


Project Stucture:

```
recipe-notebook/
│
├── app/
│   ├── main.py               # FastAPI app setup & routes
│   ├── db.py                 # DB engine and session
│   ├── models/               # SQLAlchemy models
│   ├── routes/               # API routers (auth, recipe)
│   ├── schemas/              # Pydantic schemas
│   └── utils.py              # Utility functions (token, hashing)
│
├── requirements.txt          # Python dependencies
├── README.md                 # Project documentation

```

🔐 Authentication

  Token-based (JWT)

  Include token in requests using the Authorization header:

  Authorization: Bearer <your_token>
  
📫 API Endpoints:

Auth:
| Method | Endpoint             | Description           |
| ------ | -------------------- | --------------------- |
| POST   | `/api/auth/register` | Register a new user   |
| POST   | `/api/auth/login`    | Get JWT token (login) |


Recipes:
| Method | Endpoint                                                | Description                       |
| ------ | ------------------------------------------------------- | --------------------------------- |
| GET    | `/api/recipe/`                                          | Get all recipes                   |
| GET    | `/api/recipe/{id}`                                      | Get single recipe by ID           |
| POST   | `/api/recipe/`                                          | Create recipe (auth required)     |
| PUT    | `/api/recipe/{id}`                                      | Update own recipe (auth)          |
| DELETE | `/api/recipe/{id}`                                      | Delete own recipe (auth)          |
| GET    | `/api/recipe/user/save`                                 | Get saved recipes (auth)          |
| POST   | `/api/recipe/{id}/save`                                 | Save a recipe                     |
| POST   | `/api/recipe/{id}/rate`                                 | Rate a recipe (1 per user)        |
| GET    | `/api/recipe/user/search?name=pasta&ingredients=tomato` | Search by name and/or ingredients |

