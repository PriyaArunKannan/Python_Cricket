# 🏏 Cricket Data Analysis & Visualization

This project performs **Exploratory Data Analysis (EDA)**, **SQL-based insights**, and **interactive dashboards** on cricket match data (Cricsheet dataset).
It integrates **Python, SQLite, Pandas, Matplotlib, Seaborn, Plotly, and Power BI**.

---

## 📂 Project Structure

```
cricsheet_analysis/
│── data/                      # Folder for downloaded JSON files
│── eda/                       # Folder for Python EDA notebooks/plots
│── db/                        # Folder for SQL database
│── scripts/                   # All Python scripts
│   ├── scraper.py             # Selenium script for scraping
│   ├── transform.py           # JSON → DataFrame transformation
│   ├── database.py            # SQL table creation + insertion
│   ├── queries.py             # 20 SQL queries
│   ├── eda.py                 # Python EDA visualizations
│── requirements.txt           # Dependencies
│── README.md                  # Documentation
```

---

## ⚙️ Setup

### 1️⃣ Create virtual environment

```bash
python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

**Mac/Linux**

```bash
source venv/bin/activate
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Next Steps to Run

1. **Run scraper.py** → Downloads JSON data (Cricsheet matches).

   ```bash
   python scripts/scraper.py
   ```

2. **Run transform.py** → Parses JSON → Pandas DataFrame.

   ```bash
   python scripts/transform.py
   ```

3. **Run database.py** → Stores data into SQLite DB (`db/cricket.db`).

   ```bash
   python scripts/database.py
   ```

4. **Run queries.py** → Executes 20 SQL queries for insights.

   ```bash
   python scripts/queries.py
   ```

5. **Run eda.py** → Generates Python plots (Matplotlib, Seaborn, Plotly).

   ```bash
   python scripts/eda.py
   ```

6. **Connect SQLite DB to Power BI** → Build interactive dashboards.

---

## 📊 Features

✔️ Automated **data scraping (Selenium)**
✔️ **JSON → SQL pipeline** (transform + store + query)
✔️ **20 SQL analytical queries** for insights
✔️ **EDA with Python visualizations**
✔️ Power BI **dashboards** from SQL DB

---

