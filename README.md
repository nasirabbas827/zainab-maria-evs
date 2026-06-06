# zainab-maria_final_evs  

A **Python/Django** based Electronic Voting System (EVS) that provides a secure, user‑friendly platform for managing candidates, voter registration, and vote casting. The project includes a simple blockchain implementation to ensure vote integrity.

---  

## Overview  

The repository contains a complete Django application with:

* **User management** – registration, authentication, profile handling.  
* **Candidate management** – upload and display of candidate information (e.g., date sheets, images).  
* **Blockchain‑backed voting** – each vote is recorded as a block, guaranteeing immutability.  
* **Media handling** – static and uploaded images stored under `media/`.  

The project is ready for local development and can be deployed to any WSGI‑compatible host.

---  

## Features  

| Feature | Description |
|---------|-------------|
| **Secure Authentication** | Django’s built‑in auth system with custom forms. |
| **Candidate Dashboard** | Upload and view candidate assets (PNG, JPG). |
| **Blockchain Voting** | Each vote creates a new block; tamper‑evident ledger. |
| **Admin Interface** | Full CRUD for users, candidates, and votes via Django admin. |
| **Responsive Media** | Images served from `media/` with automatic scaling. |
| **REST‑ready** | Project structure allows easy addition of DRF endpoints. |

---  

## Tech Stack  

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.9+, Django 4.x |
| **Database** | SQLite (default) – replace with PostgreSQL/MySQL for production |
| **Blockchain** | Custom lightweight Python implementation (`users/blockchain.py`) |
| **Front‑end** | Django templates + Bootstrap (optional) |
| **Containerisation** | Not included – can be added with Docker if required |
| **Dependencies** | Listed in `requirements.txt` |

---  

## Installation  

> **Prerequisites**  
> * Python 3.9 or newer  
> * Git  
> * (Optional) Virtual environment tool – `venv` or `conda`

```bash
# 1. Clone the repository
git clone https://github.com/your-username/zainab-maria_final_evs.git
cd zainab-maria_final_evs

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. (Optional) Create a superuser for the admin panel
python manage.py createsuperuser
```

---  

## Usage  

```bash
# Start the development server
python manage.py runserver
```

* Visit `http://127.0.0.1:8000/` to access the voting portal.  
* Admin interface is available at `http://127.0.0.1:8000/admin/`.  

### Basic workflow  

1. **Register / log in** – voters create an account or use existing credentials.  
2. **View candidates** – images and date sheets are displayed from `media/candidates/`.  
3. **Cast a vote** –