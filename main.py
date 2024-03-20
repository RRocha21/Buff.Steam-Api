from fastapi import FastAPI
import psycopg2
from psycopg2 import pool
import uvicorn

db_pool = None
app = FastAPI()

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
    conn = db_pool.getconn()
    cursor = conn.cursor()

    # Use a single query to insert the record if it doesn't exist
    cursor.execute(
        "INSERT INTO buff2steam (id, name, buff_min_price, steam_price_cny, steam_price_eur, b_o_ratio, steamUrl, buffUrl, updatedat) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) "
        "ON CONFLICT (id) DO NOTHING",
        (id, name, buff_min_price, steam_price_cny, steam_price_eur, b_o_ratio, steamUrl, buffUrl, updatedAt)
    )
    conn.commit()
    
    # Check if the total count exceeds 25, delete the oldest record if necessary
    cursor.execute(
        "SELECT COUNT(*) FROM buff2steam"
    )
    count = cursor.fetchone()[0]
    if count > 25:
        cursor.execute(
            "DELETE FROM buff2steam WHERE id IN (SELECT id FROM steam2buff ORDER BY updatedat ASC LIMIT 1)"
        )
        conn.commit()

    cursor.close()
    db_pool.putconn(conn)
    return {"response": True}

@app.post("/steam2buff")
async def insert_buff2steam(id, asset_id, price, currency, link, float_value, updatedAt):
    conn = db_pool.getconn()
    cursor = conn.cursor()

    # Use a single query to insert the record if it doesn't exist
    cursor.execute(
        "INSERT INTO steam2buff (id, asset_id, price, currency, link, float_value, updatedat) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s) "
        "ON CONFLICT (id) DO NOTHING",
        (id, asset_id, price, currency, link, float_value, updatedAt)
    )
    conn.commit()
    
    # Check if the total count exceeds 25, delete the oldest record if necessary
    cursor.execute(
        "SELECT COUNT(*) FROM steam2buff"
    )
    count = cursor.fetchone()[0]
    if count > 25:
        cursor.execute(
            "DELETE FROM steam2buff WHERE id IN (SELECT id FROM steam2buff ORDER BY updatedat ASC LIMIT 1)"
        )
        conn.commit()

    cursor.close()
    db_pool.putconn(conn)
    return {"response": True}


@app.get("/steam2buff")
async def read_steam2buff():
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
    conn = db_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM buff2steam ORDER BY updatedat DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    db_pool.putconn(conn)
    return result

@app.get("/steam2buff/last")
async def read_steam2buff_last():
    conn = db_pool.getconn()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM steam2buff ORDER BY updatedat DESC LIMIT 1")
    result = cursor.fetchone()
    cursor.close()
    db_pool.putconn(conn)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)