import streamlit as st
import sqlite3
import tempfile, os
from analyzer import analyze_job_description
from pdf_detector import export_analysis_to_pdf
from export_database import export_database_to_pdf

DB_PATH = "data/competencies.db"

st.set_page_config(page_title="Job Analyzer", layout="wide")
st.title("🔍 Job Analyzer (Web)")

# Helper DB functions
def get_connection():
    return sqlite3.connect(DB_PATH)

def get_competencies(kind="technical"):
    conn = get_connection()
    cur = conn.cursor()
    if kind == "technical":
        cur.execute("SELECT id, name, definition, keywords FROM technical_competencies ORDER BY id")
    else:
        cur.execute("SELECT id, name, definition, keywords FROM soft_competencies ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows

def add_competency(kind, name, definition, keywords):
    conn = get_connection(); cur = conn.cursor()
    if kind == "technical":
        cur.execute("INSERT INTO technical_competencies (name, definition, keywords) VALUES (?, ?, ?)", (name, definition, keywords))
    else:
        cur.execute("INSERT INTO soft_competencies (name, definition, keywords) VALUES (?, ?, ?)", (name, definition, keywords))
    conn.commit(); conn.close()

def update_competency(kind, cid, name, definition, keywords):
    conn = get_connection(); cur = conn.cursor()
    if kind == "technical":
        cur.execute("UPDATE technical_competencies SET name=?, definition=?, keywords=? WHERE id=?", (name, definition, keywords, cid))
    else:
        cur.execute("UPDATE soft_competencies SET name=?, definition=?, keywords=? WHERE id=?", (name, definition, keywords, cid))
    conn.commit(); conn.close()

def delete_competency(kind, cid):
    conn = get_connection(); cur = conn.cursor()
    if kind == "technical":
        cur.execute("DELETE FROM technical_competencies WHERE id=?", (cid,))
    else:
        cur.execute("DELETE FROM soft_competencies WHERE id=?", (cid,))
    conn.commit(); conn.close()

# job_background functions
def get_job_backgrounds():
    conn = get_connection(); cur = conn.cursor()
    cur.execute("SELECT id, job_level, education, age_min, age_max, exp_min, exp_max FROM job_background ORDER BY id")
    rows = cur.fetchall(); conn.close(); return rows

def add_job_background(job_level, education, age_min, age_max, exp_min, exp_max):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("INSERT INTO job_background (job_level, education, age_min, age_max, exp_min, exp_max) VALUES (?, ?, ?, ?, ?, ?)", 
                (job_level, education, age_min, age_max, exp_min, exp_max))
    conn.commit(); conn.close()

def update_job_background(cid, job_level, education, age_min, age_max, exp_min, exp_max):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("UPDATE job_background SET job_level=?, education=?, age_min=?, age_max=?, exp_min=?, exp_max=? WHERE id=?", 
                (job_level, education, age_min, age_max, exp_min, exp_max, cid))
    conn.commit(); conn.close()

def delete_job_background(cid):
    conn = get_connection(); cur = conn.cursor()
    cur.execute("DELETE FROM job_background WHERE id=?", (cid,))
    conn.commit(); conn.close()

# Sidebar menu
menu = st.sidebar.selectbox("Menu", ["Analyze", "Edit Kompetensi", "Edit Persyaratan Jabatan", "Export Database"])

if menu == "Analyze":
    st.header("Analisis Jabatan")
    col1, col2 = st.columns([2,1])
    with col1:
        title = st.text_input("Nama Jabatan")
        desc = st.text_area("Uraian Jabatan", height=300)
    with col2:
        st.write("Petunjuk: Masukkan uraian pekerjaan lengkap sehingga sistem bisa mencocokkan keywords.")
        if st.button("Analisa"):
            if not title or not desc:
                st.warning("Isi nama jabatan dan uraian sebelum menganalisa.")
            else:
                res = analyze_job_description(title, desc)
                st.subheader("Hasil Analisis")
                st.markdown(f"**Nama Jabatan:** {res.get('job_title')}")
                st.markdown(f"**Level Jabatan:** {res.get('job_level')}")
                st.markdown(f"**Pendidikan:** {res.get('education')}")
                st.markdown(f"**Usia:** {res.get('age_range')}")
                st.markdown(f"**Pengalaman:** {res.get('experience_range')}")
                st.markdown("**Standar Kompetensi:**")
                st.markdown("**Key Performace Indicators:**")
                for c in res.get("competencies", []):
                    st.markdown(f"- **{c.get('name')}** — {c.get('definition')}")
                # Create temp PDF and offer download
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
                tmp.close()
                export_analysis_to_pdf(tmp.name, res.get('job_title'), desc, res.get('education'), res.get('age_range'), res.get('experience_range'), res.get('job_level'), res.get('competencies'))
                with open(tmp.name, "rb") as f:
                    st.download_button("⬇ Download Hasil Analisis (PDF)", f.read(), file_name=f"{title.replace(' ','_')}_analysis.pdf", mime="application/pdf")
                try:
                    os.unlink(tmp.name)
                except:
                    pass

elif menu == "Edit Kompetensi":
    st.header("Edit Kompetensi (Technical / Soft)")
    kind = st.radio("Pilih jenis kompetensi", ("technical","soft"), horizontal=True)
    st.write("Daftar kompetensi:")
    rows = get_competencies(kind)
    for r in rows:
        cid, name, definition, keywords = r
        with st.expander(f"{cid}. {name}"):
            new_name = st.text_input("Nama", value=name, key=f"name_{kind}_{cid}")
            new_def = st.text_area("Definisi", value=definition, key=f"def_{kind}_{cid}", height=80)
            new_kw = st.text_input("Keywords (pisah koma)", value=keywords, key=f"kw_{kind}_{cid}")
            colx, coly = st.columns(2)
            if colx.button("Simpan Perubahan", key=f"save_{kind}_{cid}"):
                update_competency(kind, cid, new_name, new_def, new_kw)
                st.success("Tersimpan. Silakan refresh (F5) untuk melihat perubahan.")
            if coly.button("Hapus Kompetensi", key=f"del_{kind}_{cid}"):
                delete_competency(kind, cid)
                st.success("Terhapus. Silakan refresh (F5).")

    st.markdown("---")
    st.subheader("Tambah Kompetensi Baru")
    with st.form("add_comp_form"):
        add_name = st.text_input("Nama kompetensi")
        add_def = st.text_area("Definisi", height=100)
        add_kw = st.text_input("Keywords (pisahkan koma)")
        submitted = st.form_submit_button("Tambah Kompetensi")
        if submitted:
            if not add_name or not add_def or not add_kw:
                st.warning("Lengkapi semua field.")
            else:
                add_competency(kind, add_name, add_def, add_kw)
                st.success("Kompetensi baru ditambahkan. Tekan F5 untuk refresh.")

elif menu == "Edit Persyaratan Jabatan":
    st.header("Edit Persyaratan Jabatan (Job Background per Level)")
    rows = get_job_backgrounds()
    for r in rows:
        cid, job_level, education, age_min, age_max, exp_min, exp_max = r
        with st.expander(f"{cid}. {job_level}"):
            jl = st.text_input("Level Jabatan", value=job_level, key=f"jl_{cid}")
            edu = st.text_input("Pendidikan (contoh: S1 / S2)", value=education, key=f"edu_{cid}")
            amin = st.number_input("Usia minimal", value=age_min, key=f"amin_{cid}")
            amax = st.number_input("Usia maksimal", value=age_max, key=f"amax_{cid}")
            emin = st.number_input("Pengalaman minimal (tahun)", value=exp_min, key=f"emin_{cid}")
            emax = st.number_input("Pengalaman maksimal (tahun)", value=exp_max, key=f"emax_{cid}")
            col1, col2 = st.columns(2)
            if col1.button("Simpan Perubahan", key=f"save_bg_{cid}"):
                update_job_background(cid, jl, edu, amin, amax, emin, emax)
                st.success("Tersimpan. Tekan F5 untuk refresh.")
            if col2.button("Hapus Level", key=f"del_bg_{cid}"):
                delete_job_background(cid)
                st.success("Dihapus. Tekan F5 untuk refresh.")

    st.markdown("---")
    st.subheader("Tambah Level Jabatan Baru")
    with st.form("add_bg_form"):
        new_level = st.text_input("Level Jabatan (contoh: Entry Level)")
        new_edu = st.text_input("Pendidikan (contoh: S1)")
        new_amin = st.number_input("Usia minimal", min_value=16, max_value=100, value=22)
        new_amax = st.number_input("Usia maksimal", min_value=16, max_value=100, value=30)
        new_emin = st.number_input("Pengalaman minimal", min_value=0, max_value=50, value=0)
        new_emax = st.number_input("Pengalaman maksimal", min_value=0, max_value=50, value=5)
        submitted2 = st.form_submit_button("Tambah Level Jabatan")
        if submitted2:
            if not new_level or not new_edu:
                st.warning("Lengkapi field Level dan Pendidikan.")
            else:
                add_job_background(new_level, new_edu, new_amin, new_amax, new_emin, new_emax)
                st.success("Level jabatan ditambahkan. Tekan F5 untuk refresh.")

elif menu == "Export Database":
    st.header("Export Database Kompetensi ke PDF")
    kind = st.selectbox("Pilih jenis", ("technical","soft"))
    if st.button("Export dan Download PDF"):
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp.close()
        export_database_to_pdf(tmp.name, kind)
        with open(tmp.name, "rb") as f:
            st.download_button("⬇ Download PDF Database", f.read(), file_name=f"competencies_{kind}.pdf", mime="application/pdf")
        try:
            os.unlink(tmp.name)
        except:
            pass
