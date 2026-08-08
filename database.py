import sqlite3
from datetime import datetime

DB_NAME = "scans.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            filename TEXT,
            total INTEGER,
            safe INTEGER,
            malicious INTEGER,
            dos INTEGER,
            probe INTEGER,
            r2l INTEGER,
            u2r INTEGER
        )
    """)
    conn.commit()
    conn.close()

def save_scan(filename, total, safe, malicious, attack_counts):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO scans (timestamp, filename, total, safe, malicious, dos, probe, r2l, u2r)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        filename,
        total, safe, malicious,
        attack_counts.get("DoS", 0),
        attack_counts.get("Probe", 0),
        attack_counts.get("R2L", 0),
        attack_counts.get("U2R", 0)
    ))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT COUNT(*), SUM(total), SUM(safe), SUM(malicious), SUM(dos), SUM(probe), SUM(r2l), SUM(u2r) FROM scans")
    row = c.fetchone()
    conn.close()

    scans_count = row[0] or 0
    total_packets = row[1] or 0
    safe = row[2] or 0
    malicious = row[3] or 0
    dos = row[4] or 0
    probe = row[5] or 0
    r2l = row[6] or 0
    u2r = row[7] or 0

    safe_pct = round((safe / total_packets) * 100, 1) if total_packets else 0
    malicious_pct = round((malicious / total_packets) * 100, 1) if total_packets else 0

    return {
        "scans_count": scans_count,
        "total_packets": total_packets,
        "safe": safe,
        "malicious": malicious,
        "safe_pct": safe_pct,
        "malicious_pct": malicious_pct,
        "dos": dos,
        "probe": probe,
        "r2l": r2l,
        "u2r": u2r
    }

def get_recent_scans(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT timestamp, total, safe, malicious FROM scans ORDER BY id DESC LIMIT ?", (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_all_scans():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT timestamp, filename, total, safe, malicious FROM scans ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows