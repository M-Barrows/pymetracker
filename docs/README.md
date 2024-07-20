# PymeTracker

![planned home screen](./imgs/PymeTracker%20-%20Main.png)

**Pymetracker** (rhymes with Time Tracker) is meant to be a light weight time tracker you can use from the terminal. While it's often easy to reach for products with a million integrations and a flashy UI, sometimes, all you need is to see how much time you've been working on a given project or see if there are any tasks that are consistently distracting you from your goal(s). 

## Running

`python3 pymetracker/main.py`

## Query Data Directly with SQLite

1. Install SQLite with `sudo apt install sqlite3`
2. Connect to the database `sqlite3 <path/to/database.db>`
3. Change output mode to "table" with `.mode table`
4. View all tasks `SELECT * FROM TASK;`

## Existing Features

This project is new. Let me cook! 

## Planned Features

* Local only (no logging or telemetry collected by PymeTracker)
* Create Tasks (Name, Client, and Project attribute)
* Start or Stop tasks with simple commands
* View high-level activity summaries
* Export your data to CSV files
