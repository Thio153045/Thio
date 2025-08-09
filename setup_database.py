import sqlite3
import os

DB_DIR = "data"
DB_PATH = os.path.join(DB_DIR, "competencies.db")

if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# Drop tables if exist (safe for re-run)
cur.execute("DROP TABLE IF EXISTS technical_competencies")
cur.execute("DROP TABLE IF EXISTS soft_competencies")
cur.execute("DROP TABLE IF EXISTS job_background")

cur.execute("""
CREATE TABLE technical_competencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    definition TEXT NOT NULL,
    keywords TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE soft_competencies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    definition TEXT NOT NULL,
    keywords TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE job_background (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_level TEXT NOT NULL,
    education TEXT NOT NULL,
    age_min INTEGER NOT NULL,
    age_max INTEGER NOT NULL,
    exp_min INTEGER NOT NULL,
    exp_max INTEGER NOT NULL
)
""")

technical = [
    ("Analisa Data Keuangan", "Menganalisa laporan keuangan", "laporan,analisa,keuangan,neraca,laba rugi"),
    ("Pengelolaan SDM", "Mengelola rekrutmen, pelatihan dan kinerja SDM", "hrd,karyawan,pelatihan,rekrutmen,performance"),
    ("Penguasaan Pajak", "Mengetahui aturan perpajakan dan pelaporan", "pajak,pph,ppn,pelaporan,npwp"),
    ("Perencanaan Produksi", "Menyusun jadwal dan strategi produksi", "produksi,perencanaan,jadwal,pabrik"),
    ("Strategi Penjualan", "Menyusun strategi dan target penjualan", "sales,penjualan,target,prospek")
]

soft = [
    ("Komunikasi Efektif", "Menyampaikan ide secara jelas", "komunikasi,menyampaikan,negosiasi"),
    ("Integritas", "Berperilaku jujur dan dapat dipercaya", "jujur,etika,nilai,konsisten"),
    ("Kepemimpinan", "Mengarahkan dan memotivasi tim", "memimpin,arahan,motivasi,tim,leader"),
    ("Kerjasama Tim", "Bekerja secara kolaboratif", "tim,kerjasama,kolaborasi"),
    ("Problem Solving", "Menganalisa masalah dan menemukan solusi", "solusi,masalah,analisa,root cause")
]

job_bg = [
    ("Entry Level", "D3 / S1", 22, 26, 0, 2),
    ("Staff Senior", "S1", 26, 30, 3, 5),
    ("Supervisor", "S1 / S2", 28, 35, 5, 8),
    ("Manager", "S2 (diutamakan)", 30, 40, 8, 15)
]

cur.executemany("INSERT INTO technical_competencies (name, definition, keywords) VALUES (?, ?, ?)", technical)
cur.executemany("INSERT INTO soft_competencies (name, definition, keywords) VALUES (?, ?, ?)", soft)
cur.executemany("INSERT INTO job_background (job_level, education, age_min, age_max, exp_min, exp_max) VALUES (?, ?, ?, ?, ?, ?)", job_bg)

conn.commit()
conn.close()

print("Database created at:", DB_PATH)
