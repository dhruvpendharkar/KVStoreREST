import pytest
import asyncio
from KVStore import KVStore

@pytest.mark.asyncio
async def test_concurrent_isolation():
    kv = KVStore()

    async def task1():
        await kv.begin()
        await kv.set("x", 1)
        val = await kv.get("x")
        assert val == 1
        # sleep to allow task2 to run
        await asyncio.sleep(0.1)
        await kv.commit()

    async def task2():
        await kv.begin()
        await kv.set("x", 2)
        val = await kv.get("x")
        assert val == 2
        await asyncio.sleep(0.1)
        await kv.rollback()

    await asyncio.gather(task1(), task2())

    # After both tasks, global store should reflect task1 commit only
    val = await kv.get("x")
    assert val == 1


@pytest.mark.asyncio
async def test_concurrent_nested_transactions():
    kv = KVStore()

    async def task1():
        await kv.begin()
        await kv.set("a", 5)
        await kv.begin()
        await kv.set("a", 10)
        await kv.commit()   # inner commit
        val = await kv.get("a")
        assert val == 10
        await kv.commit()   # outer commit

    async def task2():
        await kv.begin()
        await kv.set("a", 20)
        val = await kv.get("a")
        assert val == 20
        await kv.rollback()

    await asyncio.gather(task1(), task2())

    # Global store should reflect task1 only
    val = await kv.get("a")
    assert val == 10


@pytest.mark.asyncio
async def test_multiple_keys_concurrent():
    kv = KVStore()

    async def task1():
        await kv.begin()
        await kv.set("k1", 100)
        await kv.set("k2", 200)
        await asyncio.sleep(0.1)
        await kv.commit()

    async def task2():
        await kv.begin()
        await kv.set("k2", 999)
        await kv.set("k3", 300)
        await asyncio.sleep(0.1)
        await kv.commit()

    await asyncio.gather(task1(), task2())

    # After both commits, global store should have correct merged values
    val_k1 = await kv.get("k1")
    val_k2 = await kv.get("k2")  # last commit wins if keys overlap
    val_k3 = await kv.get("k3")
    assert val_k1 == 100
    assert val_k2 in (200, 999)  # could be either depending on task scheduling
    assert val_k3 == 300