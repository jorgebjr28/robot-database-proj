# Script 2: load_data.py
# ----------------------
# Populates the database created by create_schema.py using the CSV files.

import sqlite3
import csv
import os

DB_FILE = "robot.db"
CSV_DIR = "csv"
ROBOT_CSV    = os.path.join(CSV_DIR, "robot.csv")
INTERVAL_CSV = os.path.join(CSV_DIR, "interval.csv")
TRAJ_FILES   = [os.path.join(CSV_DIR, f) for f in ["t1.csv", "t2.csv", "t3.csv", "t4.csv", "t5.csv"]]

def load_robots(conn):
    with open(ROBOT_CSV, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            robot_id, name = row
            conn.execute(
                "INSERT INTO Robot(robot_id, name) VALUES (?, ?)",
                (int(robot_id), name)
            )
    conn.commit()
    print("Loaded robots.")

def load_intervals(conn):
    with open(INTERVAL_CSV, newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            start_sec, end_sec, evt = row
            conn.execute(
                "INSERT INTO TargetInterval(start_time_sec, end_time_sec, event_type) VALUES (?, ?, ?)",
                (int(start_sec), int(end_sec), evt)
            )
    conn.commit()
    print("Loaded target intervals.")

def load_trajectory(conn, traj_file, robot_id):
    with open(traj_file, newline="") as f:
        reader = csv.reader(f)
        for i, (x_str, y_str) in enumerate(reader, start=1):
            # Determine if this timestamp falls into any interval
            cursor = conn.execute("""
                SELECT interval_id 
                  FROM TargetInterval 
                 WHERE ? BETWEEN start_time_sec AND end_time_sec
            """, (i,))
            interval = cursor.fetchone()
            interval_id = interval[0] if interval else None

            conn.execute(
                "INSERT INTO SensorReading(robot_id, timestamp, x_cm, y_cm, interval_id) VALUES (?, ?, ?, ?, ?)",
                (robot_id, i, float(x_str), float(y_str), interval_id)
            )
    conn.commit()
    print(f"Loaded {traj_file} → Robot {robot_id}")

def main():
    if not os.path.exists(DB_FILE):
        raise SystemExit(f"Error: database file '{DB_FILE}' not found. Run create_schema.py first.")

    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")

    load_robots(conn)
    load_intervals(conn)

    for idx, fname in enumerate(TRAJ_FILES, start=1):
        if not os.path.exists(fname):
            raise SystemExit(f"Error: trajectory file '{fname}' not found.")
        load_trajectory(conn, fname, idx)

    conn.close()
    print("All data loaded successfully.")

if __name__ == "__main__":
    main()