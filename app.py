import os
import re
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# Secret key used for session security and flash messaging
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production-12345')

# Path to SQLite database file
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')
EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def get_db_connection():
    """Create a connection to the SQLite database with Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize the SQLite database and create tables if they do not exist."""
    conn = get_db_connection()
    # Messages table
    conn.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Users table for Authentication
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Posts table for Dynamic Blog & Articles
    conn.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            content TEXT NOT NULL,
            author_id INTEGER,
            author_name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (author_id) REFERENCES users (id)
        )
    ''')

    # Seed sample posts if blog table is currently empty
    post_count = conn.execute('SELECT COUNT(*) as count FROM posts').fetchone()['count']
    if post_count == 0:
        sample_posts = [
            (
                "Why Python Flask is the Ultimate Micro-Framework for Web Apps",
                "Backend",
                "Flask gives developers full architectural freedom without bloated defaults. With its minimalist core, battle-tested Werkzeug WSGI toolkit, and Jinja2 templating engine, Flask lets you build snappy, scalable web applications with complete clarity.",
                1,
                "FlaskCraft Team"
            ),
            (
                "Mastering Pure CSS: Grids, Flexbox, and Zero Heavy Frameworks",
                "Frontend",
                "Modern CSS has evolved remarkably. By utilizing CSS Custom Properties (variables), fluid Flexbox structures, and CSS Grid systems, we can create sleek, responsive, and accessible interfaces that load in milliseconds without large external dependencies.",
                1,
                "FlaskCraft Team"
            ),
            (
                "Zero-Config Relational Databases with Embedded SQLite",
                "Databases",
                "SQLite is the most widely deployed SQL database engine in software. Requiring no separate daemon process, it stores your entire dataset in a single portable file, making local development, unit testing, and lightweight production hosting completely effortless.",
                1,
                "FlaskCraft Team"
            )
        ]
        conn.executemany(
            'INSERT INTO posts (title, category, content, author_id, author_name) VALUES (?, ?, ?, ?, ?)',
            sample_posts
        )

    conn.commit()
    conn.close()


# Ensure database and tables are created upon initialization
init_db()


def login_required(f):
    """Decorator to protect routes requiring user authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in to access this page.", "error")
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


@app.before_request
def load_logged_in_user():
    """Fetch current user from database before each request if session exists."""
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        conn = get_db_connection()
        g.user = conn.execute('SELECT id, name, email, created_at FROM users WHERE id = ?', (user_id,)).fetchone()
        conn.close()


@app.context_processor
def inject_user():
    """Make current_user accessible globally in all Jinja2 templates."""
    return dict(current_user=g.user if hasattr(g, 'user') else None)


# ---------------------------------------------------------------------------
# Public Pages
# ---------------------------------------------------------------------------
@app.route('/')
def home():
    """Render the Home page."""
    features = [
        {
            "icon": "⚡",
            "title": "Fast & Lightweight",
            "description": "Powered by Python Flask with minimal overhead, ensuring snappy response times and smooth navigation."
        },
        {
            "icon": "📝",
            "title": "Dynamic Blog & Posts",
            "description": "Read, write, and manage dynamic articles categorized with tag filtering directly from the database."
        },
        {
            "icon": "🔒",
            "title": "User Authentication",
            "description": "Built-in Signup, Login, Password Hashing (Werkzeug), and session protection for private routes."
        },
        {
            "icon": "🗄️",
            "title": "SQLite Database",
            "description": "Integrated SQLite database storing user accounts, articles, and contact inquiries reliably."
        }
    ]
    return render_template('index.html', title="Home", features=features)


@app.route('/about')
def about():
    """Render the About page."""
    team_values = [
        {
            "title": "Simplicity First",
            "text": "We believe software should be intuitive, transparent, and easy to maintain without unnecessary complexity."
        },
        {
            "title": "Security by Design",
            "text": "Industry-standard cryptographic password hashing and session guards protect user data from day one."
        },
        {
            "title": "Accessible to Everyone",
            "text": "Semantic markup, readable font sizing, and accessible interaction models for an inclusive web experience."
        }
    ]
    stats = [
        {"value": "SQLite", "label": "Zero-Config Database"},
        {"value": "PBKDF2", "label": "Secure Hash Security"},
        {"value": "100%", "label": "Responsive Design"},
        {"value": "Open Source", "label": "Community Friendly"}
    ]
    return render_template('about.html', title="About Us", team_values=team_values, stats=stats)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Render the Contact page and save submissions into SQLite database."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        # Input validation
        if not name or not email or not subject or not message:
            flash("Please fill in all required fields before submitting.", "error")
            return render_template(
                'contact.html',
                title="Contact Us",
                form_data={"name": name, "email": email, "subject": subject, "message": message}
            )

        if not EMAIL_REGEX.match(email):
            flash("Please provide a valid email address.", "error")
            return render_template(
                'contact.html',
                title="Contact Us",
                form_data={"name": name, "email": email, "subject": subject, "message": message}
            )

        # Store the message in SQLite database
        try:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO messages (name, email, subject, message) VALUES (?, ?, ?, ?)',
                (name, email, subject, message)
            )
            conn.commit()
            conn.close()
            flash(f"Thank you, {name}! Your message has been saved in the SQLite database. We will reply soon.", "success")
            return redirect(url_for('contact'))
        except Exception as e:
            flash(f"An error occurred while saving to database: {str(e)}", "error")
            return render_template(
                'contact.html',
                title="Contact Us",
                form_data={"name": name, "email": email, "subject": subject, "message": message}
            )

    return render_template('contact.html', title="Contact Us", form_data={})


# ---------------------------------------------------------------------------
# Blog & Articles Routes
# ---------------------------------------------------------------------------
@app.route('/blog')
def blog():
    """List all blog articles with optional category filtering."""
    category = request.args.get('category')
    conn = get_db_connection()
    if category:
        posts = conn.execute('SELECT * FROM posts WHERE category = ? ORDER BY id DESC', (category,)).fetchall()
    else:
        posts = conn.execute('SELECT * FROM posts ORDER BY id DESC').fetchall()
    
    categories = conn.execute('SELECT DISTINCT category FROM posts').fetchall()
    conn.close()
    return render_template('blog.html', title="Blog & Articles", posts=posts, categories=categories, current_category=category)


@app.route('/blog/<int:id>')
def blog_detail(id):
    """View a single blog article."""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    conn.close()
    if not post:
        return render_template('404.html', title="Article Not Found"), 404
    return render_template('blog_detail.html', title=post['title'], post=post)


@app.route('/blog/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new blog article (Protected)."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category = request.form.get('category', '').strip() or 'General'
        content = request.form.get('content', '').strip()

        if not title or not content:
            flash("Article title and content are required.", "error")
            return render_template('create_post.html', title="Write New Article", form_data={"title": title, "category": category, "content": content})

        conn = get_db_connection()
        conn.execute(
            'INSERT INTO posts (title, category, content, author_id, author_name) VALUES (?, ?, ?, ?, ?)',
            (title, category, content, session['user_id'], session['user_name'])
        )
        conn.commit()
        conn.close()

        flash("Your article has been successfully published to the blog!", "success")
        return redirect(url_for('blog'))

    return render_template('create_post.html', title="Write New Article", form_data={})


@app.route('/blog/<int:id>/delete', methods=['POST'])
@login_required
def delete_post(id):
    """Delete a blog article (Protected)."""
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (id,)).fetchone()
    if not post:
        conn.close()
        flash("Article not found.", "error")
        return redirect(url_for('blog'))

    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash("Article was deleted successfully.", "success")
    return redirect(url_for('blog'))


# ---------------------------------------------------------------------------
# Authentication Routes (Signup, Login, Logout, Dashboard)
# ---------------------------------------------------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """User registration handler with password hashing."""
    if g.user:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validations
        if not name or not email or not password or not confirm_password:
            flash("All fields are required.", "error")
            return render_template('signup.html', title="Create Account", form_data={"name": name, "email": email})

        if not EMAIL_REGEX.match(email):
            flash("Please enter a valid email address.", "error")
            return render_template('signup.html', title="Create Account", form_data={"name": name, "email": email})

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "error")
            return render_template('signup.html', title="Create Account", form_data={"name": name, "email": email})

        if password != confirm_password:
            flash("Passwords do not match. Please verify.", "error")
            return render_template('signup.html', title="Create Account", form_data={"name": name, "email": email})

        conn = get_db_connection()
        # Check if email is already taken
        existing_user = conn.execute('SELECT id FROM users WHERE email = ?', (email,)).fetchone()
        if existing_user:
            conn.close()
            flash("An account with this email address already exists. Please log in.", "error")
            return redirect(url_for('login'))

        # Securely hash password using Werkzeug
        password_hash = generate_password_hash(password)
        cursor = conn.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, password_hash)
        )
        conn.commit()
        new_user_id = cursor.lastrowid
        conn.close()

        # Automatically log user in upon registration
        session.clear()
        session['user_id'] = new_user_id
        session['user_name'] = name
        session['user_email'] = email

        flash(f"Welcome to FlaskCraft, {name}! Your account has been created successfully.", "success")
        return redirect(url_for('dashboard'))

    return render_template('signup.html', title="Create Account", form_data={})


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User authentication login handler."""
    if g.user:
        return redirect(url_for('dashboard'))

    next_page = request.args.get('next')

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash("Please enter both email and password.", "error")
            return render_template('login.html', title="Sign In", email=email)

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = user['name']
            session['user_email'] = user['email']

            flash(f"Welcome back, {user['name']}!", "success")
            return redirect(next_page or url_for('dashboard'))
        else:
            flash("Invalid email or password. Please try again.", "error")
            return render_template('login.html', title="Sign In", email=email)

    return render_template('login.html', title="Sign In", email="")


@app.route('/logout')
def logout():
    """Log out current user and clear session."""
    session.clear()
    flash("You have been successfully logged out.", "info")
    return redirect(url_for('home'))


@app.route('/dashboard')
@login_required
def dashboard():
    """User profile and system dashboard."""
    conn = get_db_connection()
    messages_count = conn.execute('SELECT COUNT(*) as count FROM messages').fetchone()['count']
    recent_messages = conn.execute('SELECT * FROM messages ORDER BY id DESC LIMIT 3').fetchall()
    total_users = conn.execute('SELECT COUNT(*) as count FROM users').fetchone()['count']
    total_posts = conn.execute('SELECT COUNT(*) as count FROM posts').fetchone()['count']
    my_posts = conn.execute('SELECT * FROM posts WHERE author_id = ? ORDER BY id DESC', (session['user_id'],)).fetchall()
    conn.close()

    return render_template(
        'dashboard.html',
        title="My Dashboard",
        messages_count=messages_count,
        recent_messages=recent_messages,
        total_users=total_users,
        total_posts=total_posts,
        my_posts=my_posts
    )


# ---------------------------------------------------------------------------
# Protected Messages Management
# ---------------------------------------------------------------------------
@app.route('/messages')
@login_required
def view_messages():
    """Display all contact form messages stored in SQLite database (Protected)."""
    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages ORDER BY id DESC').fetchall()
    conn.close()
    return render_template('messages.html', title="Messages Inbox", messages=messages)


@app.route('/messages/<int:id>/delete', methods=['POST'])
@login_required
def delete_message(id):
    """Delete a specific message from SQLite database by ID (Protected)."""
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM messages WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        flash(f"Message #{id} was successfully deleted from the SQLite database.", "success")
    except Exception as e:
        flash(f"Failed to delete message: {str(e)}", "error")
    return redirect(url_for('view_messages'))


# ---------------------------------------------------------------------------
# Error Handlers
# ---------------------------------------------------------------------------
@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page."""
    return render_template('404.html', title="Page Not Found"), 404


@app.errorhandler(500)
def internal_server_error(e):
    """Custom 500 error page."""
    return render_template('500.html', title="Server Error"), 500


if __name__ == '__main__':
    # Running in debug mode for local development
    app.run(host='127.0.0.1', port=5000, debug=True)
