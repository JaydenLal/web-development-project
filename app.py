from flask import Flask, render_template, request
import sqlite3

# Create the Flask app, This is the main web application
app = Flask(__name__)

# Connect to the SQLite database and return the connection.
# We set row_factory so we can access columns by name like row['game']
def get_db_connection():
    conn = sqlite3.connect('esports.db')
    conn.row_factory = sqlite3.Row
    return conn

# This connects the database and loads the database to display on index.html
@app.route('/')
def index():
    conn = get_db_connection()
    # Read the simple search query from the URL, e.g. /?q=Ruby
    q = request.args.get('q', '').strip()

    # (Default Query) SQL query: get player names, game, school, year, and score
    # from the related tables, sorted from highest score to lowest
    query = '''
        SELECT s.first_name, g.game, s.school, t.year, tm.score
        FROM tournament_matches tm
        JOIN student s ON tm.student_id = s.student_id
        JOIN game g ON tm.game_id = g.game_id
        JOIN tournament t ON tm.tournament_id = t.tournament_id
    '''

    params = ()
    if q:
        # If the user provided a search term, filter by first_name (case-insensitive)
        query += " WHERE LOWER(s.first_name) LIKE ?"
        params = (f"%{q.lower()}%",)

    # Always sort highest to lowest on this page
    query += " ORDER BY tm.score DESC"

    records = conn.execute(query, params).fetchall()
    conn.close()
    # Send the data and the current query back to the template so the
    # input keeps its value after submitting the form.
    return render_template('index.html', records=records, q=q)

# This connects the database and loads the database to display on index2.html
@app.route('/index2')
def index2():
    conn = get_db_connection()
    # Read the search query from the URL, e.g. /index2?q=Ruby
    q = request.args.get('q', '').strip()

    # SQL query: get player names, game, school, year, and score
    # from the related tables, sorted from lowest score to highest
    query = '''
        SELECT s.first_name, g.game, s.school, t.year, tm.score
        FROM tournament_matches tm
        JOIN student s ON tm.student_id = s.student_id
        JOIN game g ON tm.game_id = g.game_id
        JOIN tournament t ON tm.tournament_id = t.tournament_id
    '''

    params = ()
    if q:
        query += " WHERE LOWER(s.first_name) LIKE ?"
        params = (f"%{q.lower()}%",)

    # Sort lowest to highest on this page
    query += " ORDER BY tm.score ASC"

    records = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('index2.html', records=records, q=q)


# This connects the database and loads the database to display on index3.html
@app.route('/index3')
def index3():
    conn = get_db_connection()
    # Read the search query from the URL, e.g. /index3?q=Ruby
    q = request.args.get('q', '').strip()

    # SQL query: list tournaments and their matches, sorted chronologically
    # Join student and game so the search can match names, city, year, ids, and scores
    query = '''
        SELECT t.year,
               t.city,
               g.game AS game_name,
               s.first_name,
               s.last_name,
               tm.game_id,
               tm.student_id,
               tm.score
        FROM tournament_matches tm
        JOIN tournament t ON tm.tournament_id = t.tournament_id
        JOIN student s ON tm.student_id = s.student_id
        JOIN game g ON tm.game_id = g.game_id
    '''

    params = ()
    if q:
        # match the search term against multiple text and numeric columns
        q_like = f"%{q.lower()}%"
        query += (
            " WHERE LOWER(s.first_name) LIKE ?"
            " OR LOWER(s.last_name) LIKE ?"
            " OR LOWER(t.city) LIKE ?"
            " OR LOWER(g.game) LIKE ?"
            " OR CAST(tm.game_id AS TEXT) LIKE ?"
            " OR CAST(tm.student_id AS TEXT) LIKE ?"
            " OR CAST(tm.score AS TEXT) LIKE ?"
            " OR CAST(t.year AS TEXT) LIKE ?"
        )
        params = (q_like, q_like, q_like, q_like, q_like, q_like, q_like, q_like)

    query += " ORDER BY t.year ASC, t.city ASC"

    records = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('index3.html', records=records, q=q)

# About page
@app.route('/about')
def about():
    return render_template('about.html')

# If someone visits a page that does not exist, show the 404 page
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# Run the app when this file is run
if __name__ == '__main__':
    app.run(debug=True)