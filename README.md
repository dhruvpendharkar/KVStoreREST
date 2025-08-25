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

## Running the API

1. Start Flask Server:
   ```bash
   python app.py
   #The server runs by default at http://127.0.0.1:5000

## API Endpoints

1. Set a Key-Value Pair (POST /set):
   ```bash
   curl -X POST http://127.0.0.1:5000/set \
     -H "Content-Type: application/json" \
     -d '{"key": "name", "value": "Alice"}'
   ```
   Response (200):
   ```json
   {"status": "ok"}
   ```
   Error (404):
   ```json
   {"error": "Key and value are required"}
   ```
2. Get a key (GET /get):
   ```bash
   curl -X GET http://127.0.0.1:5000/get/name
   ```
   Response (200):
   ```json
   {"key": "name", "value": "Alice"}
   ```
   Error (404):
   ```json
   {"error": "Key not found"}
   ```
3. Delete a key (DELETE /delete):
   ```bash
   curl -X DELETE http://127.0.0.1:5000/delete/name
   ```
   Response (200):
   ```json
   {"status": "deleted"}
   ```
   Error (404):
   ```json
   {"error": "Key not found"}
   ```
4. Begin a transaction (POST /begin):
   ```bash
   curl -X POST http://127.0.0.1:5000/begin
   ```
   Response (200):
   ```json
   {"status": "transaction started"}
   ```
5. Rollback a transaction (POST /rollback):
   ```bash
   curl -X POST http://127.0.0.1:5000/rollback
   ```
   Response (200):
   ```json
   {"status": "transaction rolled back"}
   ```
   Error (400):
   ```json
   {"error": "No transaction to rollback"}
   ```
6. Commit a transaction (POST /commit):
   ```bash
   curl -X POST http://127.0.0.1:5000/commit
   ```
   Response (200):
   ```json
   {"status": "transaction committed"}
   ```
   Error (400):
   ```json
   {"error": "No transaction to commit"}
   ```

## Running Tests

For running the suite of tests use pytest. The included tests cover the KVStore API, the REST API layer built with Flask, and concurrency tests.



   
   

   





   
