# Magazine Article Management System

## Overview
This project models the relationships between Authors, Articles, and Magazines using SQLite and Python with raw SQL queries.

## Structure
- Author can write many Articles.
- Magazine can publish many Articles.
- Articles belong to one Author and one Magazine.

## Setup Instructions

### Step 1: Set up virtual environment (optional but recommended)
```bash
python -m venv env
source env/bin/activate  # For Windows: env\Scripts\activate
```

### Step 2: Install dependencies
```bash
pip install pytest
```

### Step 3: Set up the database
```bash
python scripts/setup_db.py
```

### Step 4: Explore or build on the system
Use `lib/debug.py` for interactive testing.

## File Structure
- `lib/models`: Author, Article, Magazine classes.
- `lib/db`: SQLite connection, schema, seed.
- `scripts`: Setup scripts.

