# 🔗 HighLevel CRM Integration (OAuth + Contact Update)

This Django-based project demonstrates integration with the [HighLevel CRM](https://highlevel.stoplight.io/docs/integrations/0443d7d1a4bd0-overview) using OAuth 2.0.  
It securely authenticates a user, fetches a random contact, and updates the custom field `"DFS Booking Zoom Link"` with the value `"TEST"`.

---

## 🚀 Features

- OAuth 2.0 authorization with HighLevel
- Token and location ID stored in session
- Fetches a random contact from `/contacts/`
- Retrieves custom fields from `/locations/{locationId}/customFields` which matches it's value with 'DFS Booking Zoom Link
- Updates a contact's custom field via `/contacts/{contactId}/`

---

## 📦 Tech Stack

- **Backend**: Python, Django
- **HTTP Requests**: `requests` library
- **Frontend**: Django templates with inline styling
- **Authentication**: OAuth 2.0 + Django Sessions

---

## ⚙️ Local Setup Guide
### 1. Create Virtual Environment
```
python -m venv venv
source venv/bin/activate     # On Windows: venv\Scripts\activate
```
### 2. Clone the Repository

```bash
git clone https://github.com/vishnudas-max/CRM-Manager.git
cd CRM-Manager
```

### 3. Install dependancies
```
pip install path/to/requirement.txt

```

### 4.Add a .env File

Create a .env file in your root project directory with the following:
Example .env
````
HIGHLEVEL_CLIENT_ID = your-client-id-here
HIGHLEVEL_CLIENT_SECRET = your-client-secret-here
HIGHLEVEL_REDIRECT_URI = your redirect url here
````

### 5.Apply Migrations & Run Server
```
python manage.py migrate
python manage.py runserver
```

Visit http://127.0.0.1:8000

🗂️ Example Project Structure
CRM-Manager/
├── app/                          # Main Django app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
│
├── crmanager/                    # Django project folder
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/                       # Static files
│   └── src/
│       └── input.css
│
├── templates/                    # Django templates
│   ├── base.html
│   ├── contact.html
│   └── index.html
│
├── .env                          # Environment variables (secret)
├── .gitignore                    # Git ignore file
├── db.sqlite3                    # Default database
├── manage.py                     # Django management script
├── requirements.txt              # Python dependencies

📬 Contact
For any questions or improvements, feel free to raise an issue or contact me directly.

