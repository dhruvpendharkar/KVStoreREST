# Key-Value Store REST API

This is a Flask-based REST API for a key-value store with support for transactions. The API allows users to set, get, delete, and manage key-value pairs, as well as perform transactional operations like `begin`, `rollback`, and `commit`.

## Prerequisites

- Python 3.7+
- Flask (fl)
- Flask-SQLAlchemy
- pytest (tests only)
- pytest-asyncio (tests only)

## Installation

1. Clone the repository:
   ```bash
   git clone <https://github.com/dhruvpendharkar/KVStoreREST>
   cd KVStoreREST

2. Creeate and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate
3. Install dependencies:
  ```bash
   pip install -r requirements.txt
   #Note that some dependencies in requirements.txt are for tests



   
