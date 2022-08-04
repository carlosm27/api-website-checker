import typing

from piccolo.utils.pydantic import create_pydantic_model
from piccolo.engine import engine_finder

from fastapi import FastAPI, HTTPException, status

from sql.tables import Website

WebsiteModelIn: typing.Any = create_pydantic_model(table=Website, model_name="WebsiteModelIn")

WebsiteModelOut: typing.Any = create_pydantic_model(table=Website,include_default_columns=True, model_name="WebsiteModelOut")

app = FastAPI()

@app.get("/website")
async def websites():
    try:
        website = await Website.select()
        return website
    except:
        return status.HTTP_404_NOT_FOUND

@app.post("/website", response_model= WebsiteModelOut)
async def add_website(website_model: WebsiteModelIn):
    try:
        website = Website(**website_model.__dict__)
        await website.save()
        return WebsiteModelOut(**website.__dict__)
    except:
        return status.HTTP_400_BAD_REQUEST


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


