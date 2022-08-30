
from piccolo.engine import engine_finder
from api.connectivity_checker import app_connectivity_checker
from api.crud import app_crud
from fastapi import FastAPI


app = FastAPI()


app.mount("/api/", app_connectivity_checker)
app.mount("/crud/", app_crud)


@app.on_event("startup")
async def open_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.start_connection_pool()
    except Exception:
        print("Unable to connect to the database")

@app.on_event("shutdown")
async def close_database_connection_pool():
    try:
        engine = engine_finder()
        await engine.close_connection_pool()
    except Exception:
        print("Unable to connect to the database")


if __name__=="__main__":
    app.run()