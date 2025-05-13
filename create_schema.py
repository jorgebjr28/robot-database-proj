# Script 1: create_schema.py
# --------------------------
# Creates the SQLite database and tables according to the final schema.

import sqlite3
import os

DB_FILE = "robot.db"

# Remove existing database if present for a clean setup
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Enable foreign key enforcement
cursor.execute("PRAGMA foreign_keys = ON;")

# Create Robot table
cursor.execute("""
CREATE TABLE Robot (
  robot_id INTEGER PRIMARY KEY,
  name     TEXT    NOT NULL
);
""")

# Create TargetInterval table
cursor.execute("""
CREATE TABLE TargetInterval (
  interval_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  start_time_sec INTEGER NOT NULL,
  end_time_sec   INTEGER NOT NULL,
  event_type     TEXT    NOT NULL
);
""")

# Create SensorReading table, folding in both 1:N relationships:
#   • robot_id   FK → Robot        (HasReading)
#   • interval_id FK → TargetInterval (OccursDuring, nullable)
cursor.execute("""
CREATE TABLE SensorReading (
  robot_id    INTEGER NOT NULL,
  timestamp   INTEGER NOT NULL,
  x_cm        REAL    NOT NULL,
  y_cm        REAL    NOT NULL,
  interval_id INTEGER,
  PRIMARY KEY (robot_id, timestamp),
  FOREIGN KEY (robot_id)
    REFERENCES Robot(robot_id),
  FOREIGN KEY (interval_id)
    REFERENCES TargetInterval(interval_id)
);
""")

conn.commit()
conn.close()

print("Schema created successfully in 'robot.db'.")