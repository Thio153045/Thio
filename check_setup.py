import os
import sqlite3
import sys

def check_db():
    db = "data/competencies.db"
    if not os.path.exists(db):
        print("DB not found. Run setup_database.py to create it.")
        return
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [r[0] for r in cur.fetchall()]
    print("Tables:", tables)
    conn.close()

def check_packages():
    try:
        import reportlab
        print("reportlab OK")
    except Exception as e:
        print("reportlab MISSING:", e)
    try:
        import streamlit
        print("streamlit OK")
    except Exception as e:
        print("streamlit MISSING:", e)

if __name__ == "__main__":
    check_db()
    check_packages()
