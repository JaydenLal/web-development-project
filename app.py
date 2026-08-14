from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('esports.db')
    conn.row_factory = sqlite3.Row # This lets us call columns by name
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    # SQL QUERY
    query = '''
        SELECT s.first_name, g.game, s.school, t.year, tm.score
        FROM tournament_matches tm
        JOIN student s ON tm.student_id = s.student_id
        JOIN game g ON tm.game_id = g.game_id
        JOIN tournament t ON tm.tournament_id = t.tournament_id
        ORDER BY tm.score DESC
    '''
    
    records = conn.execute(query).fetchall()
    conn.close()
    
    return render_template('index.html', records=records)

if __name__ == '__main__':
    app.run(debug=True)