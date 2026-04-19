from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host="postgres",
        database="weather_db",
        user="admin",
        password="adminpass"
    )

@app.route('/')
def index():
    return "<h1>✅ Погода в Волгограде</h1><p><a href='/data'>Посмотреть данные</a></p>"

@app.route('/data')
def data():
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM weather_data ORDER BY timestamp DESC LIMIT 5")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify(rows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
