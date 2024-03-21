from fastapi import FastAPI
import psycopg2
from psycopg2 import pool
import uvicorn

db_pool = None
app = FastAPI()
steam2buff = {}
buff2steam = {}

def create_db_pool():
    global db_pool
    db_pool = pool.SimpleConnectionPool(
        minconn=1,
        maxconn=128,
        dbname="buff2steam",
        user="postgres",
        password="benfica10",
        host="localhost",
    )

@app.on_event("startup")
async def startup_event():
    create_db_pool()

@app.on_event("shutdown")
async def shutdown_event():
    if db_pool:
        db_pool.closeall()
        
@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.get("/exchange_rates")
async def read_exchange_rates():
    conn = db_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exchangerates WHERE id = 1")
    result = cursor.fetchall()
    cursor.close()
    db_pool.putconn(conn)
    return result

@app.post("/exchange_rates")
async def update_exchange_rates(rates, updatedAt):
    conn = db_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM exchangerates WHERE id = 1")
    conn.commit()
    cursor.execute("INSERT INTO exchangerates (id,rates, updatedat) VALUES (%s, %s, %s)", (1, rates, updatedAt))
    conn.commit()
    cursor.close()
    db_pool.putconn(conn)
    return {"rates": rates, "updatedAt": updatedAt}

@app.post("/buff2steam")
async def insert_buff2steam(id, name, buff_min_price, steam_price_cny, steam_price_eur, b_o_ratio, steamUrl, buffUrl, updatedAt):
    global buff2steam
    conn = db_pool.getconn()
    cursor = conn.cursor()

    # Use a single query to insert the record if it doesn't exist
    cursor.execute(
        "INSERT INTO buff2steam (id, name, buff_min_price, steam_price_cny, steam_price_eur, b_o_ratio, steamUrl, buffUrl, updatedat) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
        "ON CONFLICT (id) DO NOTHING",
        (id, name, buff_min_price, steam_price_cny, steam_price_eur, b_o_ratio, steamUrl, buffUrl, updatedAt)
    )
    if cursor.rowcount > 0:
        buff2steam = {"id": id, "name": name, "buff_min_price": buff_min_price, "steam_price_cny": steam_price_cny, "steam_price_eur": steam_price_eur, "b_o_ratio": b_o_ratio, "steamUrl": steamUrl, "buffUrl": buffUrl, "updatedat": updatedAt}
        conn.commit()
        cursor.close()
        db_pool.putconn(conn)
        return {"response": True}
    else:
        # If no rows were affected, rollback the transaction
        conn.rollback()
        cursor.close()
        db_pool.putconn(conn)
        return {"response": False}

@app.post("/steam2buff")
async def insert_buff2steam(id, asset_id, price, currency, link, float_value, updatedAt):
    global steam2buff
    conn = db_pool.getconn()
    cursor = conn.cursor()

    # Use a single query to insert the record if it doesn't exist
    cursor.execute(
        "INSERT INTO steam2buff (id, asset_id, price, currency, link, float_value, updatedat) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s) "
        "ON CONFLICT (id) DO NOTHING",
        (id, asset_id, price, currency, link, float_value, updatedAt)
    )
    
    if cursor.rowcount > 0:
        steam2buff = {"id": id, "asset_id": asset_id, "price": price, "currency": currency, "link": link, "float_value": float_value, "updatedat": updatedAt}
        conn.commit()
        cursor.close()
        db_pool.putconn(conn)
        return {"response": True}
    else:
        # If no rows were affected, rollback the transaction
        conn.rollback()
        cursor.close()
        db_pool.putconn(conn)
        return {"response": False}


@app.get("/steam2buff")
async def read_steam2buff():
    print("Reading steam2buff")
    global steam2buff
    steam2buff = {'response': 'True'}
    conn = db_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM steam2buff")
    result = cursor.fetchall()
    cursor.close()
    db_pool.putconn(conn)
    return result

@app.get("/buff2steam")
async def read_buff2steam():
    conn = db_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buff2steam")
    result = cursor.fetchall()
    cursor.close()
    db_pool.putconn(conn)
    return result

@app.get("/buff2steam/last")
async def read_buff2steam_last():
    global buff2steam
    
    return buff2steam

@app.get("/steam2buff/last")
async def read_steam2buff_last():
    global steam2buff

    return steam2buff

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)