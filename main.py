import asyncpg
from fastapi import FastAPI
import uvicorn
from datetime import datetime

app = FastAPI()
pool = None

async def connect_to_db():
    global pool
    pool = await asyncpg.create_pool(
        min_size=1,
        max_size=16,
        database="Buff_Steam",
        user="postgres",
        password="benfica10",
        host="localhost"
    )

async def close_db_connection():
    if pool:
        await pool.close()

@app.on_event("startup")
async def startup_event():
    await connect_to_db()

@app.on_event("shutdown")
async def shutdown_event():
    await close_db_connection()

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/exchange_rates")
async def read_exchange_rates():
    async with pool.acquire() as conn:
        result = await conn.fetch("SELECT * FROM exchangerates WHERE id = 1")
    return result

@app.post("/exchange_rates")
async def update_exchange_rates(rates, updatedAt):
    async with pool.acquire() as conn:
        updatedAt = datetime.fromisoformat(updatedAt)
        async with conn.transaction():
            await conn.execute("DELETE FROM exchangerates WHERE id = 1")
            await conn.execute("INSERT INTO exchangerates (id,rates, updatedat) VALUES ($1, $2, $3)", 1, rates, updatedAt)
    return {"rates": rates, "updatedAt": updatedAt}

@app.post("/buff2steam")
async def insert_buff2steam(id, name, buff_min_price, steam_price_cny, steam_price_eur, b_o_ratio, steamUrl, buffUrl, updatedAt):
    async with pool.acquire() as conn:
        id = int(id)
        buff_min_price = float(buff_min_price)
        steam_price_cny = float(steam_price_cny)
        steam_price_eur = float(steam_price_eur)
        b_o_ratio = float(b_o_ratio)
        updatedAt = datetime.fromisoformat(updatedAt)
        async with conn.transaction():
            await conn.execute(
                "INSERT INTO buff2steam (id, name, buff_min_price, steam_price_cny, steam_price_eur, b_o_ratio, steamUrl, buffUrl, updatedat) "
                "VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9) ",
                id, name, buff_min_price, steam_price_cny, steam_price_eur, b_o_ratio, steamUrl, buffUrl, updatedAt
            )
    return {"response": True}

@app.post("/steam2buff")
async def insert_buff2steam(id, price, currency, link, float_value, updatedAt):
    async with pool.acquire() as conn:
        id = int(id)
        price = float(price)
        float_value = float(float_value)
        updatedAt = datetime.fromisoformat(updatedAt)
        async with conn.transaction():
            await conn.execute(
                "INSERT INTO steam2buff (id, price, currency, link, float_value, updatedat) "
                "VALUES ($1, $2, $3, $4, $5, $6) ",
                id, price, currency, link, float_value, updatedAt
            )
    return {"response": True}

@app.get("/steam2buff")
async def read_steam2buff():
    async with pool.acquire() as conn:
        result = await conn.fetch("SELECT * FROM steam2buff ORDER BY uuid DESC")
    return result

@app.get("/buff2steam")
async def read_buff2steam():
    async with pool.acquire() as conn:
        result = await conn.fetch("SELECT * FROM buff2steam ORDER BY uuid DESC")
    return result

@app.get("/item_nameid")
async def read_item_nameid(market_hash_name):
    async with pool.acquire() as conn:
        result = await conn.fetch("SELECT * FROM steamskins WHERE market_hash_name = $1", market_hash_name)
    return result

@app.post("/item_nameid")
async def insert_item_nameid(item_nameid, market_hash_name):
    async with pool.acquire() as conn:
        item_nameid = int(item_nameid)
        async with conn.transaction():
            await conn.execute(
                "INSERT INTO steamskins (item_nameid, market_hash_name) "
                "VALUES ($1, $2) ",
                item_nameid, market_hash_name
            )
    return {"response": True}

@app.post("/purchase/rr")
async def insert_purchase_rr(market_hash, store, purchase_price, purchase_date, float_value):
    async with pool.acquire() as conn:
        purchase_price = float(purchase_price)
        float_value = float(float_value)
        purchase_date = datetime.fromisoformat(purchase_date)
        async with conn.transaction():
            await conn.execute(
                "INSERT INTO rr (market_hash, store, purchase_price, purchase_date, float_value) "
                "VALUES ($1, $2, $3, $4, $5) ",
                market_hash, store, purchase_price, purchase_date, float_value
            )
    return {"response": True}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
