from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(Flutter)

def init_db():
    # Initialize the database and create table if not exists
    with sqlite3.connect('aliases.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS aliases (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          alias TEXT NOT NULL,
                          description TEXT NOT NULL
                          )''')
        conn.commit()

@app.route('/')
def index():
    # Fetch all aliases from the database
    with sqlite3.connect('aliases.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM aliases')
        aliases = cursor.fetchall()
    return render_template('index.html', aliases=aliases)

@app.route('/add', methods=['POST'])
def add_alias():
    # Add a new alias to the database
    alias = request.form['alias']
    description = request.form['description']
    with sqlite3.connect('aliases.db') as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT INTO aliases (alias, description) VALUES (?, ?)', (alias, description))
        conn.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:alias_id>')
def delete_alias(alias_id):
    # Delete an alias from the database
    with sqlite3.connect('aliases.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM aliases WHERE id = ?', (alias_id,))
        conn.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
