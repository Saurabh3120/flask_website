# FlaskCraft - Modern & Responsive Python Flask Website

A clean, responsive, and lightweight multi-page website built with **Python Flask**, **Jinja2 templates**, and **pure modern CSS**.

---

## 🌟 Features

- **Multi-Page Architecture:**
  - **Home (`/`):** Dynamic hero section, feature cards, architecture overview, and calls to action.
  - **Blog & Articles (`/blog`):** Dynamic articles system with category filtering, reading views, and post management.
  - **Article Editor (`/blog/create`):** Protected publishing studio allowing registered authors to publish new posts directly into SQLite.
  - **About (`/about`):** Mission statement, core principles, key performance stats, and company vision.
  - **Contact (`/contact`):** Interactive contact form with server-side validation, direct contact details, FAQ accordions, and automatic saving into SQLite.
  - **Messages Inbox (`/messages`):** Dedicated admin inbox interface to review and delete submitted contact messages stored in SQLite (Protected by authentication).
  - **User Authentication (`/signup`, `/login`, `/logout`):** Full user registration & login system with secure PBKDF2 password hashing.
  - **User Dashboard (`/dashboard`):** Personalized user profile page displaying account details, stats, recent messages, and quick actions.
  - **Custom Error Handling:** Styled, user-friendly `404 Not Found` and `500 Server Error` pages.
- **SQLite Database Integration:**
  - Zero-configuration local database (`database.db`) using Python's standard `sqlite3` library.
  - Auto-initializes `messages`, `users`, and `posts` tables on server startup with seed articles.
  - Securely hashes user passwords using Werkzeug's `generate_password_hash` & `check_password_hash`.
  - Persists `id`, `name`, `email`, `subject`, `message`, articles, and timestamps.
- **Production & Cloud Ready:**
  - Includes `Procfile`, `render.yaml`, and `gunicorn` for 1-click cloud deployment on Render, PythonAnywhere, or Railway.
- **Clean & Responsive Design:**
  - Crafted with pure CSS (no bloated frameworks required).
  - Fluid CSS Grid and Flexbox layouts.
  - Mobile-first approach with a slide-down hamburger drawer on mobile and tablet screens.
  - Modern typography (Inter font stack) and high-contrast accessible color scheme.
- **Robust Flask Backend:**
  - Jinja2 template inheritance with a unified `base.html` layout.
  - Form handling with validation and Flask's built-in `flash()` messaging system.
  - Configurable `SECRET_KEY` environment variable for production readiness.

---

## 📁 Project Structure

```text
mini_website/
│
├── app.py                     # Main Flask application, routes & SQLite DB logic
├── database.db                # SQLite database file (auto-created on startup)
├── Procfile                   # Cloud web process entrypoint (gunicorn)
├── render.yaml                # Render.com 1-click cloud deployment blueprint
├── requirements.txt           # Python package dependencies (Flask, Gunicorn)
├── README.md                  # Setup and usage documentation
├── .gitignore                 # Files excluded from version control
│
├── static/
│   ├── css/
│   │   └── style.css          # Modern, responsive stylesheet, blog & auth UI
│   └── js/
│       └── main.js            # Mobile menu, flash message auto-dismiss, smooth scroll
│
└── templates/
    ├── base.html              # Base layout (header, dynamic auth navbar, alerts, footer)
    ├── index.html             # Home page template
    ├── about.html             # About page template
    ├── contact.html           # Contact page & form template
    ├── messages.html          # SQLite messages inbox template (Protected)
    ├── blog.html              # Blog articles listing & category filters
    ├── blog_detail.html       # Single article reading template
    ├── create_post.html       # Article publishing studio (Protected)
    ├── signup.html            # User registration template
    ├── login.html             # User login template
    ├── dashboard.html         # User profile and stats dashboard
    ├── 404.html               # Custom 404 error template
    └── 500.html               # Custom 500 error template
```

---

## 🚀 Getting Started

Follow these steps to run the website locally on your computer.

### 1. Prerequisites

Ensure you have **Python 3.8 or newer** installed:

```bash
python --version
```

---

### 2. (Recommended) Create & Activate a Virtual Environment

Isolate your project dependencies by creating a virtual environment:

- **On Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

- **On Windows (Command Prompt):**
  ```cmd
  python -m venv venv
  .\venv\Scripts\activate.bat
  ```

- **On macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

---

### 3. Install Dependencies

Install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

---

### 4. Run the Application

Start the Flask development server:

```bash
python app.py
```

You should see output similar to:

```text
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```

---

### 5. Open in Your Browser

Open your favorite web browser and visit:

👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)** (or `http://localhost:5000`)

---

## 🧪 Testing the Pages

1. **Home (`/`):** View the hero showcase, feature grid, and navigate using the top navbar.
2. **About (`/about`):** Read through the story, stats, and guiding values.
3. **Contact (`/contact`):**
   - Submit the form with empty fields or an invalid email to test input validation errors.
   - Submit a valid message (e.g., Name: `Alex`, Email: `alex@example.com`, Subject: `Website Feedback`, Message: `Looks great!`).
   - Notice the green success alert banner confirming message receipt.
4. **404 Page (`/non-existent-page`):** Try navigating to a random URL like `http://127.0.0.1:5000/random` to see the custom 404 page.
5. **Mobile Responsiveness:** Open DevTools in your browser (`F12`), toggle device emulation (e.g., iPhone or Pixel), and test the mobile hamburger menu navigation.

---

## ⚙️ Configuration & Customization

- **Change Port or Host:**
  In `app.py`, modify the `app.run()` parameters:
  ```python
  app.run(host='0.0.0.0', port=8080, debug=True)
  ```
- **Custom Secret Key:**
  Set an environment variable before running:
  ```bash
  # Windows PowerShell
  $env:SECRET_KEY="your-super-secret-key"

  # Linux/macOS
  export SECRET_KEY="your-super-secret-key"
  ```

---

## 🌐 Free Live Deployment Guide

You can deploy this website to the internet for free so anyone can visit it.

### Option A: Deploy on Render.com (Recommended & Fastest)
1. Push your project code to a **GitHub** repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of FlaskCraft website"
   git remote add origin https://github.com/your-username/your-repo.git
   git push -u origin main
   ```
2. Go to **[Render.com](https://render.com)** and sign up for a free account.
3. Click **New +** &rarr; **Web Service**.
4. Connect your GitHub repository.
5. Render will automatically detect settings from `Procfile` and `render.yaml`:
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. Click **Create Web Service**. Within 1–2 minutes, your website will be live at `https://your-app-name.onrender.com`!

### Option B: Deploy on PythonAnywhere
1. Create a free account at **[PythonAnywhere.com](https://www.pythonanywhere.com)**.
2. Under the **Web** tab, click **Add a new web app**, choose **Flask** and select **Python 3.10+**.
3. Upload your project files or clone via Git in the Bash console.
4. Point the WSGI configuration file to `app.py`.
5. Reload the web app and open your free `yourusername.pythonanywhere.com` domain.

---

## 📄 License

This project is open-source and free to use for personal or commercial projects.
