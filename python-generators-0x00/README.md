# Python Generators - Stream MySQL Data

## 📌 Project Overview

This project demonstrates how to use **Python generators** to stream rows from a **MySQL database** one by one in a memory-efficient way.

It includes a `seed.py` script that:
- Connects to a MySQL server
- Creates a database and table if they don’t exist
- Loads data from a CSV file into the table
- Streams data row-by-row using a Python generator

---

## 📚 Requirements

- Python 3.8+
- MySQL Server
- `mysql-connector-python` (install with `pip install mysql-connector-python`)
- A CSV file named `user_data.csv` in the same directory with the format:

```csv
name,email,age
John Doe,john@example.com,30
Jane Smith,jane@example.com,25
...
