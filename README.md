# Robot Sensor Database Project

This project implements a database for storing and analyzing robot sensor readings that occur during specific time intervals.

## Entity-Relationship Model

The ER diagram below represents the conceptual data model for the robot sensor database:

![ER Diagram](ROBOT_ER-DIAGRAM.png)

The model consists of three main entities:
- **Robot**: Represents individual robots with sensor capabilities
- **SensorReading**: Sensor data points collected by robots at specific timestamps
- **TargetInterval**: Time intervals of interest where specific events occur

The relationships show that:
- A Robot *has* many SensorReadings
- SensorReadings *occur in* TargetIntervals (when the timestamp falls within the interval's time range)

## Relational Schema
```
Robot(<u>robot_id</u>: INTEGER, name: TEXT)
TargetInterval(<u>interval_id</u>: INTEGER, start_time_sec: INTEGER, end_time_sec: INTEGER, event_type: TEXT)
SensorReading(<u>robot_id, timestamp</u>: INTEGER, x_cm: REAL, y_cm: REAL, interval_id: INTEGER)
```
## Building the Database

The database schema is implemented with the following tables:

```sql
-- 1. Robot entity
CREATE TABLE Robot (
  robot_id INTEGER PRIMARY KEY,
  name     TEXT    NOT NULL
);

-- 2. TargetInterval entity
CREATE TABLE TargetInterval (
  interval_id    INTEGER PRIMARY KEY AUTOINCREMENT,
  start_time_sec INTEGER NOT NULL,
  end_time_sec   INTEGER NOT NULL,
  event_type     TEXT    NOT NULL
);

-- 3. SensorReading entity (folds in both 1:N relationships)
CREATE TABLE SensorReading (
  robot_id    INTEGER NOT NULL,    -- FK for HasReading (every reading has a robot)
  timestamp   INTEGER NOT NULL,    -- seconds since start
  x_cm        REAL    NOT NULL,
  y_cm        REAL    NOT NULL,
  interval_id INTEGER,             -- FK for OccursDuring (nullable: readings outside intervals)
  PRIMARY KEY (robot_id, timestamp),
  FOREIGN KEY (robot_id)
    REFERENCES Robot(robot_id),
  FOREIGN KEY (interval_id)
    REFERENCES TargetInterval(interval_id)
);
```

## Running the Analysis

You have two options for setting up and running this project:

### Option 1: Local Setup with Python Scripts

This project includes two Python scripts to create and populate the SQLite database:

#### 1. Creating the Schema

Run the `create_schema.py` script to set up the database structure:

```bash
python create_schema.py
```

This script:
- Creates a new SQLite database file named `robot.db`
- Defines the tables according to the relational schema
- Enables foreign key constraints

#### 2. Loading Data

After creating the schema, run the `load_data.py` script to populate the database with data:

```bash
python load_data.py
```

This script:
- Loads robot definitions from `csv/robot.csv`
- Loads target intervals from `csv/interval.csv`
- Loads sensor readings from trajectory files (`csv/t1.csv` through `csv/t5.csv`)
- Associates each sensor reading with the appropriate robot and target interval

### Option 2: Using Google Colab with the Notebook File

For an interactive analysis experience, you can use the included Jupyter notebook (`Database_Project.ipynb`) in Google Colab:

1. Open [Google Colab](https://colab.research.google.com/)
2. Upload the `Database_Project.ipynb` notebook file
3. You have three different options for working with the data:
   - **Option A:** Upload the pre-created `robot.db` file directly (skip to Task 3)
   - **Option B:** Upload all CSV files and run the database creation cells in the notebook
   - **Option C:** Upload the Python scripts and CSV files, and run them in sequence

4. Follow the tasks in the notebook:
   - Task 3: Analyze metadata about robot positions
   - Task 4: Analyze robot trajectory information and proximity

The notebook contains all the necessary SQL queries for completing Tasks 3 and 4 of the project.

## Data Organization

The CSV files should be organized as follows:
- `csv/robot.csv`: Contains robot IDs and names
- `csv/interval.csv`: Contains interval definitions (start time, end time, event type)
- `csv/t1.csv` through `csv/t5.csv`: Contain trajectory data (x,y coordinates) for each robot

Make sure these files exist in the `csv` directory before running the data loading script.
