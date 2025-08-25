from flask import request, jsonify
from app import app, db
from models import KeyValue
from KVStore import KVStore

kv_store = KVStore()

@app.route('/set', methods=['POST'])
async def set_value():
    data = request.get_json()
    key, value = data.get('key'), data.get('value')
    if not key or value is None:
        return jsonify({"error": "Key and value are required"}), 400
    await kv_store.set(key, value)
    new_kv = KeyValue(key=key, value=value)
    db.session.merge(new_kv)
    db.session.commit()
    return jsonify({"status": "ok"})

@app.route('/get/<key>', methods=['GET'])
async def get_value(key):
    value = await kv_store.get(key)
    if not value:
        return jsonify({"error": "Key not found"}), 404
    return jsonify({"key": key, "value": value})

@app.route('/delete/<key>', methods=['DELETE'])
async def delete_value(key):
    value = await kv_store.get(key)
    if not value:
        return jsonify({"error": "Key not found"}), 404
    await kv_store.delete(key)
    db.session.query(KeyValue).filter_by(key=key).delete()
    db.session.commit()
    return jsonify({"status": "deleted"})

@app.route('/begin', methods=['POST'])
async def begin():
    await kv_store.begin()
    return jsonify({"status": "transaction started"})

@app.route('/rollback', methods=['POST'])
async def rollback():
    try:
        await kv_store.rollback()
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"status": "transaction rolled back"})

@app.route('/commit', methods=['POST'])
async def commit():
    try:
        await kv_store.commit()
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"status": "transaction committed"})