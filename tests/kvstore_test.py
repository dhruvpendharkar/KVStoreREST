from KVStore import KVStore
import pytest

@pytest.mark.asyncio
async def test_set_and_get():
    kv = KVStore()
    await kv.set("key1", "value1")
    val = await kv.get("key1") 
    assert val == "value1"

@pytest.mark.asyncio
async def test_delete_key():
    store = KVStore()
    await store.set("a", 1)
    await store.delete("a")
    val = await store.get("a")
    assert val is None

@pytest.mark.asyncio
async def test_begin_and_rollback():
    store = KVStore()
    await store.set("a", 1)

    await store.begin()
    await store.set("a", 2)
    val1 = await store.get("a")
    assert val1 == 2

    await store.rollback()
    val2 = await store.get("a")
    assert val2 == 1

@pytest.mark.asyncio
async def test_begin_and_commit():
    store = KVStore()
    await store.set("a", 1)

    await store.begin()
    await store.set("a", 2)
    await store.commit()
    val = await store.get("a")
    assert val == 2

@pytest.mark.asyncio
async def test_nested_transactions_rollback():
    store = KVStore()
    await store.set("a", 5)

    await store.begin()          
    await store.set("a", 10)
    await store.begin()          
    await store.set("a", 20)
    await store.rollback()  
    val1 = await store.get("a")     
    assert val1 == 10

    await store.rollback()  
    val2 = await store.get("a")     
    assert val2 == 5

@pytest.mark.asyncio
async def test_nested_transactions_commit_then_rollback():
    store = KVStore()
    await store.set("a", 5)

    await store.begin()         
    await store.set("a", 10)
    await store.begin()          
    await store.set("a", 20)
    await store.commit()   
    val1 = await store.get("a")     
    assert val1 == 20

    await store.rollback()
    val2 = await store.get("a")
    assert val2 == 5

@pytest.mark.asyncio
async def test_rollback_without_transaction():
    store = KVStore()
    with pytest.raises(RuntimeError):
        await store.rollback()

@pytest.mark.asyncio
async def test_commit_without_transaction():
    store = KVStore()
    with pytest.raises(RuntimeError):
        await store.commit()
